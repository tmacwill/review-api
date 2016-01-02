import kata.db

import api.lib
import api.model.file
import api.model.tag

class Submission(kata.db.Object):
    __table__ = 'submissions'

class SubmissionFromId(kata.db.MultiContainer):
    def expire(self):
        return api.lib.WEEK

    def key(self, item):
        return 's:%s' % item

    def pull(self, items):
        return {item: get_submission(item, include_content=False) for item in items}

class SubmissionIdFromSlug(kata.db.Container):
    def init(self, slug):
        self.slug = slug

    def expire(self):
        return api.lib.WEEK

    def key(self):
        return 'ss:%s' % self.slug

    def pull(self):
        submission = Submission.get({'slug': self.slug}, one=True)
        if submission is None:
            return None

        return submission.id

def create(user_id, title, tag_ids=None):
    submission = Submission.create({
        'user_id': user_id,
        'slug': api.lib.generate_slug(n=8),
        'title': title
    })

    if tag_ids:
        api.model.tag.add_to_submission(submission.id, tag_ids)

    return submission

def get_submission(submission_id, include_content=False):
    submission = Submission.get({'id': submission_id}, one=True)
    if submission is None:
        return None

    submission.files = api.model.file.get_for_submission(submission_id, include_content=include_content)
    submission.comments = api.model.comment.get_for_submission(submission_id, include_content=include_content)
    submission.tags = api.model.tag.get_for_submission(submission_id)
    return submission

def submission_updated(submission_id):
    SubmissionFromId().dirty(submission_id)
