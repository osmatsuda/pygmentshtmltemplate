from docutils.core import publish_string
from docutils.writers import html4css1
from docutils.parsers.rst import directives
import pathlib

import unittest

from pygmentshtmltemplate.docutils import PygHtmlTmplRstDirective
directives.register_directive('my-pygmetize', PygHtmlTmplRstDirective)

ReST = f'''\
PygHtmlTmplRstDirective test
============================

using a file option

.. my-pygmetize:: python :file: {__file__}

using a code block

.. my-pygmetize:: python
   :hl_lines: 1

   """highlight this line"""
   def hello(foo):
       print(f'hello, {{foo}}!')
'''

class TestReSTDirective(unittest.TestCase):
    def test_publish(self):
        curdir = pathlib.Path(__file__).parent
        target = curdir / 'outputs/test_rst.py.html'
        outputs = publish_string(
            ReST,
            writer=html4css1.Writer(),
        )
        outputs = outputs.replace(b'</head>', b'<link rel="stylesheet" href="style.highlight.css"/>\n</head>', 1)
        with open(target, 'wb') as out:
            out.write(outputs)
