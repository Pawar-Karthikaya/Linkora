# chat/middleware.py
from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token):
    try:
        # ✅ Use SimpleJWT's own decoder instead of raw jwt.decode
        validated_token = AccessToken(token)
        user_id         = validated_token["user_id"]
        return User.objects.get(id=user_id)
    except (InvalidToken, TokenError) as e:
        print(f"❌ Token error: {e}")
        return AnonymousUser()
    except User.DoesNotExist:
        print(f"❌ User not found for token")
        return AnonymousUser()
    except Exception as e:
        print(f"❌ Middleware error: {e}")
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        params       = parse_qs(query_string)
        token_list   = params.get("token", [None])
        token        = token_list[0] if token_list else None

        if token:
            scope["user"] = await get_user_from_token(token)
            print(f"🔑 Token user: {scope['user']}")
        else:
            scope["user"] = AnonymousUser()
            print("⚠️ No token provided")

        return await super().__call__(scope, receive, send)