import pytest

from apps.workout.exceptions.workout import WorkoutProgramServiceInvalidDataException
from apps.workout.models import Exercise, WorkoutProgram


@pytest.mark.django_db
def test_create_workout_program(workout_program_service):
    data = {
        "name": "Test Workout Program",
        "description": "Test Description",
    }
    workout_program = workout_program_service.create_workout_program(data=data)

    assert workout_program.name == data["name"]
    assert workout_program.description == data["description"]


def test_create_workout_program_invalid_data(workout_program_service):
    with pytest.raises(WorkoutProgramServiceInvalidDataException):
        workout_program_service.create_workout_program(data={})


@pytest.mark.django_db
def test_add_exercise_to_program(workout_program_service):
    exercise = Exercise(name="Test Exercise", description="Test Description")
    program = WorkoutProgram.objects.create(
        name="Test Program",
        description="Test Description",
    )

    assert program.exercises.exists() is False

    workout_program_service.add_exercise_to_program(
        program=program,
        exercise=exercise,
    )

    exercise_from_program = program.exercises.first()
    assert exercise_from_program == exercise
