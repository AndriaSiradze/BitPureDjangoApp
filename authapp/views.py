import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import NotTelegramDataError, TelegramDataIsOutdatedError
from django_telegram_login.widgets.generator import create_callback_login_widget

from authapp.forms import CustomUserCreationForm

from django.utils.translation import gettext as _

from authapp.models import User, TelegramBotUser


@csrf_exempt
def telegram_auth_callback(request):
    print('telegram_auth_callback')
    if request.method == 'POST':
    # 1) Получаем данные — либо из GET, либо из JSON-тела
        data = request.GET.dict() if 'hash' in request.GET else json.loads(request.body)

    # 2) Проверяем подпись и актуальность данных
    try:
        user_info = verify_telegram_authentication(
            bot_token   = settings.TELEGRAM_LOGIN_BOT_TOKEN,
            request_data= data
        )
    except TelegramDataIsOutdatedError:
        return HttpResponseBadRequest('Telegram data is older than 24 hours')
    except NotTelegramDataError:
        return HttpResponseBadRequest('Invalid Telegram authentication data')

    # 3) Создаём или получаем вашего пользователя
    user, _ = User.objects.get_or_create(
        telegram_id = user_info['id'],
        defaults    = {
            'username'  : f"tg_{user_info['id']}",
            'first_name': user_info.get('first_name', ''),
            'last_name' : user_info.get('last_name', ''),
            'email'     : user_info.get('username','') + '@telegram',  # если нужно
        }
    )

    # 4) Логиним в Django
    login(request, user)

    # 5) Отвечаем клиенту
    if request.method == 'GET':
        # если это redirect-виджет — можно редиректить
        return redirect('authapp:login_success')
    else:
        # для AJAX-callback — просто JSON
        return JsonResponse({'ok': True})

class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    redirect_authenticated_user = True

    # def get_context_data(self, **ctx):
    #     ctx = super().get_context_data(**ctx)
    #     ctx['telegram_login_widget'] = create_callback_login_widget(
    #         bot_name     = settings.TELEGRAM_LOGIN_BOT_USERNAME,
    #         size         = 'small',
    #         user_photo   = True
    #     )
    #     return ctx

    def form_valid(self, form):
        response = super().form_valid(form)
        message = _("Login success!<br>Hi, %(username)s") % {
            "username": self.request.user.get_full_name() or self.request.user.get_username()
        }
        messages.info(self.request, mark_safe(message))
        return response

    def get_success_url(self):
        return reverse_lazy('blogapp:index')

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))




class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('authapp:login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, _("See you later!"))
        return super().dispatch(request, *args, **kwargs)


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('blogapp:index')

    def form_valid(self, form):
        user = form.save()
        response = super().form_valid(form)
        TelegramBotUser(

        )
        messages.success(self.request, 'Аккаунт успешно создан! Пожалуйста, войдите.')
        return response
