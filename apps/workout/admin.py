from django.contrib import admin

from apps.workout.models import (
    Equipment,
    Exercise,
    ExerciseResult,
    MuscleGroup,
    Set,
    WorkoutProgram,
    WorkoutSession,
)


@admin.register(WorkoutProgram)
class WorkoutProgramAdmin(admin.ModelAdmin):
    list_display = ["name", "publish", "owner"]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["name", "difficulty", "sets_to_complete", "repetitions_per_set"]


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ["user", "program", "date", "duration"]


@admin.register(ExerciseResult)
class ExerciseResultAdmin(admin.ModelAdmin):
    list_display = ["user", "exercise", "session"]


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ("exercise_result", "set_number", "repetitions", "weight")
