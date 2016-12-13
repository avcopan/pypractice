class B(object):

  def __init__(self, string = 'thing'):
    self.string = string

  def __str__(self):
    return self.string


class A(object):

  def __init__(self, string, lobject = None):
    self.string = string
    self.lobject = lobject

  def __mul__(self, other):
    if isinstance(other, B):
      product = B('({:s} * {:s})'.format(self, other))
      return product if self.lobject is None else self.lobject.__mul__(product)
    elif isinstance(other, A):
      lobject = self if other.lobject is None else self.__mul__(other.lobject)
      return A(str(other), lobject)

#  def __rmul__(self, other):
#    if not isinstance(other, A):
#      raise Exception("Cannot left-multiply A object with {:s}".format(type(other).__name__))
#    if self.lobject is None:
#      return A(str(self), lobject = other)
#    else:
#      return A(str(self), lobject = self.lobject.__rmul__(other))

  def __str__(self):
    return self.string

if __name__ == "__main__":
  thing = B()
  a = A('a')
  b = A('b')
  c = A('c')
  d = A('d')
  print((c * ((d * b) * a)) * thing)
