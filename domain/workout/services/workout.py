from abc import ABC, abstractmethod

from domain.workout.dto import WorkoutDTO
from domain.workout.repository import WorkoutDjangoRepository


class BaseWorkout(ABC):
    def __init__(self, repository_workout: WorkoutDjangoRepository):
        self.repository_workout = repository_workout

    @abstractmethod
    def create_workout(self, data: dict) -> WorkoutDTO:
        pass

    @abstractmethod
    def update_workout(self, workout_id: int, data: dict) -> WorkoutDTO:
        pass


class WorkoutService(BaseWorkout):
    def create_workout(self, data: dict) -> WorkoutDTO:
        return self.repository_workout.create(**data)

    def update_workout(self, workout_id: int, data: dict) -> WorkoutDTO:
        return self.repository_workout.update(
            id_item=workout_id,
            update_fields=True,
            **data,
        )
