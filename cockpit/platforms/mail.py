from django.core.mail import send_mail
from django.conf import settings

def email(username="abc",gmail="abc@gmail.com"):
    subject="hello from Cockpit"
    message="hi {} ".format(username)
    print("{}".format(gmail))
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[gmail]
    send_mail(
        subject,
        message,
       from_email,
       recipient_list)