from abc import ABC, abstractmethod
from functools import reduce
from typing import List

from cas.model import Node


class Rule(ABC):
	# TODO maybe override >> operator to chain rules

	@staticmethod
	@abstractmethod
	def matches(n: Node) -> bool:
		# does the node's structure match.
		# in other words, is the node in such a condition that can we apply the rule?
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
	def apply_all(node: Node, rules: List['Rule']) -> Node:
		# Explanation
		# starting with the existing node n,
		# apply rule r to node n if it matches else produce n untouched;
		# then apply the next rule to the result of that
		# repeat for each rule
		return reduce(lambda n, r: r.apply_checked(n), rules, node)
