from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import NewGoalForm
from .models import RepeatableGoal


@method_decorator(login_required, name="dispatch")
class WeeklyStarsView(TemplateView):
    template_name = "weekly_stars/weekly_stars.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: Instead of relative weeks, consider using week numbers from the start of the year
        week = self.request.GET.get("week", 0)
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday() + (7 * int(week)))
        end_of_week = start_of_week + timedelta(days=6)

        context["goals"] = RepeatableGoal.objects.filter(
            user=self.request.user,
            completions__date__gte=start_of_week,
            completions__date__lte=end_of_week,
        ).select_related("completions")

        return context


@method_decorator(login_required, name="dispatch")
class GoalDetailView(DetailView):
    model = RepeatableGoal
    template_name = "weekly_stars/goal_detail.html"
    context_object_name = "goal"


class GoalCreateView(CreateView):
    model = RepeatableGoal
    form_class = NewGoalForm
    template_name = "weekly_stars/goal_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GoalUpdateDeleteView(UpdateView):
    model = RepeatableGoal
    template_name = "weekly_stars/goal_form.html"
    fields = ("name", "complexity", "frequency")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then return empty 200 response for HTMX.
        """
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse()
