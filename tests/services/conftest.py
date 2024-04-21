import pytest

from apps.account.services.auth import AuthorizationTokenService
from domain.workout.services.exercise import ExerciseService
from domain.workout.services.workout import WorkoutProgramService


@pytest.fixture
def authorization_token_service() -> AuthorizationTokenService:
    return AuthorizationTokenService()


@pytest.fixture
def exercise_service() -> ExerciseService:
    return ExerciseService()


@pytest.fixture
def workout_program_service(mocker) -> WorkoutProgramService:
    return WorkoutProgramService(exercise_service=mocker.MagicMock())
