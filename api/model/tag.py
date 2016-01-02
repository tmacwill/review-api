import kata.db

import api.model.submission

class SubmissionTag(kata.db.Object):
    __table__ = 'submissions_tags'

class Tag(kata.db.Object):
    __table__ = 'tags'

class AllTags(kata.db.Container):
    def cache(self):
        return kata.cache.l0

    def expire(self):
        return None

    def key(self):
        return 'at'

    def pull(self):
        rows = kata.db.query('select * from ' + Tag.__table__)
        return [Tag(**row) for row in rows]

class Tags(kata.db.MultiContainer):
    def key(self, item):
        return 't:%s' % item

    def source(self):
        return Tag, 'id'

class SubmissionIdsWithTags(kata.db.MultiContainer):
    def key(self, item):
        return 't:s:%s' % item

    def pull(self, items):
        submission_tags = SubmissionTag.get_in('tag_id', items)
        result = {}
        for t in submission_tags:
            result.setdefault(t.tag_id, [])
            result[t.tag_id].append(t.submission_id)

        return result

def add_to_submission(submission_id, tag_ids):
    values = ','.join([
        '(%s,%s)' % (str(submission_id), str(tag_id))
        for tag_id in tag_ids
    ])

    sql = '''
        INSERT INTO %s
            (submission_id, tag_id)
        VALUES %s
    ''' % (SubmissionTag.__table__, values)
    kata.db.execute(sql)

def get_for_submission(submission_id):
    tag_ids = [e.tag_id for e in SubmissionTag.get({'submission_id': submission_id})]
    return Tags().get(tag_ids)

def get_submissions_with_tags_and(tag_ids):
    tags = SubmissionIdsWithTags().get(tag_ids)
    result = set()
    for tag in tags.values():
        result &= set(tag)

    return api.model.submission.SubmissionFromId().get(result)

def get_submissions_with_tags_or(tag_ids):
    tags = SubmissionIdsWithTags().get(tag_ids)
    result = set()
    for tag in tags.values():
        result |= set(tag)

    return api.model.submission.SubmissionFromId().get(result)

def get_with_query(query, limit=10):
    tags = AllTags().get()
    query = query.lower()
    return [tag for tag in tags if query in tag.name.lower()][:limit]
