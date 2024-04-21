from abc import ABC, abstractmethod

from domain.workout.dto import ExerciseDTO
from domain.workout.repository import ExerciseDjangoRepository


class BaseExercise(ABC):
    def __init__(self, repository_exercise: ExerciseDjangoRepository):
        self.repository_exercise = repository_exercise

    @abstractmethod
    def create_exercise(self, data: dict) -> ExerciseDTO:
        pass


class ExerciseService(BaseExercise):
    def create_exercise(self, data: dict) -> ExerciseDTO:
        return self.repository_exercise.create(**data)
