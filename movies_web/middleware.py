from movies_web.models import VisitorsCount
from django.middleware.common import MiddlewareMixin
from django.core.exceptions import ObjectDoesNotExist


class CounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            f = VisitorsCount.objects.get(id=1)
            f.count += 1
            f.save()
        except ObjectDoesNotExist:
            VisitorsCount.objects.create(id=1, count=1)
