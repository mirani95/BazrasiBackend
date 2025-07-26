from rest_framework_simplejwt.tokens import AccessToken


def get_token_jti(token_str):
    """ get generated jwt id (jti) for every token """

    try:
        token = AccessToken(token_str)
        return token['jti'], token['user_id']
    except Exception as e:
        return None, None
