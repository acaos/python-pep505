# Python PEP505

- GitHub: <https://github.com/acaos/python-pep505>
- PyPI: <https://pypi.org/project/pep505/>

This package polyfills [PEP 505](https://www.python.org/dev/peps/pep-0505/)'s
None-aware operators to Python 3.8 through 3.10.

Later versions of Python are expected to be supported, but the grammar (in
this package) will first need to be updated before doing so. Python versions
earlier than 3.8 will not be supported.

## Usage

After this package has been installed, it is activated by placing the
following at the top of any module you wish to use null-coalescing
operators in:

```python
# -*- parsing: pep505 -*-
```

Note that this will not work for code executed directly from the command
line (e.g. `python3 foo.py`), but will work if you execute the code as
a module (e.g. `python3 -m foo`).


## Technical Information

### Null-Coalescing Operators

This package adds the four null-coalescing operators from PEP 505. See
that PEP for a fuller treatment of the operators; the below are merely
simple examples.


#### Coalesce Operator (`??`)

The coalesce binary operator `??` has a higher precedence than any
other binary operator, but a lower precedence than an `await` expression.

The coalesce operator works as follows: `A ?? B` is the equivalent of:

```python
(X if (X := A) is not None else B)
```

`A` is evaluated only once; `B` is not evaluated if `A` is not `None`.


#### Maybe-Assign (`??=`)

The maybe-assign operator `??=` is a special form of augmented assignment,
which will assign to the left-hand side only if it is `None`.

The maybe-assign operator works as follows: `A ??= B` is the equivalent
of:

```python
if A is None:
    A = B
```

`B` is not evaluated if `A` is not `None`.


#### Maybe-Dot (`?.`)

The maybe-dot operator `?.` prevents `AttributeError` from occuring if
the object for which an attribute is being accessed is `None`; instead,
the expression evaluates to `None`.

The maybe-dot operator works as follows: `A?.B` is the equivalent of:

```python
(X.B if (X := A) is not None else None)
```

`A` is evaluated only once.


#### Maybe-Subscript (`?[`)

The maybe-subscript operator `?[` prevents `TypeError` from occuring if
the object for which an item is being accessed is `None`; instead,
the expression evaluates to `None`.

The maybe-subscript operator works as follows: `A?[B]` is the equivalent of:

```python
(X[B] if (X := A) is not None else None)
```

`A` is evaluated only once; `B` is not evaluated if `A` is not `None`.


### How the PEP505 Package Works

This package works by registering an import hook and taking over the
AST parsing of Python modules, using a modified version of the Python
tokenizer and AST.

The four operators above are transformed into an AST compatible with
any version of Python 3.8 or later. The modified grammar can be found
in `src/grammar/python_pep505.gram`, and compiled with the normal:

```sh
python3 -m pegen src/grammar/python_pep505.gram -o src/pep505/parser.py
```

Note that `parser.py` is then further modified slightly to use the local
version of the `pegen` package (replacing `pegen.` imports with `.pegen.`).

#### Temporary Variables

In order to function, this module generates temporary variable names
of the form `__coalesce_<lineno>_<column-offset>`. These are unlikely
to conflict with any existing variables, but be aware of their existence.

#### Modifying the Wheel / Installing from Source

Note that after using `python3 -m build` to build the wheel, it is necessary
to manually add the `pep505.pth` file to the wheel, with (for example):

```sh
cd src
zip -g ../dist/pep505-*-py3-none-any.whl pep505.pth
cd ..
```

If installing from source, the `src/pep505.pth` file must be placed in your
`site-packages` directory.

#### Running the Tests

The tests can be run with `python3 -m pep505.test`.


## Thanks and Credits

This package stands on the shoulders of giants.

PEP 505 was authored by Mark E. Haase and Steve Dower.

The `.pegen.parser` and `.pegen.tokenizer` modules are from
[pegen](https://github.com/we-like-parsers/pegen) by Guido van Rossum,
Pablo Galindo, and Lysandros Nikolaou. They are included here solely
to prevent this package from pulling in pegen's Flask and other
dependencies.

In addition, the Python parser in this package is built using pegen.

The `pep505.hook.activate()` function is based on André Roberge's
[ideas](https://github.com/aroberge/ideas) package.

