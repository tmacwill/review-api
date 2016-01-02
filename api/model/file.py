import kata.db
import pygments
import pygments.formatters
import pygments.lexers

import api.lib
import api.model.submission

class _TableHTMLFormatter(pygments.formatters.HtmlFormatter):
    def wrap(self, source, outfile):
        # wrap the entire output in a single table
        yield 0, '<table class="file-contents-table">'
        yield 0, '<tbody>'
        yield 0, '<tr class="first-row"><td class="line-number padding">&nbsp;</td><td class="code padding">&nbsp;</td></tr>'

        # each line of source code is a row in the table, with the line numbers in one cell and the code in another
        line_number = 1
        for i, t in source:
            line = '<tr>'
            line += '<td class="line-number" data-line="%s"><a href="#">%s</a></td>' % (line_number, line_number)
            line += '<td class="code" data-line="%s">%s</td>' % (line_number, t)
            line += '</tr>'
            yield i, line

            line_number += 1

        yield 0, '</tbody>'
        yield 0, '</table>'

class File(kata.db.Object):
    __table__ = 'files'

class SubmissionIdForFile(kata.db.Container):
    def init(self, id):
        self.id = id

    def key(self):
        return 'f:%s' % self.id

    def pull(self):
        file = File.get({'id': self.id}, one=True)
        if file is None:
            return None

        return file.submission_id

def add_to_submission(submission_id, files):
    # add submission ID to each file
    for file in files:
        file['submission_id'] = submission_id

    # save files and dirty submission
    result = File.create(files)
    api.model.submission.submission_updated(submission_id)
    return result

def get_for_submission(submission_id, include_content=False):
    fields = ['id', 'title']
    if include_content:
        fields.append('content')

    files = File.get({'submission_id': submission_id}, fields=fields)
    if include_content:
        for file in files:
            file.content = highlight(file.title, file.content)

    return files

def highlight(filename, text):
    lexer = pygments.lexers.guess_lexer_for_filename(filename, text)
    formatter = _TableHTMLFormatter()
    return '<style>' + formatter.get_style_defs() + '</style>' + pygments.highlight(text, lexer, formatter)
