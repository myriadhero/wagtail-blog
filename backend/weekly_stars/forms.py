from django import forms

from .models import RepeatableGoal


class NewGoalForm(forms.ModelForm):
    class Meta:
        model = RepeatableGoal
        fields = ("name", "complexity", "frequency")
