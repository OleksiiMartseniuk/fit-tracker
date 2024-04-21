import pytest

from apps.workout.exceptions.exercise import ExerciseServiceInvalidDataException
from apps.workout.models import Exercise


@pytest.mark.django_db
def test_create_exercise(exercise_service):
    data = {
        "name": "Test Exercise",
        "description": "Test Description",
    }
    exercise = exercise_service.create_exercise(data=data)

    assert isinstance(exercise, Exercise)
    assert exercise.name == data["name"]
    assert exercise.description == data["description"]


def test_create_exercise_invalid_data(exercise_service):
    with pytest.raises(ExerciseServiceInvalidDataException):
        exercise_service.create_exercise(data={})
