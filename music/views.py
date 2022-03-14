import logging
from django.urls import reverse_lazy
from django.views import generic
from .forms import MusicCreateForm, StageCreateForm, ConcertCreateForm, TermCreateForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Music, Stage, Concert, Term
from schedule.views import paginate_queryset
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

logger = logging.getLogger(__name__)


class MusicListView(LoginRequiredMixin, generic.ListView):
    model = Term
    template_name = 'music_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        if self.request.user.instrument is None:
            messages.warning(self.request, 'パートが登録されていません！！マイページからパートを登録してください。')
        user_id = self.request.user.id
        context = super(MusicListView, self).get_context_data(**kwargs)

        this_term = Term.objects.filter(end_date__gte=datetime.date.today()).order_by("end_date").first()
        next_term = Term.objects.filter(end_date__gt=this_term.end_date).order_by("end_date").first()
        terms = Term.objects.order_by("-end_date")

        this_term_concerts = Concert.objects.filter(term=this_term)
        next_term_concerts = Concert.objects.filter(term=next_term)

        this_term_id = this_term.id
        this_sql = (f'SELECT * FROM music '
                f'LEFT JOIN (SELECT * FROM music_stage WHERE user_id={user_id}) AS stage_table '
                f'ON music.id=stage_table.music_id '
                f'WHERE music.term_id={this_term_id};')
        this_term_musics = Music.objects.raw(this_sql)

        next_term_id = next_term.id
        next_sql = (f'SELECT * FROM music '
                f'LEFT JOIN (SELECT * FROM music_stage WHERE user_id={user_id}) AS stage_table '
                f'ON music.id=stage_table.music_id '
                f'WHERE music.term_id={next_term_id};')
        next_term_musics = Music.objects.raw(next_sql)

        context['this_term'] = this_term
        context['this_term_concerts'] = this_term_concerts
        context['this_term_musics'] = this_term_musics
        context['next_term'] = next_term
        context['next_term_concerts'] = next_term_concerts
        context['next_term_musics'] = next_term_musics
        context['terms'] = paginate_queryset(self.request, terms, 10)
        return context


class MusicDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Music
    template_name = 'music_detail.html'

    def test_func(self):
        if self.request.user.instrument is None:
            return False
        else:
            return True

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        string_sql = f'SELECT music_stage.id, state, music_id, user_id, username, nick_name, instrument_id, part.short_name FROM music_stage LEFT JOIN (SELECT id, username, nick_name, instrument_id FROM accounts_customuser) AS customuser ON user_id=customuser.id LEFT JOIN (SELECT * FROM part) AS part ON instrument_id=part.id WHERE string is true AND music_id={pk} ORDER BY instrument_id;'
        string_stages = Stage.objects.raw(string_sql)
        context['string_stages'] = string_stages

        wind_sql = f'SELECT music_stage.id, state, music_id, user_id, username, nick_name, instrument_id, part.short_name FROM music_stage LEFT JOIN (SELECT id, username, nick_name, instrument_id FROM accounts_customuser) AS customuser ON user_id=customuser.id LEFT JOIN (SELECT * FROM part) AS part ON instrument_id=part.id WHERE string is false AND music_id={pk} ORDER BY instrument_id;'
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

    def form_valid(self, form, **kwargs):
        music = form.save(commit=False)
        music.term = Term.objects.get(pk=self.kwargs['pk'])
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


class ConcertCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Concert
    template_name = 'concert_create.html'
    form_class = ConcertCreateForm
    success_url = reverse_lazy('music:music_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def form_valid(self, form, **kwargs):
        concert = form.save(commit=False)
        concert.term = Term.objects.get(pk=self.kwargs['pk'])
        concert.save()
        messages.success(self.request, '本番の予定を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "本番の予定作成に失敗しました。")
        return super().form_invalid(form)


class ConcertUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Concert
    template_name = 'concert_update.html'
    form_class = ConcertCreateForm

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse_lazy('music:music_list')

    def form_valid(self, form):
        messages.success(self.request, '本番予定を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "本番予定の更新に失敗しました。")
        return super().form_invalid(form)


class ConcertDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Concert
    template_name = 'concert_delete.html'
    success_url = reverse_lazy('music:music_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "本番予定を削除しました。")
        return super().delete(request, *args, **kwargs)


class TermCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Term
    template_name = 'term_create.html'
    form_class = TermCreateForm
    success_url = reverse_lazy('music:music_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def form_valid(self, form):
        term = form.save(commit=True)
        messages.success(self.request, '練習期間を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "練習期間作成に失敗しました。")
        return super().form_invalid(form)


class TermUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Term
    template_name = 'term_update.html'
    form_class = TermCreateForm

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse_lazy('music:music_list')

    def form_valid(self, form):
        messages.success(self.request, '練習期間の情報を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "練習期間情報の更新に失敗しました。")
        return super().form_invalid(form)


class TermDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Term
    template_name = 'term_delete.html'
    success_url = reverse_lazy('music:music_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "練習期間情報を削除しました。")
        return super().delete(request, *args, **kwargs)
