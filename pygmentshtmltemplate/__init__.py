from pygments.formatters import HtmlFormatter, html
from pygments.token import Token
from collections.abc import Generator
import re

from . import templates

__version__ = "0.0.1c"


_options_pass_to_HtmlFormatter = (
    'style', 'full', 'title', 'encoding', 'outencoding',
    'linenostart', 'hl_lines',
)

class FormatterWithTemplate(HtmlFormatter):
    name = 'FormatterWithTemplate'
    aliases = ['fmtr_tmpl']

    def __init__(self, **options) -> None:
        xopts = {}
        for k in options:
            if k in _options_pass_to_HtmlFormatter:
                xopts[k] = options[k]
        HtmlFormatter.__init__(self, **xopts)

        self._line_counter = 0
        return
        tmp_src = options.get('template')
        if not tmp_src:
            raise
        self.template = templates.from_path(tmp_src)

    def format_token(self, ttype, part) -> str:
        if ttype in Token.Text and re.fullmatch(r'[ \t]*', part):
            return part
        return f'{ttype}({part})'
            
    def format_lines(self, tokensource) -> Generator[str, None, None]:
        line = ''
        for ttype, value in tokensource:
            if ttype in Token.Text and value == '\n':
                if re.fullmatch(r'[ \t]*', line):
                    yield ''
                else:
                    yield line
                line = ''
            elif '\n' in value:
                parts = value.split('\n')
                for i in range(len(parts) -1):
                    part = parts[i]
                    if i == 0:
                        if part:
                            yield line + self.format_token(ttype, part)
                        else:
                            yield line
                    else:
                        if part:
                            yield self.format_token(ttype, part)
                        else:
                            yield ''
                line = self.format_token(ttype, parts[i+1])
            else:
                line += self.format_token(ttype, value)
        if line:
            yield line

    def format_unencoded(self, tokensource, outfile) -> None:
        outfile.write('<h1>start</h1>\n<ol>\n')

        self.line_counter = 0
        empties: list[str] = []
        for line in self.format_lines(tokensource):
            if line:
                if empties:
                    while empties:
                        empty, empties = empties[0], empties[1:]
                        outfile.write(empty)
                outfile.write(f'<li data={self.line_counter}>{line}</li>\n')
            else:
                empties.append(f'<li data={self.line_counter}></li>\n')

        outfile.write('</ol>\n')

    @property
    def line_counter(self) -> int:
        self._line_counter += 1
        return self._line_counter - 1

    @line_counter.setter
    def line_counter(self, v: int) -> None:
        self._line_counter = v
    


def debug(tokensource, outfile):
    outfile.write(f'{__version__}\n')
    for ttype, value in tokensource:
        title = '.'.join(ttype)
        outfile.write(f'<span class="{html._get_ttype_class(ttype)}" title="{title}" data="{ttype}">')
        outfile.write(html.escape_html(value))
        outfile.write(f'</span>')
