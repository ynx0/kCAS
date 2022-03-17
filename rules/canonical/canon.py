from cas.model import Node, UnaryOp, BinaryOp, Var, Num
from rules.rule import Rule


class DoubleNeg(Rule):

	# double negation cancels

	# --1: a = UnaryOp(op=NEG, a=UnaryOp(op=NEG, a=Num(1.0)))
	@staticmethod
	def matches(n: Node):
		if type(n) == UnaryOp:
			a = n.a
			return type(a) == UnaryOp and a.op == UnaryOp.Op.NEG

		return False

	# a.a == evaluate(a)
	# --1 == 1
	@staticmethod
	def apply(n: Node):
		a = n.a
		return a.a


class Coefficients(Rule):

	@staticmethod
	def matches(n: Node):
		if type(n) == BinaryOp:
			a = n.a
			b = n.b
			return type(a) == Var and type(b) == Num and n.op == BinaryOp.Op.MUL

	# a * 2 -> 2 * a
	@staticmethod
	def apply(n: Node):
		return BinaryOp(n.op, n.b, n.a)
