import kata.resource
import api.model.user

class UsersResource(kata.resource.Resource):
    def post(self, request, response):
        data = self.body(request)
        user = api.model.user.create(data['facebook_token'])

        return self.success({
            'user': user
        })
