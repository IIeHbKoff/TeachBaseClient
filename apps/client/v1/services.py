import enum
import os
import redis
import requests

from typing import Union

from apps.client.v1.models.course import Course, CourseType
from apps.client.v1.models.course_session import CourseSession
from apps.client.v1.models.user import SimpleUser
from django.forms.models import model_to_dict
from system import settings


class HttpMethods(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class Services:
    def __init__(self):
        self._redis_conn = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            username=settings.REDIS_USERNAME,
            password=settings.REDIS_PASSWORD,
        )
        self._base_teachbase_api_url = 'https://go.teachbase.ru/endpoint/v1'

    def __del__(self):
        self._redis_conn.close()

    def get_user(self, *, user_id: int) -> SimpleUser:
        user = SimpleUser.objects.filter(id=user_id).first()
        if not user:
            url = f"{self._base_teachbase_api_url}/users/{user_id}"
            user_data_from_teachbase_api = self.__make_request(url=url, method=HttpMethods.GET)[0]
            user = SimpleUser()
            for key, value in user_data_from_teachbase_api.items():
                if not isinstance(value, list):
                    setattr(user, key, value)
            user.save()
        return user

    def create_user(self, *, user: SimpleUser) -> SimpleUser:
        url = f"{self._base_teachbase_api_url}/users/create"
        data = {"users": [model_to_dict(user)],
                "external_labels": True,
                "options": {
                    "activate": True,
                    "verify_emails": True,
                    "skip_notify_new_users": True,
                    "skip_notify_active_users": True
                }}
        user_data_from_teachbase_api = self.__make_request(url=url, method=HttpMethods.POST, data=data)[0]
        new_user = SimpleUser()
        for key, value in user_data_from_teachbase_api.items():
            if not isinstance(value, list):
                setattr(new_user, key, value)
        new_user.save()
        return new_user

    def delete_user(self, *, user_id: int) -> bool:
        url = f"{self._base_teachbase_api_url}/users"
        payload = {
            "users": [user_id, ]
        }
        self.__make_request(url=url, method=HttpMethods.DELETE, data=payload)
        SimpleUser.objects.filter(id=user_id).delete()
        return True

    def get_users(self) -> list[SimpleUser]:
        url = f"{self._base_teachbase_api_url}/users"
        users_from_teachbase_api = self.__make_request(url=url, method=HttpMethods.GET)
        for row in users_from_teachbase_api:
            user = SimpleUser()
            for key, value in row.items():
                if not isinstance(value, list):
                    setattr(user, key, value)
        return SimpleUser.objects.all()

    def get_courses(self) -> list[Course]:
        url = f"{self._base_teachbase_api_url}/courses"
        courses_from_teachbase_api = self.__make_request(url=url, method=HttpMethods.GET)
        for row in courses_from_teachbase_api:
            course = Course()
            for key, value in row.items():
                if not isinstance(value, list):
                    setattr(course, key, value)
            course.authors.set([SimpleUser(**authors_row) for authors_row in row["authors"]])
            course.types.set([CourseType(**types_row) for types_row in row["types"]])
            course.save()
        return Course.objects.all()

    def get_course_info(self, *, course_id: int) -> Course:
        course = Course.objects.filter(id=course_id).first()
        if not course:
            url = f"{self._base_teachbase_api_url}/courses/{course_id}"
            course = Course(**self.__make_request(url=url, method=HttpMethods.GET))
            course.save()
        return course

    def get_course_sessions(self, *, course_id: int) -> list[CourseSession]:
        url = f"{self._base_teachbase_api_url}/courses/{course_id}/course_sessions"
        sessions_from_teachbase_api = self.__make_request(url=url, method=HttpMethods.GET)
        for row in sessions_from_teachbase_api:
            session = CourseSession()
            for key, value in row.items():
                if type(value) not in (list, dict):
                    setattr(session, key, value)
            session.course = Course.objects.filter(id=course_id).first()
            session.save()
        return CourseSession.objects.filter(course__id=course_id).all()

    def register_user_to_a_course_session(self, *, session_id: int, user_id: int):
        user = self.get_user(user_id=user_id)
        url = f"{self._base_teachbase_api_url}/course_sessions{session_id}/register"
        payload = {
            "email": user.email,
            "phone": user.phone,
            "user_id": user.id,
        }
        return self.__make_request(url=url, method=HttpMethods.POST, data=payload)

    def _login(self) -> str:
        auth_server_url = 'https://go.teachbase.ru/oauth/token'
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        grant_type_payload = {'grant_type': 'client_credentials'}
        response = requests.post(auth_server_url, data=grant_type_payload, auth=(client_id, client_secret))
        if response.status_code != 200:
            raise ValueError("Wrong credentials in environment variables")
        response_data = response.json()
        self._redis_conn.set(
            name="access_token",
            value=f"{response_data['token_type']} {response_data['access_token']}",
            exat=response_data['created_at'] + response_data['expires_in']
        )
        return f"{response_data['token_type']} {response_data['access_token']}"

    def _get_access_token(self) -> str:
        access_token = self._redis_conn.get("access_token")
        if access_token is None:
            access_token = self._login()
        return access_token

    def __make_request(
            self,
            url: str,
            method: HttpMethods = HttpMethods.GET,
            *,
            data: dict = None,
            params: dict = None,
    ) -> Union[dict, list]:
        method_dict = {
            HttpMethods.GET: requests.get,
            HttpMethods.POST: requests.post,
            HttpMethods.PUT: requests.put,
            HttpMethods.PATCH: requests.patch,
            HttpMethods.DELETE: requests.delete,
            HttpMethods.HEAD: requests.head,
            HttpMethods.OPTIONS: requests.options,
        }
        headers = {"authorization": self._get_access_token()}
        response = method_dict.get(method)(url, json=data, params=params, headers=headers)
        if response.status_code in (200, 201, 204):
            return response.json()
        elif response.status_code == 400:
            raise ValueError
        elif response.status_code == 401:
            return self.__make_request(url=url, method=method, data=data, params=params)
        elif response.status_code == 500:
            raise ValueError


