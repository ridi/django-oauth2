from django.http import HttpResponse


class HttpUnauthorizedResponse(HttpResponse):
    status_code = 401
