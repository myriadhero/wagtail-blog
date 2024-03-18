from django.contrib import admin

from .models import DailyGoalCompletion, RepeatableGoal


@admin.register(RepeatableGoal)
class RepeatableGoalAdmin(admin.ModelAdmin):
    list_display = ("name", "complexity", "frequency", "user")


@admin.register(DailyGoalCompletion)
class DailyGoalCompletionAdmin(admin.ModelAdmin):
    list_display = ("date", "goal")
