import hashlib
import hmac
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from authapp.forms import CustomUserCreationForm
from authapp.models import TelegramBotUser, User


def check_telegram_auth(auth_data, bot_token):
    auth_hash = auth_data.pop('hash')
    data_check_string = '\n'.join([f"{k}={auth_data[k]}" for k in sorted(auth_data.keys())])
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return hmac_hash == auth_hash


@csrf_exempt
def telegram_login(request):
    if request.method == 'POST':
        print(request)
        data = json.loads(request.body)
        # Validate Telegram data
        if not check_telegram_auth(data.copy(), settings.TELEGRAM_LOGIN_BOT_TOKEN):
            return JsonResponse({'error': 'Invalid Telegram data'}, status=403)
        telegram_id = data['id']
        print(data)
        username = data.get('username', '')
        first_name = data.get('first_name', '')
        user, created = User.objects.get_or_create(username=f"{username}",
                                                   telegram_id=telegram_id,
                                                   defaults={'first_name': first_name})
        login(request, user)
        return JsonResponse({'redirect_url': '/'})  # Redirect to homepage after login
    return JsonResponse({'error': 'POST required'}, status=405)


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TELEGRAM_LOGIN_BOT_USERNAME'] = settings.TELEGRAM_LOGIN_BOT_USERNAME
        return context

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
