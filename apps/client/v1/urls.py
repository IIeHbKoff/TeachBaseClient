from django.urls import path

from apps.client.v1.views.cources import GetCourses
from apps.client.v1.views.course_sessions import GetCourseSessions, SignUpForASession
from apps.client.v1.views.simple_user import CreateSimpleUser

urlpatterns = [
    path("create_user/", CreateSimpleUser.as_view()),
    path("courses/", GetCourses.as_view()),
    path("courses/<course_id>/sessions/", GetCourseSessions.as_view()),
    path("sessions/<session_id>/register_user/<user_id>/", SignUpForASession.as_view()),
]