a = [{'id': 495682, 'name': 'New Name', 'started_at': None, 'finished_at': None, 'course_id': 55894, 'infinitely': True,
      'access_type': 'open', 'finished': False, 'navigation': 0,
      'apply_url': 'https://go.teachbase.ru/course_sessions/bazovyy-kurs-o-teachbase-06-27-19-56/apply',
      'deadline_soon': False, 'assignments_count': 61, 'deadline_type': 1,
      'slug': 'bazovyy-kurs-o-teachbase-06-27-19-56', 'period': 10,
      'course': {'id': 55894, 'name': 'Базовый курс о Teachbase', 'created_at': '2020-01-24T17:49:01.421+03:00',
                 'updated_at': '2023-05-06T16:53:07.382+03:00', 'owner_id': 157611, 'content_type': 1,
                 'owner_name': 'tets test test tets tets tets',
                 'thumb_url': 'https://static.teachbase.ru/system/courses/55894/icons/thumb/5e6b153fe9e68a8e2f9f0f70c3116123afe8ebec.jpg',
                 'cover_url': 'https://static.teachbase.ru/system/courses/55894/icons/small/ececb5b1bf44377c8b81387cb04fc6a878d259c1.jpg',
                 'description': 'Базовый курс о Teachbase - составлен специалистами нашей компании для того, что бы Вам было удобнее и нагляднее ознакомиться с функциями и возможностями платформы Teachbase.<div><br></div><div>После выполнения всего курса у Вас сформируется общее представление о платформе, а так же Вы научитесь основным приёмам в работе с ней.</div>',
                 'last_activity': '2019-07-30T12:03:16.002+03:00', 'total_score': 209, 'total_tasks': 4,
                 'is_netology': False,
                 'bg_url': 'https://static.teachbase.ru/system/courses/55894/bgs/original/72c4dce38c92727eb36914dbb4ba19bf30ebac69.jpg',
                 'video_url': '', 'demo': False, 'unchangeable': False, 'include_weekly_report': False,
                 'custom_author_names': 'Teachbase', 'custom_contents_link': '', 'hide_viewer_navigation': False,
                 'duration': None, 'account_id': 30015, 'competences': [], 'authors': [], 'types': []}, 'labels': []}]
