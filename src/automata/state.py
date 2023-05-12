"""
The student state enum
"""

from dataclasses import dataclass
from enum import Enum


class PersonStateEnum(Enum):
    """
    The state enum of a person
    """

    COMMUTE = 1
    WORK = 2
    REST = 3
    CONSUMING_FOOD = 4
    EDUCATION = 5


class Location(Enum):
    """
    The person's location
    """

    HOME = 1
    UNIVERSITY = 2
    WHEREVER = 3


@dataclass
class CommuteAction:
    """
    The result of a person's commute
    """

    start: float
    duration: float
    to: Location
    action_type: PersonStateEnum = PersonStateEnum.COMMUTE


@dataclass
class CommuteResult:
    """
    The result of a person's commute
    """

    duration: float
    to: Location
    successful: bool = True


class WorkType(Enum):
    """
    Work type enum
    """

    IMMEDIATE = 1
    WITH_DEADLINE = 2
    SECONDARY = 3


@dataclass
class WorkAction:
    """
    The result of working. Used for both work and education
    """

    start: float
    duration: float
    work_type: WorkType
    action_type: PersonStateEnum = PersonStateEnum.WORK


@dataclass
class WorkResult:
    """
    The result of working. Used for both work and education
    """

    location: Location
    successful: bool = True


class RestType(Enum):
    """
    Rest type
    """

    SHORT = 1
    LONG = 2


@dataclass
class RestAction:
    """
    The result of restinh. Sleep, entertainment and food all count a a result
    """

    start: float
    duration: float
    rest_type: RestType
    action_type: PersonStateEnum = PersonStateEnum.REST


@dataclass
class RestResult:
    """
    The result of restinh. Sleep, entertainment and food all count a a result
    """

    rested: bool
    location: Location
    successful: bool = True


@dataclass
class EatAction:
    """
    Eat action class
    """

    start: float
    duration: float
    action_type: PersonStateEnum = PersonStateEnum.CONSUMING_FOOD


@dataclass
class EatResult:
    """
    Eat action result class
    """

    duration: float
    successful: bool = True


@dataclass
class EducationAction:
    """
    Education Action
    """

    start: float
    duration: float
    action_type: PersonStateEnum = PersonStateEnum.EDUCATION


@dataclass
class EducationResult:
    """
    The result of working. Used for both work and education
    """

    location: Location
    successful: bool = True
    proficiency: float = 1


Action = WorkAction | CommuteAction | RestAction | EatAction | EducationAction
Result = WorkResult | CommuteResult | RestResult | EatResult | EducationResult
