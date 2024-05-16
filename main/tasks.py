from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_email_task(subject, body, from_email, to, cc):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to,
        cc=cc,
        headers={'Reply-To': cc[0]}
    )
    email.send(fail_silently=False)
