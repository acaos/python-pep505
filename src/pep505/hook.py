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


import os
import re
import sys

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location, decode_source

from . import parser as python_parser


PEP505_DEBUG = os.getenv('PYTHON_PEP505_DEBUG')
COALESCE_REGEX = re.compile(r'(\?\?|\?\.|\?\[)')


class Pep505MetaPathFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if not path:
            path = sys.path

        if '.' in fullname:
            name = fullname.split('.')[-1]
        else:
            name = fullname

        for entry in path:
            if entry in ('', '.'):
                entry = os.getcwd()
            filename = os.path.join(entry, name + '.py')
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    contents = f.read()
                    source = decode_source(contents)

                    # TODO: optimize this so the file doesn't get read twice
                    if COALESCE_REGEX.search(source) is not None:
                        return spec_from_file_location(fullname, filename, loader=Pep505Loader(filename))

                return None

        return None


class Pep505Loader(Loader):
    def __init__(self, filename):
        self._filename = filename
        pass

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        if PEP505_DEBUG:
            sys.stderr.write(f'parsing and executing {self._filename}\n')

        with open(self._filename, 'r') as f:
            tokengen = tokenize.generate_tokens(f.readline)
            tokenizer = python_parser.Tokenizer(tokengen)
            parser = python_parser.PythonParser(tokenizer)
            tree = parser.start()

        code_object = compile(tree, self._filename, 'exec')
        exec(code_object, module.__dict__)

activated = False

def activate():
    global activated

    if not activated:
        finder = Pep505MetaPathFinder()
        sys.meta_path.insert(0, finder)
        activated = True
