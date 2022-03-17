from cas.model import Node, BinaryOp, Num, UnaryOp
from rules.rule import Rule


class IdentityAssociative(Rule):

	@staticmethod
	def matches(n: Node):
		return type(n) == BinaryOp \
		       and (type(n.a) == Num and n.a.val == 1
		            or type(n.b) == Num and n.b.val == 1)

	@staticmethod
	def apply(n: Node) -> Node:
		a = n.a
		b = n.b

		m = b if type(a) == Num and a.val == 1 else a  # non-identity value

		if n.op == BinaryOp.Op.MUL:
			# 1 * b = b * 1 = b
			return m

		return n


class NegatorAssociative(Rule):

	@staticmethod
	def matches(n: Node):
		return type(n) == BinaryOp \
		       and (type(n.a) == Num and n.a.val == -1
		            or type(n.b) == Num and n.b.val == -1)

	@staticmethod
	def apply(n: Node) -> Node:
		a = n.a
		b = n.b
		nn = b if type(a) == Num and a.val == -1 else a  # the non negative node

		if n.op == BinaryOp.Op.MUL:
			# -1 * n = n * -1 = -b
			return UnaryOp(UnaryOp.Op.NEG, nn)

		return n


class NegatorNonAssoc(Rule):

	@staticmethod
	def matches(n: Node):
		return type(n) == BinaryOp \
		       and (type(n.a) == Num and n.a.val == -1
		            or type(n.b) == Num and n.b.val == -1)

	@staticmethod
	def apply(n: Node) -> Node:
		a = n.a
		b = n.b

		if type(b) == Num and n.b.val == -1:
			if n.op == BinaryOp.Op.DIV:
				# a / -1 = -a
				return UnaryOp(UnaryOp.Op.NEG, a)

		return n