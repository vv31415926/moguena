from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from sitemoguena import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser( LoginView ):
    #form_class = AuthenticationForm
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def form_valid(self, form):
        # Вызываем родительский метод form_valid для выполнения стандартного поведения авторизации
        response = super().form_valid(form)
        user_id = self.request.user.id
        print(f"User ID: {user_id}")  # Вывод в консоль или логирование id

        return response

def logout_user( request ):
    logout( request )
    return HttpResponseRedirect( reverse('users:login') )

class RegisterUser( CreateView ):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title':"Регистрация"}
    success_url = reverse_lazy('users:login')  # URL по умолчанию

    def form_valid(self, form):
        # Получаем значение поля `kod`
        kod = form.cleaned_data.get('mykod')

        # Проверка `kod`
        if kod == "31415926":  # замените на проверочный код или более сложную проверку
            # Создание пользователя без сохранения
            user = form.save(commit=False)
            user.kod = kod
            user.save()

            # Автоматический вход пользователя после регистрации
            #login(self.request, user)
            return super().form_valid(form)
        else:
            # Добавление ошибки, если `kod` неверный
            form.add_error('mykod', "Неверный код приглашения.")
            return self.form_invalid(form)

class ProfileUser( LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': "Профиль пользователя",
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    # отбор записи для редактирования - текущий пользователь
    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange( PasswordChangeView ):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
