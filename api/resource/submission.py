import kata.resource
import api.model.submission

class SubmissionsResource(kata.resource.Resource):
    def post(self, request, response):
        # require user to be logged in
        current_user = api.model.user.current_user(request)
        if current_user is None:
            return self.unauthorized()

        # create new submission
        data = self.body(request)
        submission = api.model.submission.create(current_user.id, data['title'], data.get('tag_ids'))
        return self.success({
            'submission': submission
        })

class SubmissionResource(kata.resource.Resource):
    def get(self, request, response, slug):
        submission_id = api.model.submission.SubmissionIdFromSlug(slug).get()
        if submission_id is None:
            return self.not_found()

        submission = api.model.submission.get_submission(submission_id, include_content=True)
        return self.success({
            'submission': submission
        })
