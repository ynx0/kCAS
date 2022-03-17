from cas.model import Node, UnaryOp, Num, BinaryOp
from evaluate import evaluate
from rules.rule import Rule


class InlineNegNum(Rule):

	@staticmethod
	def matches(n: Node):
		return type(n) == UnaryOp \
		       and n.op == UnaryOp.Op.NEG \
		       and type(n.a) == Num

	# n: UnOp(NEG, Num(2)) -> Num(-2)
	@staticmethod
	def apply(n: Node):
		return Num(-1 * n.a.val)


class InlineConstant(Rule):

	# todo extend this to simplifying funcs w/ constant exprs. ez but gotta do it
	# n is of the form 4 * 5, i.e. BinOp(MUL, a=4, b=2)
	@staticmethod
	def matches(n: Node):
		return type(n) == BinaryOp \
		       and type(n.a) == Num and type(n.b) == Num

	@staticmethod
	def apply(n: Node) -> Node:
		return Num(evaluate(n))
