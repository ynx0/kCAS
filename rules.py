from functools import reduce, partial
from typing import List
from abc import ABC, abstractmethod
from evaluate import evaluate
from cas.model import *

# Rules

class Rule(ABC):
    # TODO maybe override >> operator to chain rules

    @staticmethod
    @abstractmethod
    def matches(n: Node) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def apply(n: Node) -> Node:
        # apply the rule's transformation
        # no assertions here. up to the caller to ensure the tree matches
        # thought: we could make the default return n unchanged, but that seems worse
        # because its likely a bug to have a rule with a match but no modification
        # when you really want something like that, if we have a lot of "passive" rules
        # which only print some info on something matching, then maybe it makes sense
        pass

    @classmethod
    def apply_checked(cls, n: Node) -> Node:
        return cls.apply(n) if cls.matches(n) else n

    @staticmethod
    def apply_all(n: Node, rules: List['Rule']) -> Node:
        return reduce(lambda n, r: r.apply_checked(n), rules, n)
        # Explanation
        # starting with the existing node n,
        # apply rule r to node n if it matches else produce n untouched;
        # then apply the next rule to the result of that
        # repeat for each rule


## Simplification Rules

class InlineNegNum(Rule):

    def matches(n: Node):
        return type(n) == UnaryOp \
           and n.op == UnaryOp.Op.NEG \
           and type(n.a) == Num

    # n: UnOp(NEG, Num(2)) -> Num(-2)
    def apply(n: Node):
        return Num(-1 * n.a.val)

class InlineConstant(Rule):

    # n is of the form 4 * 5, i.e. BinOp(MUL, a=4, b=2)
    def matches(n: Node):
        return type(n) == BinaryOp \
           and type(n.a) == Num and type(n.b) == Num       

    def apply(n: Node) -> Node:
        return Num(evaluate(n))


### bin op simplifiers

### e.g. 4 * x

class SimpZeroAssoc(Rule):

    def matches(n: Node):
        return type(n) == BinaryOp \
           and (type(n.a) == Num and n.a.val == 0 \
            or  type(n.b) == Num and n.b.val == 0)
    
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

class SimpZeroNonAssoc(Rule):

    def matches(n: Node):
        return type(n) == BinaryOp \
           and (type(n.a) == Num and n.a.val == 0 \
            or  type(n.b) == Num and n.b.val == 0)

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


class SimpIdentityAssoc(Rule):

    def matches(n: Node):
        return type(n) == BinaryOp \
           and (type(n.a) == Num and n.a.val == 1 \
            or  type(n.b) == Num and n.b.val == 1)

    def apply(n: Node) -> Node:
        a = n.a
        b = n.b

        m = b if type(a) == Num and a.val == 1 else a # non-identity value

        if n.op == BinaryOp.Op.MUL:
            # 1 * b = b * 1 = b
            return m

        return n


class SimpExpRules(Rule):
    def matches(n: Node):
        return type(n) == BinaryOp \
           and type(n.op) == BinaryOp.Op.EXP

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


class SimpNegatorAssoc(Rule):

    def matches(n: Node):
        return type(n) == BinaryOp \
           and (type(n.a) == Num and n.a.val == -1 \
            or  type(n.b) == Num and n.b.val == -1)

    def apply(n: Node) -> Node:
        a = n.a
        b = n.b
        nn = b if type(a) == Num and a.val == -1 else a  # the non negative node

        if n.op == BinaryOp.MUL:
            # -1 * n = n * -1 = -b
            return UnaryOp(UnaryOp.Op.NEG, nn)

        return n

class SimpNegatorNonAssoc(Rule):

    def matches(n: Node):
        return type(n) == BinaryOp \
           and (type(n.a) == Num and n.a.val == -1 \
            or  type(n.b) == Num and n.b.val == -1)

    def apply(n: Node) -> Node:
        a = n.a
        b = n.b

        if type(a) == Num and n.b.val == -1:
            if n.op == BinaryOp.DIV:
                # a / -1 = -a
                return UnaryOp(UnaryOp.Op.NEG, a)
            
        return n


class SimpCombineLikeVars(Rule):

    # basic variable arithmetic

    def matches(n: Node):
        return type(n) == BinaryOp \
           and type(n.a) == Var and type(n.b) == Var \
           and n.a.name == n.b.name

    def apply(n: Node) -> Node:
        a = n.a
        b = n.b

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

## Canonicalization
class CanonDoubleNeg(Rule):

    # double negation cancels

    # --1: a = UnaryOp(op=NEG, a=UnaryOp(op=NEG, a=Num(1.0)))
    def matches(n: Node):
        if type(n) == UnaryOp:
            a = n.a
            return type(a) == UnaryOp and a.op == UnaryOp.Op.NEG

        return False

    # a.a == evaluate(a)
    # --1 == 1
    def apply(n: Node):
        return a.a


class CanonCoeff(Rule):

    def matches(n: Node):
        if type(n) == BinaryOp:
            a = n.a
            b = n.b
            return type(a) == Var and type(b) == Num and n.op == BinaryOp.Op.MUL

    # a * 2 -> 2 * a
    def apply(n: Node):
        return BinaryOp(n.op, n.b, n.a)


def simplify(n: Node) -> Node:

    # doing this at the top ensures bottom-up recursion,
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
        InlineNegNum,
        InlineConstant,
        SimpZeroAssoc, SimpZeroNonAssoc,
        SimpIdentityAssoc,
        SimpExpRules,
        SimpNegatorAssoc,
        SimpNegatorNonAssoc,
        SimpCombineLikeVars,
        CanonDoubleNeg,
        CanonCoeff,
    ]

    apply_rules = partial(Rule.apply_all, rules=rules)

    if type(n) == BinaryOp:
        return apply_rules(BinaryOp(n.op, simplify(n.a), simplify(n.b)))
    elif type(n) == Function:
        return apply_rules(Function(n.f, simplify(n.x)))
    elif type(n) == UnaryOp:
        return apply_rules(UnaryOp(n.op, simplify(n.a)))
    elif type(n) == Var or type(n) == Num:
        return apply_rules(n)
        # simplification terminals. recursion ends here
    elif type(n) == Assignment:
        return apply_rules(Assignment(n.lhs, simplify(n.rhs)))
    else:
        assert False, f'Unhandled node type {type(n)}'


def simplify_deep():
    # todo keep running simplify on the expr until it is equal to
    # the previous simplified output or max depth or timeout exceeded
    pass

