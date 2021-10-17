#!/usr/bin/env python3

def import_tokenize():
    import importlib
    import importlib.util
    import token

    token.COALESCE = token.N_TOKENS + 1
    token.COALESCEEQUAL = token.N_TOKENS + 2
    token.COALESCEDOT = token.N_TOKENS + 3
    token.COALESCELSQB = token.N_TOKENS + 4
    token.EXACT_TOKEN_TYPES['??'] = token.COALESCE
    token.EXACT_TOKEN_TYPES['??='] = token.COALESCEEQUAL
    token.EXACT_TOKEN_TYPES['?.'] = token.COALESCEDOT
    token.EXACT_TOKEN_TYPES['?['] = token.COALESCELSQB

    tokenize_path_spec = importlib.util.find_spec('tokenize')
    tokenize_spec = importlib.util.spec_from_loader('tokenize', loader=None)
    tokenize = importlib.util.module_from_spec(tokenize_spec)

    with open(tokenize_path_spec.origin) as tokenize_file:
        tokenize_content = tokenize_file.read()
        tokenize_content = tokenize_content.replace("""if initial in '([{':""", """if initial in '([{' or token == '?[':""")

        exec(tokenize_content, tokenize.__dict__)

    del token.COALESCE
    del token.COALESCEEQUAL
    del token.COALESCEDOT
    del token.COALESCELSQB
    del token.EXACT_TOKEN_TYPES['??']
    del token.EXACT_TOKEN_TYPES['??=']
    del token.EXACT_TOKEN_TYPES['?.']
    del token.EXACT_TOKEN_TYPES['?[']

    return tokenize

tokenize = import_tokenize()


import warnings

import parsinghook

from . import parser as python_parser


def parse_module(f, filename, **kwargs):
    tokengen = tokenize.generate_tokens(f.readline)
    tokenizer = python_parser.Tokenizer(tokengen)
    parser = python_parser.PythonParser(tokenizer)
    tree = parser.start()

    return tree


def activate():
    warnings.warn('the `pep505.hook.activate()` function is obsolete and taken over by the `parsinghook` package.', DeprecationWarning)
