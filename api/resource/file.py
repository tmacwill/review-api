import kata.resource
import api.model.file
import api.model.submission

class FilesResource(kata.resource.Resource):
    def post(self, request, response, submission_id):
        # require user to be logged in
        current_user = api.model.user.current_user(request)
        if current_user is None:
            return self.unauthorized()

        # get the submission being uploaded to
        submission = api.model.submission.SubmissionFromId().get(submission_id)
        if submission is None:
            return self.not_found()

        # only the submission owner can upload files
        if submission.user_id != current_user.id:
            return self.unauthorized()

        # add file to the submission
        data = self.body(request)
        file = api.model.file.add_to_submission(submission_id, data['files'])
        return self.success()
