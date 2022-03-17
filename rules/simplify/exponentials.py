from cas.model import Node, BinaryOp, Num
from rules.rule import Rule


class ExponentRules(Rule):

	@staticmethod
	def matches(n: Node):
		return type(n) == BinaryOp \
		       and type(n.op) == BinaryOp.Op.EXP

	@staticmethod
	def apply(n: Node):
		a = n.a
		b = n.b
		if type(a) == Num:
			if a.val == 1:
				# 1 ** b = 1
				return Num(1)
			elif a.val == -1:
				# -1 ** b = 1 if b is even
				# -1 ** b = -1 if b is odd
				return Num(1) if b.val % 2 == 0 else Num(-1)
			elif a.val == 0 and b.val > 0:
				# 0 ** b = 0, n > 0
				# 0 ** 0 = undef
				# 0 ** -b = b / 0 = undef
				return Num(0)
		elif type(b) == Num:
			if b.val == 0:
				# a ** 0 = 1
				return Num(1)
			elif b.val == 1:
				# a ** 1 = a
				return a
			elif b.val <= -1:
				# a ** -k = 1 / (a ** k)
				return BinaryOp(BinaryOp.Op.DIV, Num(1), BinaryOp(BinaryOp.Op.EXP, a, b.val))

		return n