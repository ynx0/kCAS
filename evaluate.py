import math
from typing import Dict
from cas.model import *


# Node Evaluation
class UnboundVariableError(RuntimeError):
	pass


def evaluate(n: Node, bound_vars: Dict[str, Node] = None):
	assert n.is_node, f'Parameter {n}: {type(n)} is not a node'
	bound_vars = bound_vars or dict()

	if type(n) == Num:
		return n.val
	elif type(n) == Var:
		val = bound_vars.get(n.name)
		if val is None:
			raise UnboundVariableError(f"Error: Unbound variable '{n.name}'")

		return evaluate(val, bound_vars)

	elif type(n) == Function:
		f = {
			'sin': math.sin,
			'cos': math.cos,
			'tan': math.tan,
			'sqrt': math.sqrt,
			'log': math.log10,
			'ln': math.log
		}[n.f.value]
		x = evaluate(n.x, bound_vars)
		return f(x)

	elif type(n) == UnaryOp:
		x = evaluate(n.a, bound_vars)
		if n.op == UnaryOp.Op.NEG:
			return -1 * x
		else:
			assert False, f'Unhandled unary operation {n.op}'

	elif type(n) == BinaryOp:
		a = evaluate(n.a, bound_vars)
		b = evaluate(n.b, bound_vars)

		if n.op == BinaryOp.Op.ADD:
			return a + b
		elif n.op == BinaryOp.Op.SUB:
			return a - b
		elif n.op == BinaryOp.Op.MUL:
			return a * b
		elif n.op == BinaryOp.Op.DIV:
			return a / b
		elif n.op == BinaryOp.Op.EXP:
			return a ** b
		else:
			assert False, f'Unhandled binary operation {n.op}'

	else:
		print(f'evaluate: unimplemented node type {type(n)}')
