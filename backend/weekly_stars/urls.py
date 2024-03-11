from django.urls import path

from .views import GoalCreateView, GoalDetailView, GoalUpdateDeleteView, WeeklyStarsView

app_name = "weekly_stars"

urlpatterns = [
    path("", WeeklyStarsView.as_view(), name="weekly_stars"),
    path("goal/<int:pk>/", GoalDetailView.as_view(), name="goal_detail"),  # GET
    path("goal/", GoalCreateView.as_view(), name="goal_new"),  # POST
    path("goal/<int:pk>/", GoalUpdateDeleteView.as_view(), name="goal_edit"),  # POST
    path("goal/<int:pk>/", GoalUpdateDeleteView.as_view(), name="goal_delete"),  # DELETE
]
