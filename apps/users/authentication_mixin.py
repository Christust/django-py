from apps.users.authentication import ExpireTokenAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer


class Authentication(object):
    user = None
    user_token_expired = False

    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                return None
            token_expire = ExpireTokenAuthentication()
            (
                self.user,
                token,
                message,
                self.user_token_expired,
            ) = token_expire.authenticate_credentials(token)
            if self.user != None and token != None:
                return self.user
            return message
        return None

    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(request)
        if user is not None:
            if type(user) == str:
                response = Response(
                    {"error": user, "user_token_expired": self.user_token_expired},
                    status.HTTP_403_FORBIDDEN,
                )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                return response
            return super().dispatch(request, *args, **kwargs)
        response = Response(
            {
                "error": "No se envio token",
                "user_token_expired": self.user_token_expired,
            },
            status.HTTP_400_BAD_REQUEST,
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response
