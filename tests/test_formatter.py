import unittest
import pathlib, re
import pygments, pygments.lexers, pygments.formatters

import lxml.html as L

import pygmentshtmltemplate as PHT
import pygmentshtmltemplate.templates as TPL


def count_lines(path):
    with open(path) as f:
        n = len(f.read().rstrip().split('\n'))
    return n

def count_formatted_lines(code):
    htmlblock = L.fragment_fromstring(code)
    return len(htmlblock.xpath('li'))


class TestFormatterBasic(unittest.TestCase):
    def setUp(self):
        self.lexr = pygments.lexers.get_lexer_by_name('python')
        self.fmtr = pygments.formatters.get_formatter_by_name('fmtr_tmpl')
        self.resources = pathlib.Path(__file__).parent / 'resources'
        
    def test_linecount(self):
        with open(self.resources / 'src.py') as f:
            formatted = pygments.highlight(f.read(), self.lexr, self.fmtr)

        self.assertEqual(count_formatted_lines(formatted),
                         count_lines(self.resources / 'src.py'))
        
    def test_linecount2(self):
        with open(__file__) as f:
            formatted = pygments.highlight(f.read(), self.lexr, self.fmtr)

        self.assertEqual(count_formatted_lines(formatted),
                         count_lines(__file__))
        

class TestFormatterMember(unittest.TestCase):
    def test_get_wrap_style_rules(self):
        fmtr = pygments.formatters.get_formatter_by_name('fmtr_tmpl')
        selector_vals = {
            'wrap': 'ol',
            'line': 'li',
            'token': 'code'
        }
        wrap_cssrules = TPL.build_wrap_cssrules(selector_vals,
                                                front_base_color='#000000',
                                                linenostart=0)
        rules = []
        for sels, decl in wrap_cssrules:
            rules.append(
                ','.join(sels) + '{' + ';'.join([
                    k + ':' + v for k, v in decl.items()
                ]) + '}'
            )

    def test_get_style_defs(self):
        dest = pathlib.Path(__file__).parent / 'outputs'
        fmtr = pygments.formatters.get_formatter_by_name('fmtr_tmpl')
        with open(dest / 'style.highlight.css', 'w') as out_hi,\
             open(dest / 'style.ol.css', 'w') as out_ol:
            out_hi.write(fmtr.get_style_defs('.highlight'))
            out_ol.write(fmtr.get_style_defs())
        
        

if __name__ == '__main__':
    unittest.main()


    
