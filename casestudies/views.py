from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import CaseStudy
from django.db.models import Q

# Create your views here.

def home(request):
    latest_cases = CaseStudy.objects.all().order_by('-created_at')[:9]
    context = {'case_studies': latest_cases}
    return render(request, 'casestudies/index.html', context)

def all_case_studies(request):
    studies = CaseStudy.objects.all().order_by('-created_at')
    
    query = request.GET.get('q')
    difficulty = request.GET.get('difficulty')
    domain = request.GET.get('domain')
    tags = request.GET.get('tags')
# Pyright: this is a valid Django Q expression, safe to ignore the warning
    if query:
        studies = studies.filter(   
            Q(title__icontains=query) | 
            Q(case_background__icontains=query) |
            Q(tags__icontains=query) |
            Q(domain__icontains=query) |
            Q(author__icontains=query)
        )
    
    if difficulty:
        studies = studies.filter(difficulty=difficulty)
        
    if domain:
        studies = studies.filter(domain__iexact=domain)
        
    if tags:
        studies = studies.filter(tags__icontains=tags)

    context = {
        'case_studies': studies,
        'query': query,
        'selected_difficulty': difficulty,
        'selected_domain': domain,
        'selected_tags': tags,
    }
    return render(request, 'casestudies/cases.html', context)

def case_study_detail(request, slug):
    try:
        case_study = CaseStudy.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404("No CaseStudy matches the given query.")
    
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
        {'case_study': case_study, 'tag_color_pairs': tag_color_pairs}
    )

def about(request):
    return render(request, 'casestudies/about.html')

def send_case_study(request):
    return render(request, 'casestudies/send-case-study.html')

def terms_of_service(request):
    return render(request, 'casestudies/terms.html')

def privacy_policy(request):
    return render(request, 'casestudies/privacy.html')

def socials(request):
    return render(request, 'casestudies/socials.html')

def acknowledgements(request):
    return render(request, 'casestudies/acknowledgements.html')

def custom_404(request, exception=None):
    return render(request, 'casestudies/404.html', status=404)

