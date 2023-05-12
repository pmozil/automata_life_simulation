"""
The stack of actions thet the person has to execute
"""

from .state import (Action, CommuteAction, EatAction, EducationAction,
                    RestAction, WorkAction)


class EventQueue:
    """
    The event stack class.
    """

    def __init__(self):
        """
        Init for EventStack
        """
        self.__event_queue: list[Action] = []

    def __len__(self) -> int:
        """
        Get queue length
        """
        return len(self.__event_queue)

    def peek_front(self) -> Action | None:
        """
        Get the first element of queue without mutating self
        """
        return self.__event_queue[0] if self.__event_queue else None

    def pop_front(self) -> Action | None:
        """
        Pop from the front of the stack
        """
        return self.__event_queue.pop(0) if self.__event_queue else None

    def peek_back(self) -> Action | None:
        """
        Get the last element of queue without mutating self
        """
        return self.__event_queue[-1] if self.__event_queue else None

    def pop_back(self) -> Action | None:
        """
        Pop from the back of te queue
        """
        return self.__event_queue.pop(-1) if self.__event_queue else None

    def push_front(self, action: Action):
        """
        Push into the front of the queue
        """
        self.__event_queue = [action] + self.__event_queue

    def push_back(self, action: Action):
        """
        Push into the back of the queue
        """
        self.__event_queue.append(action)

    def remove(self, action: Action):
        """
        Remove action from queue
        """
        if action in self.__event_queue:
            self.__event_queue.remove(action)

    def push_after_next_work(self, new_action: Action):
        """
        Push after next work action
        """
        for idx, action in enumerate(self.__event_queue):
            if isinstance(action, WorkAction):
                self.__event_queue.insert(idx + 1, new_action)
                break
        else:
            self.__event_queue.append(new_action)

    def push_after_next_commute(self, new_action: Action):
        """
        Push after next commute action
        """
        for idx, action in enumerate(self.__event_queue):
            if isinstance(action, CommuteAction):
                self.__event_queue.insert(idx + 1, new_action)
                break
        else:
            self.__event_queue.append(new_action)

    def push_after_next_rest(self, new_action: Action):
        """
        Push after next rest action
        """
        for idx, action in enumerate(self.__event_queue):
            if isinstance(action, RestAction):
                self.__event_queue.insert(idx + 1, new_action)
                break
        else:
            self.__event_queue.append(new_action)

    def push_after_next_eat(self, new_action: Action):
        """
        Push after next eat action
        """
        for idx, action in enumerate(self.__event_queue):
            if isinstance(action, EatAction):
                self.__event_queue.insert(idx + 1, new_action)
                break
        else:
            self.__event_queue.append(new_action)

    def push_after_next_education(self, new_action: Action):
        """
        Push after next eat action
        """
        for idx, action in enumerate(self.__event_queue):
            if isinstance(action, EducationAction):
                self.__event_queue.insert(idx + 1, new_action)
                break
        else:
            self.__event_queue.append(new_action)

    def contains(self, action: type) -> bool:
        """
        Check if queue contains action
        """
        return any(isinstance(act, action) for act in self.__event_queue)

    def filter_non_permanent(self):
        """
        Remove eat sleep and commute actions
        """
        self.__event_queue = list(
            filter(
                lambda x: isinstance(x, WorkAction)
                or isinstance(x, EducationAction),
                self.__event_queue,
            )
        )
