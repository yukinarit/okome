import ast
from dataclasses import dataclass

import okome


@dataclass
class Foo:
    """
    Class comment.
    """

    a: int
    """ This is valid comment for field that can be parsed by okome """
    b: float  # This comment won't be parsed.
    c: bool
    # This comment won't be parsed as well.
    d: str = "foo"
    """
    Multi line comment
    also works!
    """


def test_fields():

    print(
        ast.dump(
            ast.parse(
                '''
@dataclass
class Opt:
    """
    Class comment.
    """
    a: int
    """ This is valid comment that can be parsed by okome """
    b: float   # This comment won't be parsed.
    c: bool = False
    # This comment won't be parsed as well.
    d: str
    """
    Multi line comment
    is valid!
    """
''',
                mode="exec",
            ),
            indent=4,
        )
    )

    c = okome.parse(Foo)
    assert c.name == "Foo"
    assert c.comment == ["Class comment."]

    assert c.fields[0].name == "a"
    assert c.fields[0].comment == ["This is valid comment for field that can be parsed by okome"]
    assert c.fields[1].name == "b"
    assert c.fields[1].comment is None
    assert c.fields[2].name == "c"
    assert c.fields[2].comment is None
    assert c.fields[3].name == "d"
    assert c.fields[3].comment == ["Multi line comment", "also works!"]
