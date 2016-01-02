import kata.resource
import api.model.comment

class CommentsResource(kata.resource.Resource):
    def post(self, request, response, file_id):
        # require user to be logged in
        current_user = api.model.user.current_user(request)
        if current_user is None:
            return self.unauthorized()

        # add comment to file
        data = self.body(request)
        comment = api.model.comment.add_to_file(
            user_id=current_user.id,
            file_id=file_id,
            start_line=data['start_line'],
            end_line=data['end_line'],
            content=data['content']
        )

        return self.success({
            'id': comment.id
        })
