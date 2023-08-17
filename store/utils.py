from django.db.models import Q
from .models import St


def searchSt(request):
    search_query  = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    ss = St.objects.distinct().filter(
        Q(title_icontains=search_query)
    )
    return ss, search_query