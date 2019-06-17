import re
from dataclasses import dataclass, field
from typing import List, Optional, Any

from dte.__init__ import DTERoot, NO_VALUE, PatternedString


def empty_list():
    return field(default_factory=list)


@dataclass
class Element(DTERoot):
    # hasValue() or (children().count() > id.count())
    id: Optional["string"] = None
    extension: List["Extension"] = empty_list()
    value: Any = NO_VALUE

    def _is_instance(v: Any) -> bool:
        return True



@dataclass
class string(Element):
    class S(PatternedString):
        pattern = re.compile(r'[ \r\n\t\S]+')
    value: Optional[S] = NO_VALUE


x = string(value='abcd')
x = string(value=[8])
