from service.models import Service
from .models import Article

def menu_links(request):
    links =  Article.objects.filter().order_by('-id')[:2]
    return dict(articles_links=links)
