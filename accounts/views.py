import logging
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserUpdateForm
from .models import CustomUser


logger = logging.getLogger(__name__)


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetailView(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    model = CustomUser
    template_name = 'user_detail.html'


class UserUpdateView(OnlyYouMixin, generic.UpdateView):
    model = CustomUser
    template_name = 'user_update.html'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse_lazy('accounts:user_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'ユーザー情報を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'ユーザー情報の更新に失敗しました。')
        return super().form_invalid(form)
