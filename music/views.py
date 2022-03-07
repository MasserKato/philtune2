import logging
from django.urls import reverse_lazy
from django.views import generic
from .forms import MusicCreateForm, StageCreateForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Music, Stage
from schedule.views import paginate_queryset
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now

logger = logging.getLogger(__name__)



@login_required
def music_index(request):
    user_id = request.user.id
    sql = f'SELECT * FROM music LEFT JOIN (SELECT * FROM music_stage WHERE user_id={user_id}) AS stage_table ON music.id=stage_table.music_id;'
    music = Music.objects.raw(sql)
    page_obj = paginate_queryset(request, music, 5)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'music_list.html', context)


class MusicListView(LoginRequiredMixin, generic.ListView):
    model = Music
    template_name = 'music_list.html'
    paginate_by = 2

    def get_queryset(self):
        musics = Music.objects.order_by('-created_at')
        return musics


class MusicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Music
    template_name = 'music_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_list = Stage.objects.filter(music=self.kwargs['pk'], user=self.request.user).first()
        context['stage'] = data_list
        return context


class MusicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Music
    template_name = 'music_create.html'
    form_class = MusicCreateForm
    success_url = reverse_lazy('music:music_list')

    def form_valid(self, form):
        music = form.save(commit=False)
        music.user = self.request.user
        music.save()
        messages.success(self.request, '曲を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "曲の作成に失敗しました。")
        return super().form_invalid(form)


class MusicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Music
    template_name = 'music_update.html'
    form_class = MusicCreateForm

    def get_success_url(self):
        return reverse_lazy('music:music_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '練習予定を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "曲の更新に失敗しました。")
        return super().form_invalid(form)


class MusicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Music
    template_name = 'Music_delete.html'
    success_url = reverse_lazy('music:music_list')

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
