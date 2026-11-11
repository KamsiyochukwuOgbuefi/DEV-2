from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect
from company.models import Company, CompanyOverview
from service.models import Service, ServiceProcess
from staff.models import Staff
# from blog.models import Article, Author, Paragraph
from enquiry.forms import EnquiryForm, NewsletterForm
from project.models import Project, ProjectImages, Partner, Testimonial
from industry.models import Industry, IndustryProcess


RESOURCES = (
    {
        'slug': 'security-operations',
        'filename': 'Tareon RealWear Security Brochure v.2.pdf',
        'title': 'Connected worker solutions for security operations',
        'category': 'Tareon briefing',
        'summary': 'See how voice-controlled RealWear headsets bring a supervisor into the field with live video, hands-free incident capture and hazardous-area capability.',
    },
    {
        'slug': 'future-of-work',
        'filename': 'ABIResearch_WhitePaper_FutureofWork.pdf',
        'title': 'The future of work for the frontline',
        'category': 'Research white paper',
        'summary': 'A look at connected frontline work, digital twins and the technologies reshaping industrial operations.',
    },
    {
        'slug': 'manufacturing-xr',
        'filename': 'CPG Manufacturers Leverage XR for Improved Efficiency, Training and Safety on the Frontline.pdf',
        'title': 'XR for manufacturing efficiency, training and safety',
        'category': 'Manufacturing white paper',
        'summary': 'How wearable technology helps CPG manufacturers connect people and machines while improving frontline performance.',
    },
    {
        'slug': 'pharmaceutical',
        'filename': 'Pharmaceutical Whitepaper Final.pdf',
        'title': 'Accelerating pharmaceutical breakthroughs',
        'category': 'Life sciences white paper',
        'summary': 'Explore assisted reality technology for faster, more connected pharmaceutical development and production.',
    },
    {
        'slug': 'healthcare',
        'filename': 'RealWear_Guide_to_Wearables_for_Healthcare_eBook.pdf',
        'title': 'Transforming healthcare with hands-free smart glasses',
        'category': 'Healthcare guide',
        'summary': 'Practical insight into extended reality and wearables that support better care, expertise and collaboration.',
    },
    {
        'slug': 'oil-and-gas',
        'filename': 'Realwear_Whitepaper_Oil_and_Gas_final.pdf',
        'title': 'XR technologies for oil and gas',
        'category': 'Energy white paper',
        'summary': 'Learn how intrinsically safe assisted reality supports inspection, asset management and safer operations.',
    },
    {
        'slug': 'security-flyer',
        'filename': 'Tareon-Security-Operations-Flier.pdf',
        'title': 'Security operations at a glance',
        'category': 'Tareon flyer',
        'summary': 'A concise introduction to Tareon’s connected-worker security proposition.',
    },
)


def resources(request):
    return render(request, 'resources/library.html', {'title': 'Insights & Resources', 'resources': RESOURCES})


def resource_file(request, slug):
    resource = next((item for item in RESOURCES if item['slug'] == slug), None)
    if not resource:
        raise Http404('Resource not found')

    path = Path(settings.BASE_DIR) / 'tapdf' / resource['filename']
    if not path.is_file():
        raise Http404('Resource file not found')

    response = FileResponse(path.open('rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment' if request.GET.get('download') == '1' else 'inline'
    response['Content-Disposition'] += '; filename="{}"'.format(path.name)
    return response


def home(request):
    title = "Home"
    company = Company.objects.get(id=1, is_client=False)
    company_overview = CompanyOverview.objects.get(company=company)
    services = Service.objects.filter(company=company)
    staffs = Staff.objects.filter(company=company)[:3]
    # projects = Project.objects.filter(company=company)[:3]
    partners = Partner.objects.filter(company=company)
    testimonials = Testimonial.objects.filter(company=company)
    industries = Industry.objects.filter(company=company)
    display_desc = {}
    for industry in industries:
        display_desc[industry.id] = ' '.join(industry.description.split(' ')[:10]) + '...'
        break

    # articles = Article.objects.all().order_by('-id')[:3]
    # display_paragraph = {}
    # for article in articles:
    #     for paragraph in Paragraph.objects.filter(article=article):
    #         display_paragraph[article.id] = ' '.join(paragraph.paragraph_content.split(' ')[:18]) + '...'
    #         break

    enquiry_form = EnquiryForm()
    newsletter_form = NewsletterForm()


    context = {
        'title': title,
        'company': company,
        'company_overview': company_overview,
        'services': services,
        'staffs': staffs,
        # 'articles': articles,
        # 'display_paragraph': display_paragraph,
        'enquiry_form': enquiry_form,
        'newsletter_form': newsletter_form,
        # 'projects': projects,
        'partners': partners,
        'testimonials': testimonials,
        'industries': industries,
        'display_desc': display_desc,
    }
    return render(request, 'home.html', context)

