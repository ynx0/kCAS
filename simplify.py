# Rules
from functools import partial

from cas.model import *
from rules.canonical import canon
from rules.simplify import *
from rules.rule import Rule


def simplify(n: Node) -> Node:
	# having the recursive calls at the top ensures bottom-up recursion,
	# because say you have e = UnOp(NEG, a=Fn(SIN, x=BinOp(ADD, a=Num(2), b=Num(4))))
	# the recursion would return an UnOp but call simplify on Fn (e.a)
	# which would then call simplify on BinOp (e.a)
	# which would then call simplify on Num(2) (e.a.a) and Num(4) (e.a.b)
	# which would produce
	# simp(Num(2)) => Num(2)
	# simp(Num(4)) => Num(4)
	# simp(Num(2) + Num(4)) => Num(6)
	# ...

	# so now we don't have to ever call simplify in any rule,
	# because we can assume that any node you get has its children simplified

	assert n is not None

	rules = [
		canon.DoubleNeg,
		canon.Coefficients,
		const.InlineNegNum,
		const.InlineConstant,
		zero.Associative, zero.NonAssociative,
		identity.IdentityAssociative,
		exponentials.ExponentRules,
		identity.NegatorAssociative,
		identity.NegatorNonAssoc,
		algebra.CombineLikeVars,
	]

	apply_rules = partial(Rule.apply_all, rules=rules)

	if type(n) == BinaryOp:
		return apply_rules(BinaryOp(n.op, simplify(n.a), simplify(n.b)))
	elif type(n) == Function:
		return apply_rules(Function(n.f, simplify(n.x)))
	elif type(n) == UnaryOp:
		return apply_rules(UnaryOp(n.op, simplify(n.a)))
	elif type(n) == Var or type(n) == Num:
		# simplification terminals. recursion ends here
		return apply_rules(n)
	elif type(n) == Assignment:
		return apply_rules(Assignment(n.lhs, simplify(n.rhs)))
	else:
		assert False, f'Unhandled node type {type(n)}'


def simplify_deep(n: Node, max_iter=100):
	# keep running simplify on the expr until it is equal to
	# the previous simplified output or max depth or timeout exceeded
	i = 0
	previous_expr = None

	while n != previous_expr and i < max_iter:
		previous_expr = n  # will this break b/c its only a reference?
		n = simplify(n)
		i += 1

	return n
