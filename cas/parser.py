from .model import *
from lark import Lark, Transformer
from typing import Union

## Concrete to Abstract Tree

class MathAst(Transformer):

    def eqn(self, args):
        return Equation(args[0], args[1])

    def asn(self, args):
        return Assignment(Var(args[0].value), args[1])

    def add(self, args):
        return BinaryOp(BinaryOp.Op.ADD, args[0], args[1])

    def sub(sqelf, args):
        return BinaryOp(BinaryOp.Op.SUB, args[0], args[1])
    
    def mul(self, args):
        return BinaryOp(BinaryOp.Op.MUL, args[0], args[1])
    
    def div(self, args):
        return BinaryOp(BinaryOp.Op.DIV, args[0], args[1])
    
    def exp(self, args):
        return BinaryOp(BinaryOp.Op.EXP, args[0], args[1])

    def neg(self, args):
        return UnaryOp(UnaryOp.Op.NEG, args[0])

    def fun(self, args):
        fn = args[0].value  # token
        expr = args[1] # .children
        return Function(Function.Name(fn), expr)

    def par(self, args):
        # parenthetical expression
        return args[0]

    def var(self, args):
        return Var(args[0].value)

    def num(self, args):
        return Num(float(args[0].value))


transformer = MathAst()
raw_parser = Lark.open('math.lark')


def parse(expr_str) -> Union[Equation, Node]:
    return transformer.transform(raw_parser.parse(expr_str)) 
