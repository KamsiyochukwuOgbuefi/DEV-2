from service.models import Service
from company.models import Company
from project.models import Project

def menu_links(request):
    company = Company.objects.all()[0]
    service_ids = Project.objects.order_by('service').values_list('service', flat=True).distinct('service')
    links =  Service.objects.filter(company=company, id__in=service_ids)
    return dict(project_links=links)