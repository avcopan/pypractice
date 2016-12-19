from abc import abstractmethod
from contracts import contract, ContractsMeta, with_metaclass

class ClassAttributeContractNotRespected(Exception):

  def __init__(self, message):
    Exception.__init__(self, message)

class AttributeContractMeta(ContractsMeta):

  def __call__(cls, *args, **kwargs):
    instance = ContractsMeta.__call__(cls, *args, **kwargs)
    instance._check_common_attributes()
    return instance

def check_common_attributes(instance, attribute_dictionary):
  """Check whether an instance has a given set of attributes.

  Args:
    instance (object): An instance of a class.
    attribute_dictionary (dict): A list of attribute names (keys, type `str`)
      and along with their desired type (values, type `type`).

  Raises:
    ClassAttributeNotRespected: Raised when `instance` is either missing an
      attribute or has initialized it with the wrong type.
  """
  for attr, attr_type in attribute_dictionary.items():
    if not (hasattr(instance, attr) and
            isinstance(getattr(instance, attr), attr_type)):
      raise ClassAttributeContractNotRespected(
              "Attribute '{:s}' must be initialized with type '{:s}'."
              .format(attr, attr_type.__name__))


class AbstractBase(with_metaclass(AttributeContractMeta, object)):
  _common_attributes = {
    'this': str,
    'that': int
  }

  def _check_common_attributes(self):
    check_common_attributes(self, AbstractBase._common_attributes)



if __name__ == "__main__":
  import numpy as np

  class SubClass1(AbstractBase):

    def __init__(self, this, that):
      self.this = this
      self.that = that

  instance1a = SubClass1('a', 1)
# instance1b = SubClass1(1, 'a') # breaks
