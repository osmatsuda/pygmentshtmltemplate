import unittest
import pathlib, re
import pygments, pygments.lexers, pygments.formatters

import pygmentshtmltemplate as PHT


def count_lines(path):
    with open(path) as f:
        n = len(f.read().rstrip().split('\n'))
    return n

def count_formatted_lines(code):
    mi = ma = 0
    for m in re.finditer(r'data=(\d+)', code):
        ma = int(m.group(1))
    return ma - mi + 1


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
        

if __name__ == '__main__':
    unittest.main()


    
