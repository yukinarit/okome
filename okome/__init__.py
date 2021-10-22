import ast
import dataclasses
import inspect
import logging
from typing import Iterator, List, Optional

log = logging.getLogger("okome")


@dataclasses.dataclass
class Field:
    """
    Dataclass field information extracted from source code.
    """

    name: str
    """ Name of dataclass field """

    comment: Optional[List[str]] = None
    """ Comment lines of dataclass field """


def fields(cls) -> Iterator[Field]:
    """"""
    c = parse(cls)
    yield from c.fields


@dataclasses.dataclass
class Class:
    """
    Class information extracted from source code.
    """

    name: str
    """ Name of class """

    comment: Optional[List[str]] = None
    """ Comment lines of class """

    fields: List[Field] = dataclasses.field(default_factory=list)


def parse(cls) -> Class:
    """
    Parses class and fields information from class object.
    """
    source = inspect.getsource(cls)
    log.debug(source)
    node = ast.parse(source, mode="exec")
    class_def = node.body[0]
    assert isinstance(class_def, ast.ClassDef)
    class_name = class_def.name
    log.debug(f"class_name = {class_name}")
    class_comment = _parse_class_comment(class_def)
    log.debug(f"class_comment = {class_comment}")

    c = Class(class_name, class_comment)
    c.fields = _parse_fields(class_def)
    return c


def _parse_class_comment(class_def: ast.ClassDef) -> Optional[List[str]]:
    """
    Parses docstring comment of a class from AST.
    """
    class_comment = None

    if class_def.body:
        mem = class_def.body[0]
        if isinstance(mem, ast.Expr) and isinstance(mem.value, ast.Constant):
            class_comment = []
            for line in mem.value.value.strip().split("\n"):
                class_comment.append(line)

    return class_comment


def _parse_fields(class_def: ast.ClassDef) -> List[Field]:
    fields = []

    for i, mem in enumerate(class_def.body):
        if isinstance(mem, ast.AnnAssign) and isinstance(mem.target, ast.Name):
            f = Field(mem.target.id)
            log.debug(f"Parsed {f}")
            if (
                i + 1 < len(class_def.body)
                and isinstance(class_def.body[i + 1], ast.Expr)
                and isinstance(class_def.body[i + 1].value, ast.Constant)
            ):
                lines: List[str] = []
                for line in class_def.body[i + 1].value.value.strip().split("\n"):
                    lines.append(line.strip())
                f.comment = lines
            fields.append(f)

    return fields
