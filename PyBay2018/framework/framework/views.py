# GPRC
import person_pb2

from django.http import HttpResponse
from jwt_utils import encode_auth_token, decode_auth_token


def send_response(request):

    if 'HTTP_AUTHORIZATION' in request.META:
     #isinstance(decode_auth_token(request.META['HTTP_AUTHORIZATION']), int):

      print decode_auth_token(request.META['HTTP_AUTHORIZATION'])
      person = person_pb2.Person()
      person.id = 1234
      person.name = "John Doe"
      person.email = "jdoe@example.com"

      response = HttpResponse(person.SerializeToString())
      return response

    return HttpResponse('Unauthorized', status=401)
