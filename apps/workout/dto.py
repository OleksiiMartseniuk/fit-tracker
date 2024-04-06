from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.workout.models import (
        Exercise,
        ExerciseResult,
        Set,
        Workout,
        WorkoutSession,
    )


@dataclass
class WorkoutDTO:
    name: str
    description: str
    publish: bool
    owner: int | None
    exercises: list[int] | None

    @classmethod
    def from_model(cls, workout: "Workout") -> "WorkoutDTO":
        return cls(
            name=workout.name,
            description=workout.description,
            publish=workout.publish,
            owner=workout.owner_id,
            exercises=list(workout.exercises.values_list("id", flat=True)),
        )


@dataclass
class ExerciseDTO:
    name: str
    description: str | None
    sets_to_complete: int | None
    repetitions_per_set: int | None
    distance: float | None
    image: str | None

    @classmethod
    def from_model(cls, exercise: "Exercise") -> "ExerciseDTO":
        return cls(
            name=exercise.name,
            description=exercise.description,
            sets_to_complete=exercise.sets_to_complete,
            repetitions_per_set=exercise.repetitions_per_set,
            distance=exercise.distance,
            image=exercise.image.url,
        )


@dataclass
class WorkoutSessionDTO:
    user: int
    workout: int
    date: datetime
    duration: int | None

    @classmethod
    def from_model(cls, workout_session: "WorkoutSession") -> "WorkoutSessionDTO":
        return cls(
            user=workout_session.user_id,
            workout=workout_session.workout_id,
            date=workout_session.date,
            duration=workout_session.duration,
        )


@dataclass
class ExerciseResultDTO:
    user: int
    exercise: int
    session: int
    sets: list[int] | None
    duration: int | None
    distance: float | None
    notes: str | None

    @classmethod
    def from_model(cls, exercise_result: "ExerciseResult") -> "ExerciseResultDTO":
        return cls(
            user=exercise_result.user_id,
            exercise=exercise_result.exercise_id,
            session=exercise_result.session_id,
            sets=list(exercise_result.sets.values_list("id", flat=True)),
            duration=exercise_result.duration,
            distance=exercise_result.distance,
            notes=exercise_result.notes,
        )


@dataclass
class SetDTO:
    exercise_result: int
    set_number: int
    repetitions: int

    @classmethod
    def from_model(cls, set: "Set") -> "SetDTO":
        return cls(
            exercise_result=set.exercise_result_id,
            set_number=set.set_number,
            repetitions=set.repetitions,
        )
