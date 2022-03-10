import logging
from django.urls import reverse_lazy
from django.views import generic
from .forms import InquiryForm, ScheduleCreateForm, ReactionCreateForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Schedule, Reaction
from music.models import Music
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"


class HelpView(generic.TemplateView):
    template_name = "help.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('schedule:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


@login_required
def schedule_index(request):
    user_id = request.user.id
    sql = f'SELECT * FROM schedule_schedule LEFT JOIN (SELECT * FROM schedule_reaction WHERE user_id={user_id}) AS reaction_table ON schedule_schedule.id=reaction_table.schedule_id;'
    schedule = Schedule.objects.raw(sql)
    page_obj = paginate_queryset(request, schedule, 10)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'schedule_list.html', context)


class ScheduleListView(LoginRequiredMixin, generic.ListView):
    model = Schedule
    template_name = 'schedule_list.html'
    paginate_by = 2

    def get_queryset(self):
        schedules = Schedule.objects.order_by('-created_at')
        return schedules
"""
    def get_context_data(self, **kwargs):
        context = super(ScheduleListView, self).get_context_data(**kwargs)
        context['reaction'] = Reaction.objects.get(user=self.request.user)
        return context
"""


class ScheduleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Schedule
    template_name = 'schedule_detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)

        schedule = Schedule.objects.get(id=pk)

        for music in schedule.music.all():
            sql = f"SELECT reaction.state, reaction.comment, music_stage.id, music_stage.state, username, nick_name, part.short_name FROM music_stage LEFT JOIN accounts_customuser ON user_id=accounts_customuser.id LEFT JOIN part ON instrument_id=part.id LEFT JOIN (SELECT * FROM schedule_reaction WHERE schedule_id={pk}) AS reaction ON reaction.user_id=music_stage.user_id WHERE music_id=1;"

            string_sql = f"SELECT reaction.state AS syukketu, reaction.comment, music_stage.id, music_stage.state AS noriban, username, nick_name, part.short_name FROM music_stage LEFT JOIN accounts_customuser ON user_id=accounts_customuser.id LEFT JOIN part ON instrument_id=part.id LEFT JOIN (SELECT * FROM schedule_reaction WHERE schedule_id={pk}) AS reaction ON reaction.user_id=music_stage.user_id WHERE music_id={music.id} AND string is true;"
            string_reactions = Reaction.objects.raw(string_sql)
            context[f'{music.category}_string_reactions'] = string_reactions

            wind_sql = f"SELECT reaction.state AS syukketu, reaction.comment, music_stage.id, music_stage.state AS noriban, username, nick_name, part.short_name FROM music_stage LEFT JOIN accounts_customuser ON user_id=accounts_customuser.id LEFT JOIN part ON instrument_id=part.id LEFT JOIN (SELECT * FROM schedule_reaction WHERE schedule_id={pk}) AS reaction ON reaction.user_id=music_stage.user_id WHERE music_id={music.id} AND wind is true;"
            wind_reactions = Reaction.objects.raw(wind_sql)
            context[f'{music.category}_wind_reactions'] = wind_reactions

            your_part_sql = f"SELECT reaction.state AS syukketu, reaction.comment, music_stage.id, music_stage.state AS noriban, username, nick_name, part.short_name FROM music_stage LEFT JOIN accounts_customuser ON user_id=accounts_customuser.id LEFT JOIN part ON instrument_id=part.id LEFT JOIN (SELECT * FROM schedule_reaction WHERE schedule_id={pk}) AS reaction ON reaction.user_id=music_stage.user_id WHERE music_id=1 AND instrument_id={self.request.user.instrument.id};"
            your_part_reactions = Reaction.objects.raw(your_part_sql)
            context[f'{music.category}_your_part_reactions'] = your_part_reactions
        
        data_list = Reaction.objects.filter(schedule=self.kwargs['pk'], user=self.request.user).first()
        context['reaction']=data_list
        return context


class ScheduleCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Schedule
    template_name = 'schedule_create.html'
    form_class = ScheduleCreateForm
    success_url = reverse_lazy('schedule:schedule_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def form_valid(self, form):
        schedule = form.save(commit=False)
        schedule.user = self.request.user
        schedule.save()
        messages.success(self.request, '練習予定を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "練習予定の作成に失敗しました。")
        return super().form_invalid(form)


class ScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Schedule
    template_name = 'schedule_update.html'
    form_class = ScheduleCreateForm

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse_lazy('schedule:schedule_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '練習予定を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "練習予定の更新に失敗しました。")
        return super().form_invalid(form)


class ScheduleDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Schedule
    template_name = 'schedule_delete.html'
    success_url = reverse_lazy('schedule:schedule_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "練習予定を削除しました。")
        return super().delete(request, *args, **kwargs)


class ReactionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Reaction
    template_name = 'reaction_create.html'
    form_class = ReactionCreateForm

    def get_success_url(self):
        r_id = self.kwargs['pk']
        return reverse_lazy('schedule:schedule_detail', kwargs={'pk': r_id})

    def form_valid(self, form, **kwargs):
        reaction = form.save(commit=False)
        reaction.user = self.request.user
        reaction.schedule = Schedule.objects.get(pk=self.kwargs['pk'])
        reaction.save()
        messages.success(self.request, '回答を送信しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "回答の作成に失敗しました。")
        return super().form_invalid(form)


class ReactionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Reaction
    template_name = 'reaction_update.html'
    form_class = ReactionCreateForm

    def get_success_url(self):
        r_id = self.kwargs['pk']
        return reverse_lazy('schedule:schedule_detail', kwargs={'pk': Reaction.objects.get(id=r_id).schedule_id})

    def form_valid(self, form):
        r_id = self.kwargs['pk']
        reaction = form.save(commit=False)
        reaction.user = self.request.user
        atsukau_reaction = Reaction.objects.get(id=r_id)
        reaction.schedule = Schedule.objects.get(pk=atsukau_reaction.schedule_id)
        reaction.save()
        messages.success(self.request, '回答を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '回答の更新に失敗しました。')
        return super().form_invalid(form)
