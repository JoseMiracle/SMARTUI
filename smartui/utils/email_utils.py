from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def sign_in_with_otp_activation_mail(email,full_name, generated_otp):
     context = {
          'full_name': full_name,
          'otp': generated_otp,
     }
     html_message = render_to_string('accounts/sign_in_with_otp.html', context=context)
     plain_message = strip_tags(html_message)
     email = EmailMultiAlternatives(
        subject="OTP For Sign in",
        to=[email],
        body=plain_message,
        from_email="admin@mail.com"
    )
     email.attach_alternative(html_message, "text/html")
     email.send()
