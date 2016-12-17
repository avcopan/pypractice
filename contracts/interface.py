from abc import abstractmethod
from contracts import contract, ContractsMeta, with_metaclass

class ClassAttributeContractNotRespected(Exception):

  def __init__(self, message):
    Exception.__init__(self, message)

class AbstractBase(with_metaclass(ContractsMeta, object)):
  _common_attributes = {
    'this': str,
    'that': int
  }
  def __init__(self):
    """
    Make sure the common attributes of IntegralsBase have been defined.
    """
    for attr, attr_type in AbstractBase._common_attributes.items():
      if not (hasattr(self, attr) and
              isinstance(getattr(self, attr), attr_type)):
        raise ClassAttributeContractNotRespected(
                "Attribute '{:s}' must be initialized with type '{:s}'."
                .format(attr, attr_type.__name__))

  @abstractmethod
  @contract(returns='array[NxN](float64), N>10')
  def get_square_array(self):
    """
    Compute overlap integrals for this molecule and basis set.

    < mu(1) | nu(1) >
    """
    pass


if __name__ == "__main__":
  import numpy as np

  class SubClass0(AbstractBase):

    def __init__(self, this, that):
      self.this = this
      AbstractBase.__init__(self)

    def get_square_array(self):
      return np.zeros((15, 15))

  class SubClass1(AbstractBase):

    def __init__(self, this, that):
      self.this = this
      self.that = that
      AbstractBase.__init__(self)

    def get_square_array(self):
      return np.zeros((15, 15))

  class SubClass2(AbstractBase):

    def __init__(self, this, that):
      self.this = this
      self.that = that
      AbstractBase.__init__(self)

    def get_square_array(self):
      return np.zeros((9, 9))

  class SubClass3(AbstractBase):

    def __init__(self, this, that):
      self.this = this
      self.that = that
      AbstractBase.__init__(self)

    def get_square_array(self):
      return np.zeros((15, 14))

  instance0  = SubClass0('a', 1)

  instance1a = SubClass1('a', 1)
  instance1a.get_square_array()
# instance1b = SubClass1(1, 'b') # this breaks

  instance2 = SubClass2('a', 1)
# instance2.get_square_array() # this breaks

  instance3 = SubClass3('a', 1)
# instance3.get_square_array() # this breaks
