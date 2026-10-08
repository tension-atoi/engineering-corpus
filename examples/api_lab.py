"""Fictional Python API: deterministic inventory without a model dependency."""
import argparse
import ast
import json

SOURCE = 'class Queue:\n    def enqueue(self, item):\n        return [item]\n'


def validate(symbol):
    module = ast.parse(SOURCE)
    exports = [f'{node.name}.{method.name}' for node in module.body if isinstance(node, ast.ClassDef)
               for method in node.body if isinstance(method, ast.FunctionDef) and not method.name.startswith('_')]
    assert symbol in exports, f'unknown symbol: {symbol}; inventory: {exports}'
    namespace = {}
    exec(compile(module, '<fictional-queue>', 'exec'), namespace)
    assert namespace['Queue']().enqueue('parcel') == ['parcel']
    return {'symbol': symbol, 'exports': exports, 'example': ['parcel']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', default='Queue.enqueue')
    print(json.dumps(validate(parser.parse_args().symbol), sort_keys=True))
