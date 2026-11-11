from .models import Industry
from company.models import Company

def menu_links(request):
    company = Company.objects.all()[0]
    links =  Industry.objects.filter(company=company)
    return dict(industry_links=links)
