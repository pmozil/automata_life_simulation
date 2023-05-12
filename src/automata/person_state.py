"""
The person state
"""

import random
from dataclasses import dataclass

from .event_queue import EventQueue
from .state import (Action, CommuteAction, CommuteResult, EatAction, EatResult,
                    EducationAction, EducationResult, Location,
                    PersonStateEnum, RestAction, RestResult, RestType, Result,
                    WorkAction, WorkResult, WorkType)


@dataclass
class PersonState:
    """
    The person state class
    """

    event_queue: EventQueue
    current_state: PersonStateEnum
    current_location: Location = Location.HOME
    current_action: Action | None = None
    is_rested: bool = True
    is_fed: bool = True
    proficiency: float = 1

    def next_state(self, current_time: float) -> Action | None:
        """
        Go to next action if the current is finished
        """

        if not (current_time % 24):
            self.event_queue.filter_non_permanent()

        if self.current_action is not None:
            action = self.current_action
            result, is_done = self.process_action(action, current_time)

            if not is_done or result is None or not result.successful:
                print(f"Current state is {self.current_state}")
                return

            self.current_action = None

        if self.current_location != Location.HOME:
            self.push_commute(
                CommuteAction(
                    start=current_time,
                    duration=1 * random.uniform(0.5, 1.5),
                    to=Location.HOME,
                )
            )

        if random.uniform(0, 1) > 0.7:
            self.push_commute(
                CommuteAction(
                    start=current_time,
                    duration=1 * random.uniform(0.5, 1.5),
                    to=random.choice([Location.UNIVERSITY, Location.WHEREVER]),
                )
            )

        if len(self.event_queue) < 5:
            self.push_education(
                EducationAction(
                    start=current_time,
                    duration=1 * random.uniform(0, 6),
                )
            )

        if random.uniform(0, 1) > 0.2:
            self.push_work(
                WorkAction(
                    start=current_time,
                    duration=2 * random.uniform(0.3, 4),
                    work_type=random.choice(
                        [
                            WorkType.SECONDARY,
                            WorkType.WITH_DEADLINE,
                            WorkType.IMMEDIATE,
                        ]
                    ),
                )
            )

        if (
            current_time >= 22
            or current_time <= 4
            or random.uniform(0, 1) > 0.9
        ) and not self.event_queue.contains(RestAction):
            self.push_rest(
                RestAction(
                    start=current_time,
                    duration=4 * random.uniform(0, 3),
                    rest_type=random.choice([RestType.SHORT, RestType.LONG]),
                )
            )
        elif random.uniform(0, 1) > 0.6:
            self.push_eat(
                EatAction(
                    start=current_time, duration=0.32 * random.uniform(0.8, 3)
                )
            )

        if (
            current_time >= 22
            or current_time <= 4
            and not self.event_queue.contains(RestAction)
        ):
            self.is_rested = False

        if self.current_action is None:
            self.current_action = self.event_queue.pop_front()
            if self.current_action is not None:
                self.current_state = self.current_action.action_type
            return self.current_action

    def process_action(
        self, action: Action, current_time: float
    ) -> tuple[Result | None, bool]:
        """
        Check if action passes. Work can fail
        """
        if (
            action is None
            or (current_time - action.duration) % 24 < action.start
        ):
            return None, False

        if isinstance(action, WorkAction):
            result = self.process_work(action)
            self.is_rested = False
            if not result.successful:
                action = WorkAction(
                    start=current_time,
                    duration=action.duration,
                    work_type=action.work_type,
                )
                self.push_work(action)
                print("No luck doing the work. Will try again >:-[")
                return result, True

            self.push_rest(
                RestAction(
                    start=current_time,
                    duration=0.5 * random.uniform(0, 1),
                    rest_type=RestType.SHORT,
                )
            )

            print("The work is all done!")
            return result, True

        if isinstance(action, CommuteAction):
            match action.to:
                case Location.HOME:
                    print("Going home")
                case Location.UNIVERSITY:
                    print("Going to university")
                case Location.WHEREVER:
                    print("Going somewhere that is not home or university")
            result = self.process_commmute(action)
            self.current_location = result.to
            self.push_education(
                EducationAction(
                    start=current_time,
                    duration=1 * random.uniform(0, 6),
                )
            )
            return result, True

        if isinstance(action, RestAction):
            print("Going to rest")
            result = self.process_rest()
            self.is_rested = result.rested
            return result, True

        if isinstance(action, EatAction):
            print("Need to eat something")
            self.fed = True
            return EatResult(duration=action.duration), True

        if isinstance(action, EducationAction):
            print("Gonna study")
            result = self.process_education(action)
            self.proficiency *= result.proficiency
            print(f"Increased proficiency by {result.proficiency}")
            return result, True

    def push_work(self, action: WorkAction):
        """
        Push work onto queue
        """
        match action.work_type:
            case WorkType.IMMEDIATE:
                self.event_queue.push_front(action)
            case WorkType.WITH_DEADLINE:
                self.event_queue.push_after_next_commute(action)
            case WorkType.SECONDARY:
                self.event_queue.push_after_next_rest(action)

    def process_work(self, action: WorkAction) -> WorkResult:
        """
        Process the work action
        """
        fail_probablility = 1 * (action.duration**0.00001)

        if not self.is_rested:
            fail_probablility *= 0.9

        if not self.is_fed:
            fail_probablility *= 0.9

        match self.current_location:
            case Location.HOME | Location.UNIVERSITY:
                fail_probablility *= 0.95
            case Location.WHEREVER:
                fail_probablility *= 0.5

        return WorkResult(
            successful=random.uniform(0, 1) <= fail_probablility,
            location=self.current_location,
        )

    def push_commute(self, action: CommuteAction):
        """
        Push commute action
        """
        self.event_queue.push_front(action)

    def process_commmute(self, action: CommuteAction) -> CommuteResult:
        """
        Process commute action
        """
        return CommuteResult(duration=action.duration, to=action.to)

    def push_rest(self, action: RestAction):
        """
        Push next rest action
        """
        self.event_queue.push_after_next_work(action)

    def process_rest(self) -> RestResult:
        """
        Process rested
        """
        return RestResult(
            rested=random.uniform(0, 1) < 0.9, location=self.current_location
        )

    def push_eat(self, action: EatAction):
        """
        Push eat action
        """
        self.event_queue.push_after_next_commute(action)

    def push_education(self, action: EducationAction):
        """
        Push EducationAction
        """
        self.event_queue.push_after_next_eat(action)

    def process_education(self, action: EducationAction) -> EducationResult:
        """
        Process education action
        """
        fail_probablility = 1

        if not self.is_rested:
            fail_probablility *= 0.7

        if not self.is_fed:
            fail_probablility *= 0.8

        match self.current_location:
            case Location.HOME:
                fail_probablility *= 0.95
            case Location.WHEREVER:
                fail_probablility *= 0.4

        return EducationResult(
            successful=random.uniform(0, 1) < fail_probablility,
            location=self.current_location,
            proficiency=action.duration**0.0001 + 0.5,
        )
