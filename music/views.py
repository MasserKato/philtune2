import logging
from django.urls import reverse_lazy
from django.views import generic
from .forms import MusicCreateForm, StageCreateForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Music, Stage
from schedule.views import paginate_queryset
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now

logger = logging.getLogger(__name__)


class MusicListView(LoginRequiredMixin, generic.ListView):
    model = Music
    template_name = 'music_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        context = super(MusicListView, self).get_context_data(**kwargs)
        sql = f'SELECT * FROM music LEFT JOIN (SELECT * FROM music_stage WHERE user_id={user_id}) AS stage_table ON music.id=stage_table.music_id WHERE end_date >= current_date;'
        past_sql = f'SELECT * FROM music LEFT JOIN (SELECT * FROM music_stage WHERE user_id={user_id}) AS stage_table ON music.id=stage_table.music_id WHERE end_date < current_date;'
        music = Music.objects.raw(sql)
        past_music = Music.objects.raw(past_sql)
        page_obj = paginate_queryset(self.request, music, 10)
        past_obj = paginate_queryset(self.request, past_music, 10)
        context['page_obj'] = page_obj
        context['past_obj'] = past_obj
        return context


class MusicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Music
    template_name = 'music_detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        string_sql = f'SELECT music_stage.id, state, music_id, user_id, username, nick_name, instrument_id, part.short_name FROM music_stage LEFT JOIN (SELECT id, username, nick_name, instrument_id FROM accounts_customuser) AS customuser ON user_id=customuser.id LEFT JOIN (SELECT * FROM part) AS part ON instrument_id=part.id WHERE string is true AND music_id={pk};'
        string_stages = Stage.objects.raw(string_sql)
        context['string_stages'] = string_stages

        wind_sql = f'SELECT music_stage.id, state, music_id, user_id, username, nick_name, instrument_id, part.short_name FROM music_stage LEFT JOIN (SELECT id, username, nick_name, instrument_id FROM accounts_customuser) AS customuser ON user_id=customuser.id LEFT JOIN (SELECT * FROM part) AS part ON instrument_id=part.id WHERE string is false AND music_id={pk};'
        wind_stages = Stage.objects.raw(wind_sql)
        context['wind_stages'] = wind_stages

        your_part_sql = f'SELECT music_stage.id, state, music_id, user_id, username, nick_name, instrument_id, part.short_name FROM music_stage LEFT JOIN (SELECT id, username, nick_name, instrument_id FROM accounts_customuser) AS customuser ON user_id=customuser.id LEFT JOIN (SELECT * FROM part) AS part ON instrument_id=part.id WHERE instrument_id={self.request.user.instrument.id} AND music_id={pk};'
        your_part_stages = Stage.objects.raw(your_part_sql)
        context['your_part_stages'] = your_part_stages
        
        data_list = Stage.objects.filter(music=pk, user=self.request.user).first()
        context['stage'] = data_list
        return context


class MusicCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Music
    template_name = 'music_create.html'
    form_class = MusicCreateForm
    success_url = reverse_lazy('music:music_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def form_valid(self, form):
        music = form.save(commit=False)
        music.user = self.request.user
        music.save()
        messages.success(self.request, '曲を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "曲の作成に失敗しました。")
        return super().form_invalid(form)


class MusicUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Music
    template_name = 'music_update.html'
    form_class = MusicCreateForm

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse_lazy('music:music_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '練習予定を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "曲の更新に失敗しました。")
        return super().form_invalid(form)


class MusicDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Music
    template_name = 'Music_delete.html'
    success_url = reverse_lazy('music:music_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "曲を削除しました。")
        return super().delete(request, *args, **kwargs)


class StageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Stage
    template_name = 'stage_create.html'
    form_class = StageCreateForm

    def get_success_url(self):
        r_id = self.kwargs['pk']
        return reverse_lazy('music:music_detail', kwargs={'pk': r_id})

    def form_valid(self, form, **kwargs):
        stage = form.save(commit=False)
        stage.user = self.request.user
        stage.music = Music.objects.get(pk=self.kwargs['pk'])
        stage.save()
        messages.success(self.request, '乗り番を送信しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "乗り番の作成に失敗しました。")
        return super().form_invalid(form)


class StageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Stage
    template_name = 'stage_update.html'
    form_class = StageCreateForm

    def get_success_url(self):
        r_id = self.kwargs['pk']
        return reverse_lazy('music:music_detail', kwargs={'pk': Stage.objects.get(id=r_id).music_id})

    def form_valid(self, form):
        r_id = self.kwargs['pk']
        stage = form.save(commit=False)
        stage.user = self.request.user
        atsukau_stage = Stage.objects.get(id=r_id)
        stage.music = Music.objects.get(pk=atsukau_stage.music_id)
        stage.save()
        messages.success(self.request, '乗り番を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '回答の更新に失敗しました。')
        return super().form_invalid(form)


class StageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Stage
    template_name = 'stage_delete.html'

    def get_success_url(self):
        r_id = self.kwargs['pk']
        return reverse_lazy('music:music_detail', kwargs={'pk': Stage.objects.get(id=r_id).music_id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "降り番になりました。")
        return super().delete(request, *args, **kwargs)