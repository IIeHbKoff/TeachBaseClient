import enum
import json
import os
import redis
import requests

from typing import Union

from apps.client.v1.models.course import Course
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
        url = f"{self._base_teachbase_api_url}/users/{user_id}"
        return SimpleUser(**self.__make_request(url=url, method=HttpMethods.GET))

    def create_user(self, *, user: SimpleUser) -> int:
        url = f"{self._base_teachbase_api_url}/users/create"
        new_user = self.__make_request(url=url, method=HttpMethods.POST, data=model_to_dict(user))
        return new_user.get("id")

    def delete_user(self, *, user_id: int) -> bool:
        url = f"{self._base_teachbase_api_url}/users"
        payload = {
            "users": [user_id, ]
        }
        self.__make_request(url=url, method=HttpMethods.DELETE, data=payload)
        return True

    def get_users(self) -> list[SimpleUser]:
        url = f"{self._base_teachbase_api_url}/users"
        return [SimpleUser(**row) for row in self.__make_request(url=url, method=HttpMethods.GET)]

    def get_courses(self) -> list[Course]:
        url = f"{self._base_teachbase_api_url}/courses"
        return [Course(**row) for row in self.__make_request(url=url, method=HttpMethods.GET)]

    def get_course_info(self, *, course_id: int) -> Course:
        url = f"{self._base_teachbase_api_url}/courses/{course_id}"
        return Course(**self.__make_request(url=url, method=HttpMethods.GET))

    def get_course_sessions(self, *, course_id: int) -> list[CourseSession]:
        url = f"{self._base_teachbase_api_url}/courses/{course_id}/course_sessions"
        return [CourseSession(**row) for row in self.__make_request(url=url, method=HttpMethods.GET)]

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
        # access_token = redis_conn.get("access_token")
        # if access_token is None:
        #     access_token = login()
        return json.loads(self._redis_conn.get("access_token")) or self._login()

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
        response = method_dict.get(method)(url, data=data, params=params, headers=headers)
        if response.status_code in (200, 201, 204):
            return response.json()
        elif response.status_code == 400:
            raise ValueError
        elif response.status_code == 401:
            return self.__make_request(url=url, method=method, data=data, params=params)
        elif response.status_code == 500:
            raise ValueError
