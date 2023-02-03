import requests
from django.conf import settings


def validate_recaptcha_token(token: str | None) -> tuple[bool, float]:
    """
    Validate the reCaptcha response token on form submit
    :param token: (str) response token from post
    :return: success: (bool) validation result, score: (float) client score
    """
    try:
        # Send a post request to google recaptcha api to validate
        # https://developers.google.com/recaptcha/docs/verify
        data = {"secret": settings.RECAPTCHA_PRIVATE_KEY, "response": token}
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify", data=data
        )
        response_json: dict = response.json()
        return response_json.get("success", False), response_json.get("score", 0.0)
    except requests.exceptions.RequestException:
        return False, 0.0
