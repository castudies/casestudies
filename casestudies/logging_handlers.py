import logging
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.views.debug import ExceptionReporter
import traceback

class CustomAdminEmailHandler(logging.Handler):
    def emit(self, record):
        try:
            request = getattr(record, 'request', None)
            subject = self.format_subject(record)
            message, additional_info = self.format_message(record, request)
            # Add file, line, function, logger name
            extra_details = f"""
                <b>Logger:</b> {record.name}<br>
                <b>Level:</b> {record.levelname}<br>
                <b>File:</b> {record.pathname}<br>
                <b>Line:</b> {record.lineno}<br>
                <b>Function:</b> {record.funcName}<br>
            """
            if additional_info:
                extra_details += f"<br><b>Traceback:</b><br>{additional_info}"
            context = {
                'subject': subject,
                'message': message,
                'additional_info': extra_details,
                'timestamp': timezone.now(),
            }
            html_message = render_to_string('casestudies/email/issue_update.html', context)
            admin_email = settings.ADMINS[0][1] if settings.ADMINS else settings.EMAIL_HOST_USER
            email = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=settings.SERVER_EMAIL,
                to=[admin_email],
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)
        except Exception:
            self.handleError(record)

    def format_subject(self, record):
        return f"[Django Error] {record.levelname}: {record.getMessage()[:60]}"

    def format_message(self, record, request):
        if request and record.exc_info:
            exc_type, exc_value, tb = record.exc_info
            reporter = ExceptionReporter(exc_type, exc_value, tb, request, is_email=True)
            html = reporter.get_traceback_html()
            return record.getMessage(), html
        elif record.exc_info:
            # If no request, but exc_info is present, format the traceback
            tb_html = '<pre>' + ''.join(traceback.format_exception(*record.exc_info)) + '</pre>'
            return record.getMessage(), tb_html
        else:
            return record.getMessage(), getattr(record, 'stack_info', '') or '' 