from typing import Union
from abc import ABC
from enum import Enum, unique

# this file could also be called types.py
# Proper Types for Equation / Node tree

# root object. either an equation or a node
class Obj(ABC):

    def __str__(self):
        n = self
        # assert type(n) == Equation or issubclass(type(n), Node), f'Invalid input type {type(n)}'
        if type(n) == Num:
            # remove decimal if float is int
            val = int(n.val) if n.val.is_integer() else n.val
            return str(val)
        elif type(n) == Var:
            return n.name
        elif type(n) == Function:
            return f"{n.f.value}({n.x})"
        elif type(n) == UnaryOp:
            return f"{n.op.value}{n.a}"
        elif type(n) == BinaryOp:
            return f"{n.a} {n.op.value} {n.b}"
        elif type(n) == Equation or type(n) == Assignment:
            return f"{n.lhs} = {n.rhs}"
        else:
            assert False, f'Unhandled node type {type(n)}'


class Node(Obj, ABC):
    pass


class Equation(Obj):
    def __init__(self, lhs: Node, rhs: Node):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return f"Equation(lhs={self.lhs} rhs={self.rhs})"


class Assignment(Equation):
    def __init__(self, lhs: 'Var', rhs: Node):
        assert type(lhs) == Var
        super().__init__(lhs, rhs)

    def __repr__(self):
        return f"Assignment(lhs={self.lhs} rhs={self.rhs})"



class BinaryOp(Node):

    @unique
    class Op(Enum):
        ADD = "+"
        SUB = "-"
        MUL = "*"
        DIV = "/"
        EXP = "**"

    def __init__(self, op, a, b):
        self.op = op
        self.a = a
        self.b = b

    def __repr__(self):
        return f"BinOp(op={self.op.name}, a={self.a} b={self.b})"



class UnaryOp(Node):

    class Op(Enum):
        NEG = "-"
    
    def __init__(self, op, a):
        self.op = op
        self.a = a

    def __repr__(self):
        return f"UnaryOp(op={self.op.name}, a={self.a})"


class Function(Node):

    @unique
    class Name(Enum):
        SIN = "sin"
        COS = "cos"
        TAN = "tan"
        SQRT = "sqrt"
        LOG = "log"
        LN = "ln"
    
    def __init__(self, f, x):
        self.f = f
        self.x = x

    def __repr__(self):
        return f"Fn({self.f.name}, x={self.x})"


class Var(Node):
    def __init__(self, name: str):
        assert type(name) == str, f'Var name {repr(name)}: {type(name)} not a string'
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"

class Num(Node):
 
    def __init__(self, val):
        self.val = float(val)  # normalize inputs
 
    def __repr__(self):
        return f"Num({self.val})"

# misc functions

def is_node(o: Union[Equation, Node]):
    return issubclass(type(o), Node)

def is_equation(o: Union[Equation, Node]):
    return type(o) == Equation

