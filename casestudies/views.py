from django.shortcuts import render, get_object_or_404
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

    if query:
        studies = studies.filter(
            Q(title__icontains=query) | 
            Q(case_background__icontains=query)
        )
    
    if difficulty:
        studies = studies.filter(difficulty=difficulty)
        
    if domain:
        studies = studies.filter(domain__iexact=domain)

    context = {
        'case_studies': studies,
        'query': query,
        'selected_difficulty': difficulty,
        'selected_domain': domain,
    }
    return render(request, 'casestudies/cases.html', context)

def case_study_detail(request, slug):
    case_study = get_object_or_404(CaseStudy, slug=slug)
    return render(request, 'casestudies/detail.html', {'case_study': case_study})

def about(request):
    return render(request, 'casestudies/about.html')

def terms_of_service(request):
    return render(request, 'casestudies/terms.html')

def privacy_policy(request):
    return render(request, 'casestudies/privacy.html')

def socials(request):
    return render(request, 'casestudies/socials.html')

def acknowledgements(request):
    return render(request, 'casestudies/acknowledgements.html')
