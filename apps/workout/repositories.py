from apps.utils.mixins import DjangoCRUDMixin
from apps.utils.repository import Repository
from apps.workout.dto import (
    ExerciseDTO,
    ExerciseResultDTO,
    SetDTO,
    WorkoutDTO,
    WorkoutSessionDTO,
)
from apps.workout.exceptions.workout import WorkoutItemNotFoundException
from apps.workout.models import Exercise, ExerciseResult, Set, Workout, WorkoutSession


class WorkoutDjangoRepository(DjangoCRUDMixin[WorkoutDTO], Repository[WorkoutDTO]):
    def __init__(self):
        self.model = Workout
        self.dto = WorkoutDTO

    def add_exercise_to_workout(self, workout_id: int, exercise_id: int) -> None:
        try:
            workout = Workout.objects.get(id=workout_id)
            workout.exercises.add(exercise_id)
        except self.model.DoesNotExist:
            raise WorkoutItemNotFoundException(
                f"Workout with id {workout_id} not found",
            )
        except Exception:
            raise WorkoutItemNotFoundException(
                f"Exercise with id {exercise_id} not found",
            )


class ExerciseDjangoRepository(DjangoCRUDMixin[ExerciseDTO], Repository[ExerciseDTO]):
    def __init__(self):
        self.model = Exercise
        self.dto = ExerciseDTO


class WorkoutSessionDjangoRepository(
    DjangoCRUDMixin[WorkoutSessionDTO],
    Repository[WorkoutSessionDTO],
):
    def __init__(self):
        self.model = WorkoutSession
        self.dto = WorkoutSessionDTO


class ExerciseResultDjangoRepository(
    DjangoCRUDMixin[ExerciseResultDTO],
    Repository[ExerciseResultDTO],
):
    def __init__(self):
        self.model = ExerciseResult
        self.dto = ExerciseResultDTO


class SetDjangoRepository(DjangoCRUDMixin[SetDTO], Repository[SetDTO]):
    def __init__(self):
        self.model = Set
        self.dto = SetDTO
