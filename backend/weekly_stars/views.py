from collections import defaultdict
from datetime import date, timedelta
from typing import Any

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, View

from .forms import NewGoalForm
from .models import DailyGoalCompletion, RepeatableGoal


@method_decorator(login_required, name="dispatch")
class WeeklyStarsView(TemplateView):
    template_name = "weekly_stars/weekly_stars.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: Instead of relative weeks, consider using week numbers from the start of the year
        week = self.request.GET.get("week", 0)
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday() + (7 * int(week)))
        end_of_week = start_of_week + timedelta(days=6)

        goals = RepeatableGoal.objects.filter(user=self.request.user).all()
        completions = (
            DailyGoalCompletion.objects.filter(
                goal__in=goals,
                date__gte=start_of_week,
                date__lte=end_of_week,
            )
            .select_related("goal")
            .all()
        )

        completions_by_goal = defaultdict(list)
        for completion in completions:
            completions_by_goal[completion.goal.pk].append(completion.date)

        context["goals_with_completions"] = defaultdict(list)
        for goal in goals:
            for day in range(7):
                cdate = start_of_week + timedelta(days=day)
                is_completed = goal.pk in completions_by_goal and cdate in completions_by_goal[goal.pk]
                context["goals_with_completions"][goal].append((cdate, is_completed))

        # Set default_factory to None to avoid issues with django templates
        context["goals_with_completions"].default_factory = None

        return context


@method_decorator(login_required, name="dispatch")
class GoalDetailView(DetailView):
    model = RepeatableGoal
    template_name = "weekly_stars/goal_detail.html"
    context_object_name = "goal"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user)

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["weekly_stars/goal_row.html"]
        return super().get_template_names()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        week = self.request.GET.get("week", 0)
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday() + (7 * int(week)))
        end_of_week = start_of_week + timedelta(days=6)

        completions = [
            c.date for c in self.object.completions.filter(date__gte=start_of_week, date__lte=end_of_week).all()
        ]
        context["completions"] = [
            ((cdate := start_of_week + timedelta(days=day)), cdate in completions) for day in range(7)
        ]

        return context


@method_decorator(login_required, name="dispatch")
class GoalCreateView(CreateView):
    model = RepeatableGoal
    form_class = NewGoalForm
    context_object_name = "goal"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.headers.get("HX-Request"):
            return self.object.get_absolute_url()
        return reverse("weekly_stars:weekly_stars")

    def get_template_names(self) -> list[str]:
        # if POST request, return the default template
        if self.request.method == "POST":
            return ["weekly_stars/goal_row.html"]
        return ["weekly_stars/new_goal_form.html"]


@method_decorator(login_required, name="dispatch")
class GoalUpdateDeleteView(UpdateView):
    model = RepeatableGoal
    template_name = "weekly_stars/goal_form.html"
    fields = ("name", "complexity", "frequency")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        if self.request.headers.get("HX-Request"):
            return self.object.get_absolute_url()
        return reverse("weekly_stars:weekly_stars")

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then return empty 200 response for HTMX.
        """
        goal = self.get_object()
        goal.delete()
        if self.request.headers.get("HX-Request"):
            return HttpResponse()
        return self.get_success_url()


@method_decorator(login_required, name="dispatch")
class CompletionCreateDeleteView(View):
    template = "weekly_stars/goal_completion.html"

    def validate_goal(self, request) -> RepeatableGoal:
        goal = RepeatableGoal.objects.get(pk=self.kwargs.get("goal_pk"), user=request.user)
        return goal

    def post(self, request, *args, **kwargs):
        goal = self.validate_goal(request)
        completion_date = date(
            year=kwargs["year"],
            month=kwargs["month"],
            day=kwargs["day"],
        )
        completion, created = goal.completions.get_or_create(date=completion_date)

        if request.headers.get("HX-Request"):
            return render(request, self.template, {"goal": goal, "completion": (completion_date, True)})
        return HttpResponseRedirect(reverse("weekly_stars:weekly_stars"))

    def delete(self, request, *args, **kwargs):
        goal = self.validate_goal(request)
        completion_date = date(
            year=kwargs["year"],
            month=kwargs["month"],
            day=kwargs["day"],
        )
        completion = goal.completions.filter(date=completion_date).first()
        if completion:
            completion.delete()

        if request.headers.get("HX-Request"):
            return render(request, self.template, {"goal": goal, "completion": (completion_date, False)})
        return HttpResponseRedirect(reverse("weekly_stars:weekly_stars"))
