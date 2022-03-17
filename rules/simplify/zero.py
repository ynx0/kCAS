from cas.model import Node, BinaryOp, Num, UnaryOp
from rules.rule import Rule


class Associative(Rule):

	@staticmethod
	def matches(n: Node):
		return type(n) == BinaryOp \
		       and (type(n.a) == Num and n.a.val == 0
		            or type(n.b) == Num and n.b.val == 0)

	@staticmethod
	def apply(n: Node) -> Node:
		# TODO: should we convert 1 / b to b ** -1?
		a = n.a
		b = n.b
		nz = b if type(a) == Num and a.val == 0 else a  # the non zero node

		# 0 + n = n + 0 = n
		if n.op == BinaryOp.Op.ADD:
			return nz
		# 0 * n = n * 0 = 0
		elif n.op == BinaryOp.Op.MUL:
			return Num(0)


class NonAssociative(Rule):

	@staticmethod
	def matches(n: Node):
		return type(n) == BinaryOp \
		       and (type(n.a) == Num and n.a.val == 0
		            or type(n.b) == Num and n.b.val == 0)

	@staticmethod
	def apply(n: Node) -> Node:
		a = n.a
		b = n.b

		if n.op == BinaryOp.Op.SUB:
			# 0 - n = 0 + -n = -n
			if type(a) == Num and a.val == 0:
				return UnaryOp(UnaryOp.Op.NEG, b)
			elif type(b) == Num and b.val == 0:
				# n - 0 = n
				return b

		elif n.op == BinaryOp.Op.DIV:
			# b / 0 = undef, so nothing to simplify
			# 0 / b = 0
			if type(a) == Num and a.val == 0:
				return Num(0)

		return n
