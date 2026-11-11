# from service.models import Service
from .models import Company

def menu_links(request):
    links = Company.objects.all()[0]
    return dict(company_links=links)