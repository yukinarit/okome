# `okome` 🍚

*dataclass comment parser*

```python
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
```

It's known to be impossible to get comments declared for dataclass and its fields. Eric V. Smith, the author of `dataclasses` module said in https://bugs.python.org/issue38401

> To change this is beyond the scope of dataclasses, and would need to be a language change. I can't think of a good way to attach the string to the annotation before it

---

With `okome`, you can get comments from dataclass!

```python
c = okome.parse(Foo)
print(f"Class comment: {c.comment}")
for f in c.fields:
    print(f'Field "{f.name}" comment: {f.comment}')
```

![](magic.gif)

```python
$ python simple.py
Class comment: ['This is a comment for class `Foo`.']
Field "a" comment: ['This is valid comment for field that can be parsed by okome']
Field "b" comment: ['Multi line comment', 'also works!']
```