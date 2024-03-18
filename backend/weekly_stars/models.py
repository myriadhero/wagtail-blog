from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


# Create your models here.
class RepeatableGoal(models.Model):
    class Complexity(models.TextChoices):
        RABBIT = "R"
        ELEPHANT = "E"
        DEADLINE = "D"

    name = models.CharField(max_length=100)
    # description = models.TextField(blank=True)
    complexity = models.CharField(
        max_length=1,
        choices=Complexity.choices,
        default=Complexity.ELEPHANT,
    )
    frequency = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")

    def __str__(self) -> str:
        return f"{self.name} - {self.complexity} - {self.frequency}"

    def get_absolute_url(self):
        return reverse("weekly_stars:goal_detail", kwargs={"pk": self.pk})


class DailyGoalCompletion(models.Model):
    date = models.DateField()
    goal = models.ForeignKey(RepeatableGoal, on_delete=models.CASCADE, related_name="completions")

    class Meta:
        unique_together = ("goal", "date")

    def __str__(self) -> str:
        return f"{self.date} - {self.goal.name}"
