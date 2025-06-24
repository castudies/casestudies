from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

def send_issue_update(subject, message, additional_info=None):
    """
    Send a simple issue update email using the single template.
    """
    context = {
        'subject': subject,
        'message': message,
        'additional_info': additional_info,
        'timestamp': timezone.now(),
    }
    html_message = render_to_string('casestudies/email/issue_update.html', context)
    admin_email = settings.ADMINS[0][1] if settings.ADMINS else settings.EMAIL_HOST_USER
    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[admin_email],
    )
    email.content_subtype = "html"
    return email.send(fail_silently=False) 