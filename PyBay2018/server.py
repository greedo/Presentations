# GPRC
import person_pb2

# Twisted
from twisted.web import server
from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.internet import reactor
from twisted.internet import endpoints

from jwt_utils import encode_auth_token

class Person(Resource):
    isLeaf = True

    def render_GET(self, request):

        person = person_pb2.Person()
        person.id = 1234
        person.name = "John Doe"
        person.email = "jdoe@example.com"

	request.setHeader('Authorization', encode_auth_token('my_user'))

        return person.SerializeToString()

if __name__ == "__main__":

    site = server.Site(Simple())
    server = endpoints.serverFromString(
        reactor,
        "ssl:port=5000:privateKey=key.pem:certKey=cert.pem",
    )
    server.listen(site)
    reactor.run()
