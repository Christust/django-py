from rest_framework.authentication import TokenAuthentication
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import AuthenticationFailed


class ExpireTokenAuthentication(TokenAuthentication):
    expired = False

    def expires_in(self, token):
        time_elapse = timezone.now() - token.created
        left_time = (
            timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapse
        )
        return left_time

    def is_token_expire(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        is_expire = self.is_token_expire(token)
        if is_expire:
            self.expired = True
            user = token.user
            token.delete()
            token = self.get_model().objects.create(user=user)

        return is_expire

    def authenticate_credentials(self, key):
        user, token, message = None, None, None
        try:
            token = self.get_model().objects.select_related("user").get(key=key)
            user = token.user
        except self.get_model().DoesNotExist:
            message = "Token invalido"
            self.expired = True

        if token is not None:
            if not token.user.is_active:
                message = "Usuario no activo"

            is_expired = self.token_expire_handler(token)

            if is_expired:
                user = None
                message = "Token expirado"
                return (user, token, message, self.expired)

        return (user, token, message, self.expired)
