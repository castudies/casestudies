from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import CaseStudy, UserSubmittedCaseStudy, Notification, UploadLog
from django.db.models import Q
from .forms import CaseStudySubmissionForm
from django.contrib import messages
from .utils import send_submission_notification_to_admin
from itertools import chain
from operator import attrgetter
import logging
from django.core.cache import cache
from django.utils import timezone

# Create your views here.

def home(request):
    admin_cases = CaseStudy.objects.all()
    user_cases = UserSubmittedCaseStudy.objects.filter(is_approved=True)  # type: ignore
    all_cases = list(chain(admin_cases, user_cases))
    def get_date(obj):
        return getattr(obj, 'created_at', None) or getattr(obj, 'submitted_at', None)
    latest_cases = sorted(all_cases, key=get_date, reverse=True)[:9]  # type: ignore
    notification = Notification.objects.filter(is_active=True).first()  # type: ignore
    context = {'case_studies': latest_cases, 'query': None, 'notification': notification}
    return render(request, 'casestudies/index.html', context)

def all_case_studies(request):
    print("GET domain param:", repr(request.GET.get('domain')))
    # Get all admin case studies
    admin_cases = CaseStudy.objects.all()
    # Get all approved user-submitted case studies
    user_cases = UserSubmittedCaseStudy.objects.filter(is_approved=True)  # type: ignore
    
    # Filtering
    query = request.GET.get('q')
    difficulty = request.GET.get('difficulty')
    domain = request.GET.get('domain')
    tags = request.GET.get('tags')
    sort_by = request.GET.get('sort', '-created_at')  # Default to latest first
    
    # Apply search filter
    if query:
        admin_cases = admin_cases.filter(
            Q(title__icontains=query) |
            Q(case_background__icontains=query) |
            Q(tags__icontains=query) |
            Q(domain__icontains=query) |
            Q(author__icontains=query)
        )
        user_cases = user_cases.filter(
            Q(title__icontains=query) | 
            Q(case_background__icontains=query) |
            Q(tags__icontains=query) |
            Q(domain__icontains=query) |
            Q(author__icontains=query)
        )
    
    # Apply filters
    if difficulty:
        admin_cases = admin_cases.filter(difficulty=difficulty)
        user_cases = user_cases.filter(difficulty__iexact=difficulty)
    if domain:
        admin_cases = admin_cases.filter(domain__iexact=domain)
        user_cases = user_cases.filter(domain__iexact=domain)
    if tags:
        admin_cases = admin_cases.filter(tags__icontains=tags)
        user_cases = user_cases.filter(tags__icontains=tags)

    # Combine and sort
    all_cases = list(chain(admin_cases, user_cases))
    # Use created_at for admin, submitted_at for user
    def get_date(obj):
        return getattr(obj, 'created_at', None) or getattr(obj, 'submitted_at', None)
    if sort_by == 'created_at':
        all_cases = sorted(all_cases, key=get_date)  # type: ignore
    elif sort_by == '-created_at':
        all_cases = sorted(all_cases, key=get_date, reverse=True)  # type: ignore
    elif sort_by == 'title':
        all_cases = sorted(all_cases, key=lambda x: x.title)  # type: ignore
    elif sort_by == '-title':
        all_cases = sorted(all_cases, key=lambda x: x.title, reverse=True)  # type: ignore
    else:
        all_cases = sorted(all_cases, key=get_date, reverse=True)  # type: ignore

    # Get available filter options (from admin cases only for now)
    available_domains = CaseStudy.objects.values_list('domain', flat=True).distinct().exclude(domain='').order_by('domain')
    available_difficulties = CaseStudy.DIFFICULTY_CHOICES

    context = {
        'case_studies': all_cases,
        'query': query,
        'selected_difficulty': difficulty,
        'selected_domain': domain,
        'selected_tags': tags,
        'selected_sort': sort_by,
        'available_domains': available_domains,
        'available_difficulties': available_difficulties,
    }
    return render(request, 'casestudies/cases.html', context)

