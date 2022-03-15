from .model import *
from lark import Lark, Transformer
from typing import Union


## Concrete to Abstract Tree

class MathAst(Transformer):

	@staticmethod
	def eqn(args):
		return Equation(args[0], args[1])

	@staticmethod
	def asn(args):
		return Assignment(Var(args[0].value), args[1])

	@staticmethod
	def add(args):
		return BinaryOp(BinaryOp.Op.ADD, args[0], args[1])

	@staticmethod
	def sub(args):
		return BinaryOp(BinaryOp.Op.SUB, args[0], args[1])

	@staticmethod
	def mul(args):
		return BinaryOp(BinaryOp.Op.MUL, args[0], args[1])

	@staticmethod
	def div(args):
		return BinaryOp(BinaryOp.Op.DIV, args[0], args[1])

	@staticmethod
	def exp(args):
		return BinaryOp(BinaryOp.Op.EXP, args[0], args[1])

	@staticmethod
	def neg(args):
		return UnaryOp(UnaryOp.Op.NEG, args[0])

	@staticmethod
	def fun(args):
		fn = args[0].value  # token
		expr = args[1]  # .children
		return Function(Function.Name(fn), expr)

	@staticmethod
	def par(args):
		# parenthetical expression
		return args[0]

	@staticmethod
	def var(args):
		return Var(args[0].value)

	@staticmethod
	def num(args):
		return Num(float(args[0].value))


transformer = MathAst()
raw_parser = Lark.open('math.lark')


def parse(expr_str) -> Union[Equation, Node]:
	return transformer.transform(raw_parser.parse(expr_str))
