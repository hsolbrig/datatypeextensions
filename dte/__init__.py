import re
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Type, Union

# Strictness setting for the entire module
from dte.bool_container import BOOL

GLOBAL_STRICT = BOOL(True)


def strict() -> bool:
    """ Switch to global strict mode """
    rval = GLOBAL_STRICT.v
    GLOBAL_STRICT.v = True
    return rval


def lax() -> bool:
    """ Switch to global lax mode """
    rval = GLOBAL_STRICT.v
    GLOBAL_STRICT.v = False
    return rval


NO_VALUE = object()


class DTERootMeta(ABCMeta):
    # def __new__(cls, *args, **kwargs):
    #     return super().__new__(*args, **kwargs)

    def __instancecheck__(self, instance) -> bool:
        return self._is_instance(instance)


class DTERoot(metaclass=DTERootMeta):
    _strict = GLOBAL_STRICT

    def __init__(self, v: Optional[Any] = NO_VALUE) -> None:
        if v is NO_VALUE:
            raise ValueError(f"{self._n}: Missing required field")
        if bool(self._strict) and not self._is_valid(v):
            raise ValueError(str(type(self).__name__) + ': ' + self._error_str(v))

    @staticmethod
    @abstractmethod
    def _is_instance(v: Any) -> bool:
        return True

    def _error_str(self, v: Any) -> Optional[str]:
        return f'"{v}" is not a valid {self._n()}'

    def _is_valid(self, v: Optional[Any] = NO_VALUE) -> bool:
        if v is NO_VALUE:
            v = self
        return self._is_instance(v)

    def _n(self) -> str:
        """ Return our type name """
        return type(self).__name__


# =======================
# Sample implementations
# =======================
class PositiveInteger(int, DTERoot):

    @staticmethod
    def _is_instance(v: Any) -> bool:
        try:
            return int(v) > 0
        except :
            return False

    def _error_str(self, v: Any) -> Optional[str]:
        try:
            if int(v) <= 0:
                return "Value must be positive"
            return None
        except Exception as e:
            return str(e)


class PatternedString(str, DTERoot):
    pattern = re.compile('.*$')

    @classmethod
    def _is_instance(cls, v: Any) -> bool:
        return bool(cls.pattern.match(v))

@dataclass
class SpecialString(PatternedString):
    pattern = re.compile(r'[a-zA-Z][a-z]+$')
    id: Optional[Identifier]



def test(f: Type, v: Any) -> Optional[object]:
    try:
        x = f(v)
    except Exception as e:
        print(f"    ****> {str(e)}")
        return NO_VALUE
    print(f"{f.__name__}({v}) = {x} (Valid: {x._is_valid()})")



print(f"{'*' * 20} Strict {'*' * 20}")

test( PositiveInteger, 17)
test( PositiveInteger, -1)
test( PositiveInteger, 'a')
test( PositiveInteger, None)

test(SpecialString, 'Abcd')
test(SpecialString, 'A1')
test(SpecialString, None)

lax()
print(f"\n{'*' * 20} Lax {'*' * 20}")
test( PositiveInteger, 17)
test( PositiveInteger, -1)
test( PositiveInteger, 'a')
test( PositiveInteger, None)

v1 = test(SpecialString, 'Abcd')
v2 = test(SpecialString, 'A1')
v3 = test(SpecialString, None)
