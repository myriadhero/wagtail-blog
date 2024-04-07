from django.urls import path

from .views import (
    CompletionCreateDeleteView,
    GoalCreateView,
    GoalDetailView,
    GoalUpdateDeleteView,
    LastThirtyStarsView,
    WeeklyStarsView,
)

app_name = "weekly_stars"

urlpatterns = [
    path("", WeeklyStarsView.as_view(), name="weekly_stars"),
    path("thirty/", LastThirtyStarsView.as_view(), name="thirty_stars"),
    path("goal/", GoalCreateView.as_view(), name="goal_new"),  # POST
    path("goal/<int:pk>/", GoalDetailView.as_view(), name="goal_detail"),  # GET
    path("goal/<int:pk>/update/", GoalUpdateDeleteView.as_view(), name="goal_edit_delete"),  # POST, DELETE
    path(
        "goal/<int:goal_pk>/complete/<int:year>-<int:month>-<int:day>/",
        CompletionCreateDeleteView.as_view(),
        name="toggle_completion",
    ),
]
