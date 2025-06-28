from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

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

def send_submission_notification_to_admin(case_study, request):
    """Send notification email to admin when a new case study is submitted"""
    try:
        admin_email = settings.ADMINS[0][1] if settings.ADMINS else 'admin@example.com'
        current_site = get_current_site(request)
        
        # Build admin URL for user submitted case studies
        admin_url = f"https://{current_site.domain}/63f4ul7/casestudies/usersubmittedcasestudy/{case_study.id}/change/"
        
        context = {
            'case_study': case_study,
            'admin_url': admin_url,
        }
        
        html_message = render_to_string('casestudies/email/submission_received.html', context)
        plain_message = f"""
        New Case Study Submission
        
        Title: {case_study.title}
        Author: {case_study.author}
        Email: {case_study.submitter_email}
        Domain: {case_study.domain}
        Difficulty: {case_study.difficulty}
        Submitted: {case_study.submitted_at.strftime('%B %d, %Y %I:%M %p')}
        
        Review at: {admin_url}
        """
        
        send_mail(
            subject=f'New Case Study Submission: {case_study.title}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending admin notification: {e}")
        return False

def send_approval_notification_to_user(case_study, request):
    """Send approval notification email to user"""
    try:
        current_site = get_current_site(request)
        case_study_url = f"https://{current_site.domain}{case_study.get_absolute_url()}"
        
        context = {
            'case_study': case_study,
            'case_study_url': case_study_url,
        }
        
        html_message = render_to_string('casestudies/email/submission_approved.html', context)
        plain_message = f"""
        Your Case Study Has Been Approved!
        
        Hello {case_study.author},
        
        Great news! Your case study "{case_study.title}" has been approved and is now live on our website.
        
        View your case study at: {case_study_url}
        
        Thank you for contributing to our platform!
        
        Best regards,
        The Casestudies Team
        """
        
        
        send_mail(
            subject=f'Case Study Approved: {case_study.title}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[case_study.submitter_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending approval notification: {e}")
        return False

def send_rejection_notification_to_user(case_study, request):
    """Send rejection notification email to user"""
    try:
        current_site = get_current_site(request)
        submit_url = f"https://{current_site.domain}{reverse('casestudies:submit_case_study')}"
        
        context = {
            'case_study': case_study,
            'submit_url': submit_url,
        }
        
        html_message = render_to_string('casestudies/email/submission_rejected.html', context)
        plain_message = f"""
        Case Study Submission Update
        
        Hello {case_study.author},
        
        Thank you for submitting your case study "{case_study.title}" to our platform.
        
        After careful review, we regret to inform you that we are unable to publish your case study at this time.
        
        Submit another case study at: {submit_url}
        
        Thank you for your understanding.
        
        Best regards,
        The Casestudies Team
        """
        
        
        send_mail(
            subject=f'Case Study Submission Update: {case_study.title}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[case_study.submitter_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending rejection notification: {e}")
        return False 