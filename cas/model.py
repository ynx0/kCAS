from abc import ABC
from enum import Enum, unique


# TODO we need to implement deep equals

# this file could also be called types.py
# Proper Types for Equation / Node tree


# root object. either an equation or a node
class Obj(ABC):

	@property
	def is_node(self):
		return issubclass(type(self), Node)

	@property
	def is_equation(self):
		return issubclass(type(self), Equation)


class Node(Obj, ABC):
	pass


class Equation(Obj):
	def __init__(self, lhs: Node, rhs: Node):
		self.lhs = lhs
		self.rhs = rhs

	def __repr__(self):
		return f"Equation(lhs={self.lhs} rhs={self.rhs})"

	def __str__(self):
		return f"{self.lhs} = {self.rhs}"


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

	def __str__(self):
		return f"{self.a} {self.op.value} {self.b}"


class UnaryOp(Node):
	class Op(Enum):
		NEG = "-"

	def __init__(self, op, a):
		self.op = op
		self.a = a

	def __repr__(self):
		return f"UnaryOp(op={self.op.name}, a={self.a})"

	def __str__(self):
		return f"{self.op.value}{self.a}"


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

	def __str__(self):
		return f"{self.f.value}({self.x})"


class Var(Node):
	def __init__(self, name: str):
		assert type(name) == str, f'Var name {repr(name)}: {type(name)} not a string'
		self.name = name

	def __repr__(self):
		return f"Var({self.name})"

	def __str__(self):
		return self.name


class Num(Node):

	def __init__(self, val):
		self.val = float(val)  # normalize inputs

	def __repr__(self):
		return f"Num({self.val})"

	def __str__(self):
		# remove decimal if float is int
		val = int(self.val) if self.val.is_integer() else self.val
		return str(val)

