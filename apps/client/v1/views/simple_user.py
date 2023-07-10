import json

from django.http import HttpResponse
from django.views import View

from apps.client.v1.models.user import SimpleUser
from apps.client.v1.services import Services


class CreateSimpleUser(View):
    @staticmethod
    def post(request):
        data = json.loads(request.body)
        new_user = Services().create_user(user=SimpleUser(**data))
        return HttpResponse(status=201, content=json.dumps({"status": "created", "object_id": new_user.id}))
