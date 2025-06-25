from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import CaseStudy
from django.db.models import Q

# Create your views here.

def home(request):
    latest_cases = CaseStudy.objects.all().order_by('-created_at')[:9]
    context = {'case_studies': latest_cases, 'query': None}
    return render(request, 'casestudies/index.html', context)

def all_case_studies(request):
    studies = CaseStudy.objects.all()
    
    query = request.GET.get('q')
    difficulty = request.GET.get('difficulty')
    domain = request.GET.get('domain')
    tags = request.GET.get('tags')
    sort_by = request.GET.get('sort', '-created_at')  # Default to latest first
    
    # Apply search filter
    if query:
        studies = studies.filter(   
            Q(title__icontains=query) | 
            Q(case_background__icontains=query) |
            Q(tags__icontains=query) |
            Q(domain__icontains=query) |
            Q(author__icontains=query)
        )
    
    # Apply filters
    if difficulty:
        studies = studies.filter(difficulty=difficulty)
        
    if domain:
        studies = studies.filter(domain__iexact=domain)
        
    if tags:
        studies = studies.filter(tags__icontains=tags)

    # Apply sorting
    if sort_by == 'created_at':
        studies = studies.order_by('created_at')  # Oldest first
    elif sort_by == '-created_at':
        studies = studies.order_by('-created_at')  # Latest first
    elif sort_by == 'title':
        studies = studies.order_by('title')  # A-Z
    elif sort_by == '-title':
        studies = studies.order_by('-title')  # Z-A
    else:
        studies = studies.order_by('-created_at')  # Default to latest first

    # Get available filter options
    available_domains = CaseStudy.objects.values_list('domain', flat=True).distinct().exclude(domain='').order_by('domain')
    available_difficulties = CaseStudy.DIFFICULTY_CHOICES

    context = {
        'case_studies': studies,
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
    try:
        case_study = CaseStudy.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404("No CaseStudy matches the given query.")
    
    # Get similar case studies based on domain (excluding current case study)
    similar_case_studies = CaseStudy.objects.filter(
        domain=case_study.domain
    ).exclude(
        id=case_study.id
    ).order_by('-created_at')[:3]  # Limit to 3 similar case studies
    
    tags_list = []
    if case_study.tags:
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
            'query': None
        }
    )

def about(request):
    return render(request, 'casestudies/about.html', {'query': None})

def send_case_study(request):
    return render(request, 'casestudies/send-case-study.html', {'query': None})

def terms_of_service(request):
    return render(request, 'casestudies/terms.html', {'query': None})

def privacy_policy(request):
    return render(request, 'casestudies/privacy.html', {'query': None})

def socials(request):
    return render(request, 'casestudies/socials.html', {'query': None})

def acknowledgements(request):
    return render(request, 'casestudies/acknowledgements.html', {'query': None})

def custom_404(request, exception=None):
    return render(request, 'casestudies/404.html', {'query': None}, status=404)

