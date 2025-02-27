from smtplib import SMTPException

from celery import shared_task
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response

from config import settings
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_reset_password_email(email, reset_link):
    try:

        send_mail(
            "Сброс пароля",
            f"Перейдите по ссылке для сброса пароля:"
            f" {reset_link}. Если Вы не запрашивали сброс пароля "
            f"проигнорируйте данное сообщение.",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        print("Письмо отправлено")
    except SMTPException as e:
        logger.error(f"Ошибка при отправке письма: {str(e)}")
        return {"error": f"Ошибка при отправке письма: {str(e)}"}
    except ValueError:
        logger.error("Некорректный email или данные для отправки.")
        return {"error": "Некорректный email или данные для отправки."}
        # return Response(
        #     {"error": f"Ошибка при отправке письма: {str(e)}"},
        #     status=status.HTTP_500_INTERNAL_SERVER_ERROR
        # )
    # except ValueError:
    #     return Response(
    #         {"error": "Некорректный email или данные для отправки."},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )
