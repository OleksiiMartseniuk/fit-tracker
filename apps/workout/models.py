from django.conf import settings
from django.db import models


class WorkoutProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    exercises = models.ManyToManyField(
        "Exercise",
        related_name="workout_programs",
        blank=True,
    )
    publish = models.BooleanField(default=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workout_programs",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"[{self.id}] {self.name}"


class Exercise(models.Model):
    class DifficultyChoices(models.TextChoices):
        EASY = "easy"
        MODERATE = "moderate"
        DIFFICULT = "difficult"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    equipment_required = models.ForeignKey(
        "Equipment",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    muscle_group = models.ForeignKey(
        "MuscleGroup", on_delete=models.SET_NULL, blank=True, null=True
    )
    difficulty = models.CharField(
        max_length=15,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.EASY,
    )
    sets_to_complete = models.PositiveIntegerField(
        help_text="Number of sets to complete the exercise",
        blank=True,
        null=True,
    )
    repetitions_per_set = models.PositiveIntegerField(
        help_text="Number of repetitions per set",
        blank=True,
        null=True,
    )
    distance = models.FloatField(
        help_text="Running distance in meters",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="exercise_images/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"[{self.id}] {self.name}"


class Equipment(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"[{self.id}] {self.slug}"


class MuscleGroup(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"[{self.id}] {self.slug}"


class WorkoutSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    program = models.ForeignKey(
        WorkoutProgram,
        on_delete=models.CASCADE,
    )
    date = models.DateField()
    duration = models.DurationField(
        blank=True,
        null=True,
    )


class ExerciseResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
    )
    session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
    )
    sets = models.ManyToManyField(
        "Set",
        blank=True,
    )
    duration = models.DurationField(
        blank=True,
        null=True,
    )
    distance = models.FloatField(
        blank=True,
        null=True,
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return (
            f"[{self.id}] {self.user.username} - "
            f"{self.exercise.name} - {self.session.date}"
        )


class Set(models.Model):
    exercise_result = models.ForeignKey(
        ExerciseResult,
        on_delete=models.CASCADE,
    )
    set_number = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()
    weight = models.FloatField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return (
            f"[{self.id}] Set {self.set_number} - "
            f"Reps: {self.repetitions} - Weight: {self.weight}"
        )
