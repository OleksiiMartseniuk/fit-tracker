from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorkoutDTO:
    id: int
    name: str
    description: str
    publish: bool
    owner: int | None
    exercises: list[int] | None


@dataclass
class ExerciseDTO:
    id: int
    name: str
    description: str | None
    sets_to_complete: int | None
    repetitions_per_set: int | None
    distance: float | None
    image: str | None


@dataclass
class WorkoutSessionDTO:
    id: int
    user: int
    workout: int
    date: datetime
    duration: int | None


@dataclass
class ExerciseResultDTO:
    id: int
    user: int
    exercise: int
    session: int
    sets: list[int] | None
    duration: int | None
    distance: float | None
    notes: str | None


@dataclass
class SetDTO:
    id: int
    exercise_result: int
    set_number: int
    repetitions: int
