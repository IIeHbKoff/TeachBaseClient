import json

from django.http import HttpResponse
from django.views import View
from django.core import serializers

from apps.client.v1.services import Services


class GetCourseSessions(View):
    @staticmethod
    def get(request, course_id: int):
        sessions = Services().get_course_sessions(course_id=course_id)
        return HttpResponse(status=200, content=serializers.serialize('json', sessions))


class SignUpForASession(View):
    @staticmethod
    def get(request, user_id: int, session_id: int):
        Services().register_user_to_a_course_session(session_id=session_id, user_id=user_id)
        return HttpResponse(status=200, content=json.dumps({"status": "success"}))
