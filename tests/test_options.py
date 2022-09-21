import unittest, pathlib
import pygments
import lxml.html as L

class TestFormatterOptions(unittest.TestCase):
    def setUp(self):
        self.get_formatter_by_name = pygments.formatters.get_formatter_by_name
        
        self.curdir = pathlib.Path(__file__).parent
        self.tmpl = self.curdir / 'resources/test_template.xml'
        self.lexer = pygments.lexers.get_lexer_by_name('python')
        with open(self.curdir / 'resources/src.py') as src:
            self.source = src.read()

    def test_title_and_filename(self):
        title = 'hello'
        filename = 'hello.py'
        frmtr = self.get_formatter_by_name(
            'fmtr_tmpl',
            template=str(self.tmpl),
            title=title,
            filename=filename,
        )
        formatted = pygments.highlight(self.source, self.lexer, frmtr)
        h1, ol, p = L.fragments_fromstring(formatted)

        self.assertEqual(h1.text, title)
        self.assertEqual(p.text, filename)

    def test_cssclass(self):
        frmtr = self.get_formatter_by_name('fmtr_tmpl')
        formatterd = pygments.highlight(self.source, self.lexer, frmtr)
        ol = L.fragment_fromstring(formatterd)

        self.assertEqual(ol.get('class'), 'highlight')

        cssclass = 'code-hilight'
        frmtr = self.get_formatter_by_name('fmtr_tmpl', cssclass=cssclass)
        formatterd = pygments.highlight(self.source, self.lexer, frmtr)
        ol = L.fragment_fromstring(formatterd)

        self.assertEqual(ol.get('class'), cssclass)

    def test_linehighlight(self):
        hl_lines = '1 7 14 21'
        frmtr = self.get_formatter_by_name(
            'fmtr_tmpl',
            template=str(self.tmpl),
            hl_lines=hl_lines,
        )
        formatted = pygments.highlight(self.source, self.lexer, frmtr)
        _, ol, _ = L.fragments_fromstring(formatted)
        self.assertEqual(ol[0].get('id'), 'line-1')
        self.assertEqual([li.get('id') for li in ol.xpath('li[@class="hll"]')],
                         ['line-'+n for n in hl_lines.split()])
        
    def test_linehighlight_default(self):
        hl_lines = '1'
        frmtr = self.get_formatter_by_name(
            'fmtr_tmpl',
            hl_lines=hl_lines,
        )
        formatted = pygments.highlight(self.source, self.lexer, frmtr)
        ol = L.fragment_fromstring(formatted)

        self.assertEqual(ol[0].get('class'), 'hll')

        

