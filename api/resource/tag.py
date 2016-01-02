import kata.resource

import api.model.tag

class TagsResource(kata.resource.Resource):
    def get(self, request, response, query):
        return self.success({
            'tags': api.model.tag.get_with_query(query)
        })
