import dataclasses

import okome


@dataclasses.dataclass
class Foo:
    """
    This is a comment for class `Foo`.
    """

    a: int
    """ This is valid comment for field that can be parsed by okome """
    b: str
    """
    Multi line comment
    also works!
    """


print(okome.parse(Foo))
