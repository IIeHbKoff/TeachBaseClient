from django.http import HttpResponse
from django.views import View
from django.core import serializers
from apps.client.v1.services import Services


class GetCourses(View):
    @staticmethod
    def get(request):
        courses_list = Services().get_courses()
        return HttpResponse(status=200, content=serializers.serialize("json", courses_list))
