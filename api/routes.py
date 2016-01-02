import kata.router

import api.resource.comment
import api.resource.file
import api.resource.submission
import api.resource.tag
import api.resource.user

# users
kata.router.add_route('/users', api.resource.user.UsersResource)

# submissions
kata.router.add_route('/submissions', api.resource.submission.SubmissionsResource)
kata.router.add_route('/submissions/slug/{slug}', api.resource.submission.SubmissionResource)

# files
kata.router.add_route('/submissions/{submission_id}/files', api.resource.file.FilesResource)

# comments
kata.router.add_route('/comments/{file_id}', api.resource.comment.CommentsResource)

# tags
kata.router.add_route('/tags/{query}', api.resource.tag.TagsResource)
