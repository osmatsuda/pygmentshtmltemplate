import unittest
import pathlib
import pygments.lexers, pygments.formatters


class TestBasic(unittest.TestCase):
    def setUp(self):
        self.lexr = pygments.lexers.get_lexer_by_name('python')
        src_path = pathlib.Path(__file__).parent / 'resources/src.py'
        with open(src_path) as src:
            self.code = src.read()
        
    def test_setup(self):
        self.assertEqual(self.lexr.name, 'Python')
        self.assertEqual(self.code[0:10], 'import mat')
        formatter = pygments.formatters.get_formatter_by_name('fmtr_tmpl')
        self.assertEqual(formatter.__class__.__name__, 'FormatterWithTemplate')
        

if __name__ == '__main__':
    unittest.main()
