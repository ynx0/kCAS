from cas.model import Node, BinaryOp, Var, Num
from rules.rule import Rule


class CombineLikeVars(Rule):

	# basic variable arithmetic

	@staticmethod
	def matches(n: Node):
		return type(n) == BinaryOp \
		       and type(n.a) == Var and type(n.b) == Var \
		       and n.a.name == n.b.name

	@staticmethod
	def apply(n: Node) -> Node:
		a = n.a

		if n.op == BinaryOp.Op.ADD:
			# a + a -> 2 * a
			return BinaryOp(BinaryOp.Op.MUL, 2, Var(a.name))
		elif n.op == BinaryOp.Op.MUL:
			# a * a = a**2
			return BinaryOp(BinaryOp.Op.EXP, Var(a.name), 2)
		elif n.op == BinaryOp.Op.SUB:
			# a - a = 0
			return Num(0)
		elif n.op == BinaryOp.Op.DIV:
			# a / a = 1
			return Num(1)

		return n
