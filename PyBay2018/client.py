#GRPC
import person_pb2

# Hyper
from hyper import HTTPConnection

from jwt_utils import decode_auth_token

conn = HTTPConnection(host='localhost', port=5000)
conn.request('GET', '/')
resp = conn.get_response()

if decode_auth_token(response.headers['Authorization']):

	person = person_pb2.Person()
	data = person.ParseFromString(resp.read())

	print "Person ID:", person.id
	print "Name:", person.name
	if person.HasField('email'):
		print "E-mail address:", person.email
