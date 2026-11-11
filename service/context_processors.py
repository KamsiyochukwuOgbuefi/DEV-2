from .models import Service
from company.models import Company

def menu_links(request):
    company = Company.objects.all()[0]
    links =  Service.objects.filter(company=company)
    return dict(service_links=links)
