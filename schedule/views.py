import logging
from django.urls import reverse_lazy
from django.views import generic
from .forms import InquiryForm, ScheduleCreateForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Schedule
from django.utils.timezone import now

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('schedule:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class ScheduleListView(LoginRequiredMixin, generic.ListView):
    model = Schedule
    template_name = 'schedule_list.html'
    paginate_by = 2

    def get_queryset(self):
        schedules = Schedule.objects.order_by('-created_at')
        return schedules


class ScheduleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Schedule
    template_name = 'schedule_detail.html'


class ScheduleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Schedule
    template_name = 'schedule_create.html'
    form_class = ScheduleCreateForm
    success_url = reverse_lazy('schedule:schedule_list')

    def form_valid(self, form):
        schedule = form.save(commit=False)
        schedule.user = self.request.user
        schedule.save()
        messages.success(self.request, '練習予定を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "練習予定の作成に失敗しました。")
        return super().form_invalid(form)


class ScheduleUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Schedule
    template_name = 'schedule_update.html'
    form_class = ScheduleCreateForm

    def get_success_url(self):
        return reverse_lazy('schedule:schedule_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '練習予定を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "練習予定の更新に失敗しました。")
        return super().form_invalid(form)


class ScheduleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Schedule
    template_name = 'schedule_delete.html'
    success_url = reverse_lazy('schedule:schedule_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "練習予定を削除しました。")
        return super().delete(request, *args, **kwargs)
