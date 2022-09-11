import math, \
    sys

class Base:
    """
    This is a Doc

      yo
    """
    def __init__(self, a, b):
        # ‘Comment’
        self.a = a
        self.b = b
        self._a = math.pi
        self._b = '\'' + 'fake' + '\''
        self._description = f'a = {a}\nb = {b}\n'

    def __repr__(self):
        return f'''\
<section>
  <p>a + b = {self.a+self.b}</p>
</section>
'''
    @property
    def description(self):
        return self._description

    def clone(self):
        """clone"""
        me = self.__class__(self.a, self.b)
        return me


class C(Base):
    def bi(self):
        me = self.clone()
        me.a *= 2
        me.b *= 2
        return me

