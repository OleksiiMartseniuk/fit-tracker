from django.contrib import admin

from apps.workout.models import Exercise, ExerciseResult, Set, Workout, WorkoutSession


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ["name", "publish", "owner"]
    raw_id_fields = ["owner"]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["name", "sets_to_complete", "repetitions_per_set"]


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ["user", "workout", "date", "duration"]
    raw_id_fields = ["user", "workout"]


@admin.register(ExerciseResult)
class ExerciseResultAdmin(admin.ModelAdmin):
    list_display = ["user", "exercise", "session"]
    raw_id_fields = ["user", "exercise", "session"]


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ["exercise_result", "set_number", "repetitions"]
    raw_id_fields = ["exercise_result"]
