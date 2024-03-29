#!/usr/bin/env python3
import sys
from typing import Dict

from lark.exceptions import UnexpectedInput

from cas.model import Node, Assignment
from cas.parser import parse
from evaluate import evaluate, UnboundVariableError
from simplify import simplify


# use equation syntax for variable binding

# todo https://docs.python.org/3/library/readline.html
# or maybe: https://github.com/Textualize/textual


def main():
	ctx: Dict[str, Node] = dict()

	while 1:
		command = None

		text = input('> ')

		if text == '':
			continue

		if text.startswith('simp '):
			command = 'simp'
			text = text.replace('simp ', '')
		elif text.startswith('raw '):
			command = 'raw'
			text = text.replace('raw ', '')
		elif text == 'vars':
			print(ctx)
			continue

		try:
			expr = parse(text)

		except UnexpectedInput as e:
			print('Error: bad expression')
			print(e)
			continue

		if type(expr) == Assignment:
			ctx[expr.lhs.name] = expr.rhs
			continue

		try:
			ret = None
			if command is None:
				ret = evaluate(expr, ctx)
			elif command == 'simp':
				ret = simplify(expr)
			elif command == 'raw':
				ret = expr
		except UnboundVariableError:
			print('Error: unbound variable exception')
			continue

		print(ret)


if __name__ == '__main__':
	try:
		main()
	except (KeyboardInterrupt, EOFError):
		sys.exit()
