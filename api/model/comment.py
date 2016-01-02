import kata.db

import api.model.file

class Comment(kata.db.Object):
    __table__ = 'comments'

def add_to_file(user_id, file_id, start_line, end_line, content):
    # create new comment
    comment = Comment.create({
        'user_id': user_id,
        'file_id': file_id,
        'start_line': start_line,
        'end_line': end_line,
        'content': content
    })

    # get the submission that corresponds to this file so we can dirty it
    submission_id = api.model.file.SubmissionIdForFile(file_id).get()
    if submission_id is None:
        return None

    api.model.submission.submission_updated(submission_id)
    return comment

def get_for_submission(submission_id, include_content=False):
    fields = ['id', 'file_id', 'user_id', 'start_line', 'end_line']
    if include_content:
        fields.append('content')

    files = api.model.file.get_for_submission(submission_id, include_content=False)
    file_ids = [e.id for e in files]
    return Comment.get_in('file_id', file_ids, fields=fields)
