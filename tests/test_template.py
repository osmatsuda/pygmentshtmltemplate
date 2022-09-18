import unittest
import pathlib, re
import pygments, pygments.lexers, pygments.formatters
import pygments.token as TKN
from pygments.formatters.html import _get_ttype_class

import pygmentshtmltemplate as PHT
from pygmentshtmltemplate.templates import from_src

class TestTemplateBasic(unittest.TestCase):
    def setUp(self):
        self.resources = pathlib.Path(__file__).parent / 'resources'
        self.template = from_src(str(self.resources / 'test_template.xml'))
        
    def test_basic(self):
        self.assertEqual(self.template.__class__.__name__, 'Template')

    def test_template_context(self):
        context = self.template.context
        self.assertEqual(context.lead_parts, '<h1>${title}</h1>\n<ol class="${cssclass}">\n')
        self.assertEqual(context.trail_parts, '</ol>\n<p>${filename}</p>\n')

        lines = [
            ['<li id="line-${lineno}" class="hll">', '</li>'],
            ['<li id="line-${lineno}">', '</li>'],
        ]
        line_test_keys = [
            ['highlighted', 'lineno'],
            ['lineno'],
        ]
        tokens = [
            ['<code class="${token_class} init">', '</code>'],
            ['<code class="${token_class}" title="${token_type}">', '</code>'],
        ]
        token_test_keys = [
            ['token_class'],
            ['token_class', 'token_type'],
        ]
        self.assertEqual(len(context.lines), 2)
        self.assertEqual(len(context.tokens), 2)
        
        for i in range(2):
            line = context.lines[i]
            self.assertEqual(line.lead_parts, lines[i][0], f'i={i}')
            self.assertEqual(line.trail_parts, lines[i][1], f'i={i}')
            self.assertEqual(line.test_keys, line_test_keys[i], f'i={i}')

            token = context.tokens[i]
            self.assertEqual(token.lead_parts, tokens[i][0], f'i={i}')
            self.assertEqual(token.trail_parts, tokens[i][1], f'i={i}')
            self.assertEqual(token.test_keys, token_test_keys[i], f'i={i}')

    def test_template_select_line(self):
        lines_data = [{'hl_lines': [1,3,5]},
                      {'hl_lines': [1,3,5]},
                      {}]
        linenos = [6, 5, 0]
        lead_results = ['<li id="line-${lineno}">',
                        '<li id="line-${lineno}" class="hll">',
                        '<li id="line-${lineno}">']
        for i in range(3):
            data = PHT._update_options_with_lineno(linenos[i], lines_data[i])
            lead, trail = self.template.select_line_parts(data)
            self.assertEqual(lead, lead_results[i], f'i={i}')
            self.assertEqual(trail, '</li>')

    def test_template_select_token(self):
        lines_data = [{'hl_lines': [1,3,5]},
                      {'hl_lines': [1,3,5]},
                      {},
                      {}]
        linenos = [6, 5, 0, 1]
        tokens = [(TKN.Comment.Single, '# __init__'),
                  (TKN.Name.Function.Magic, '__init__'),
                  (TKN.Name.Function.Magic, '__repr__'),
                  (TKN.Text, 'yo')]
        lead_results = ['<code class="${token_class}" title="${token_type}">',
                        '<code class="${token_class} init">',
                        '<code class="${token_class}" title="${token_type}">',
                        '']
        for i in range(4):
            tprops = {'token_class': _get_ttype_class(tokens[i][0]),
                      'token_type': '.'.join(tokens[i][0])}
            data = PHT._update_options_with_lineno(linenos[i], lines_data[i]) | tprops
            lead, trail = self.template.select_token_parts(*tokens[i], data)
            self.assertEqual(lead, lead_results[i], f'i={i}')
            if i < 3:
                self.assertEqual(trail, '</code>')
            else:
                self.assertEqual(trail, '')

    def test_template_render_token(self):
        lines_data = [{'hl_lines': [1,3,5]},
                      {'hl_lines': [1,3,5]},
                      {},
                      {}]
        linenos = [6, 5, 0, 1]
        tokens = [(TKN.Comment.Single, '# __init__'),
                  (TKN.Name.Function.Magic, '__init__'),
                  (TKN.Name.Function.Magic, '__repr__'),
                  (TKN.Text, 'yo')]
        results = ['<code class="c1" title="Comment.Single"># __init__</code>',
                   '<code class="fm init">__init__</code>',
                   '<code class="fm" title="Name.Function.Magic">__repr__</code>',
                   'yo']
        for i in range(4):
            tprops = {'token_class': _get_ttype_class(tokens[i][0]),
                      'token_type': '.'.join(tokens[i][0])}
            data = PHT._update_options_with_lineno(linenos[i], lines_data[i]) | tprops
            result = self.template.render_token(*tokens[i], data)
            self.assertEqual(result, results[i], f'i={i}')


class TestTemplateDefault(unittest.TestCase):
    def setUp(self):
        self.template = from_src('')

    def test_template_context(self):
        context = self.template.context
        self.assertEqual(context.lead_parts, '<ol class="${cssclass}">\n')
        self.assertEqual(context.trail_parts, '</ol>\n')

        lines = [
            ['<li class="hll">', '</li>'],
            ['<li>', '</li>'],
        ]
        tokens = [
            ['<code class="${token_class}">', '</code>'],
        ]
        self.assertEqual(len(context.lines), 2)
        self.assertEqual(len(context.tokens), 1)
        
        for i in range(2):
            self.assertEqual(context.lines[i].lead_parts, lines[i][0], f'i={i}')
            self.assertEqual(context.lines[i].trail_parts, lines[i][1], f'i={i}')
        
        self.assertEqual(context.tokens[0].lead_parts, tokens[0][0])


if __name__ == '__main__':
    unittest.main()
