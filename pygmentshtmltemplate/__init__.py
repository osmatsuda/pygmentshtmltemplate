from pygments.formatter import Formatter

__version__ = "0.0.1"

class MyFormatter(Formatter):
    name = 'MyFormatter'
    aliases = ['myformatter']

    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            outfile.write(f'<!--/*{ttype}-->'.encode())
            outfile.write(value.encode())
            outfile.write(f'<!--{ttype}*/-->'.encode())