def case_study_detail(request, slug):
    # Try to get from admin case studies first
    try:
        case_study = CaseStudy.objects.get(slug=slug)
        case_type = 'admin'
    except Exception:
        # Try to get from approved user-submitted case studies
        try:
            case_study = UserSubmittedCaseStudy.objects.get(slug=slug, is_approved=True)  # type: ignore
            case_type = 'user'
        except Exception:
            raise Http404("No CaseStudy matches the given query.")
    
    # Get similar case studies based on domain (excluding current case study)
    admin_cases = CaseStudy.objects.filter(domain=case_study.domain).exclude(slug=case_study.slug)
    user_cases = UserSubmittedCaseStudy.objects.filter(domain=case_study.domain, is_approved=True).exclude(slug=case_study.slug)  # type: ignore
    similar_case_studies = sorted(
        chain(admin_cases, user_cases),
        key=lambda x: getattr(x, 'created_at', None) or getattr(x, 'submitted_at', None),
        reverse=True
    )[:3]  # type: ignore
    
    tags_list = []
    if hasattr(case_study, 'tags') and case_study.tags:
        tags_list = [tag.strip() for tag in case_study.tags.split(',') if tag.strip()]
    tag_colors = [
        "bg-pink-100", "bg-blue-100", "bg-yellow-100", "bg-green-100",
        "bg-purple-100", "bg-red-100", "bg-indigo-100"
    ]
    tag_color_pairs = [
        (tag, tag_colors[i % len(tag_colors)]) for i, tag in enumerate(tags_list)
    ]
    return render(
        request,
        'casestudies/detail.html',
        {
            'case_study': case_study, 
            'tag_color_pairs': tag_color_pairs, 
            'similar_case_studies': similar_case_studies,
            'query': None,
            'case_type': case_type,
        }
    )

def about(request):
    return render(request, 'casestudies/about.html', {'query': None})

def submission_guideline(request):
    return render(request, 'casestudies/submission_guideline.html', {'query': None})

def terms_of_service(request):
    return render(request, 'casestudies/terms.html', {'query': None})

def privacy_policy(request):
    return render(request, 'casestudies/privacy.html', {'query': None})

def socials(request):
    return render(request, 'casestudies/socials.html', {'query': None})

def acknowledgements(request):
    return render(request, 'casestudies/acknowledgements.html', {'query': None})

def support(request):
    return render(request, 'casestudies/support.html', {'query': None})

def custom_404(request, exception=None):
    return render(request, 'casestudies/404.html', {'query': None}, status=404)

def submit_case_study(request):
    logger = logging.getLogger('casestudies.uploads')
    ip = request.META.get('REMOTE_ADDR')
    RATE_LIMIT = 3
    RATE_PERIOD = 60 * 60  # 1 hour in seconds
    cache_key = f"case_submit_{ip}"
    now = timezone.now()
    # Rate limiting logic
    attempts = cache.get(cache_key, [])
    # Remove attempts older than 1 hour
    attempts = [t for t in attempts if (now - t).total_seconds() < RATE_PERIOD]
    if request.method == 'POST':
        if len(attempts) >= RATE_LIMIT:
            messages.error(request, "You have reached the submission limit. Please try again later.")
            form = CaseStudySubmissionForm(request.POST, request.FILES)
            return render(request, 'casestudies/submit_case_study.html', {'form': form, 'query': None})
        form = CaseStudySubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            case = form.save(commit=False)
            case.is_approved = None  # Mark as pending
            case.save()
            # Log the upload event
            user_email = form.cleaned_data.get('submitter_email', 'unknown')
            dataset = form.cleaned_data.get('dataset')
            thumbnail = form.cleaned_data.get('thumbnail')
            logger.info(
                f"Case study submitted: email={user_email}, ip={ip}, "
                f"dataset={getattr(dataset, 'name', None)}, thumbnail={getattr(thumbnail, 'name', None)}"
            )
            # Log to database for admin audit
            UploadLog.objects.create(
                ip=ip,
                email=user_email,
                dataset=getattr(dataset, 'name', None),
                thumbnail=getattr(thumbnail, 'name', None)
            )
            # Update rate limit cache
            attempts.append(now)
            cache.set(cache_key, attempts, timeout=RATE_PERIOD)
            # Send email notification to admin
            send_submission_notification_to_admin(case, request)
            request.session['allow_submission_success'] = True  # Set flag for success page access
            return redirect('casestudies:submission_success')
    else:
        form = CaseStudySubmissionForm()
    return render(request, 'casestudies/submit_case_study.html', {'form': form, 'query': None})

def submission_success(request):
    if not request.session.get('allow_submission_success'):
        return render(request, 'casestudies/404.html', {'query': None}, status=404)
    # Clear the flag so it can't be reused
    request.session.pop('allow_submission_success', None)
    return render(request, 'casestudies/submission_success.html', {'query': None})