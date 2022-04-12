# Notes

in the calc example, I couldn't figure out why for instance sum was defined as also being a product. well, it has to do with order of operations and chaining each expression type.

here is an equivalent construction:
```

sum: (product | sum) "+" (product | sum)

```

todo write out simple toy grammar


## brainstorm 1

we want to be able to apply basic transformations on equations
as such, we need a format that can be parsed into a math expression
which can then be manipulated into another math expression which is ultimately the result
algebraic rules
derivative rules
integral rules (identities)


example problem / interface we want:

```
solve("2x + 4 = 8", "x")

1. 2x + 4 = 8
isolation tactic:
2. 2x = 8 - 4
simplifiy
3. 2x = 4
transformations to x are: 2 *. invert. 1/2 *
x = 4 / 2
simplify
x = 2

lhs = x,
solve for: x

finished.
```


----



Ok so officially dubbed milestone one is complete. We have a basic parser which supports parsing PEMDAS expressions, basic functions, and an equation mode which has two arbitrary expressions on either side of the "=" sign.  some kind of integral solver that goes in the following chain
1. identity
2. 




The next step would be to implement some sort of interpreter / transformer on the ast. The first thing is to clean up the tree and lift it to Python objects that we make up from it's parse tree representation.

Then we can start implementing "tactics" (borrowed loosely from proof assistant terminology) that basically I manually encode, which provide mathematical equivalence statements that preserve algebraic invariants but allow for reduction of some kind. 

I'll be defining the tactics manually, and then using them manually as well at the python repl. One could then imagining automating some of these and making a simple "brute-force" algebra solver.




Later, we could imagine some kind of integral solver that goes in the following chain
1. identity
2. u sub
3. product rule
4. pfd
5. 
and if one fails, it goes for the next one until it suceeds and results in a new equation. then it goes back to the beginning of the heuristic chain and keeps applying until all tactics fail or the result is reduced to what was requested.


----


ok, so in our transformer, we want to "switch" on if it is an expr or equation.

if it is an expression, we evaluate it. if it is an equation we (for now) return the equation verbatim. 
later we can try something like "simplifying" the equation.

but we gotta make our own AST repr first.

## note 14 mar

problem with doing something like

```
?sum: sum "+" sum  -> add
    | sum "-" sum  -> sub
    | product
```

is that the grammar will, if given parenthesis, associate everything else right as well which is incorrect (although not the end of the world for evaluation, it could mess up simplification rules on objs that are not commutative)

if we try the expression `x * y * z`, we get what we should: which is essentially `(x * y) * z`
but if we try `x * y * (z)`, although no different semantically, the `y` gets pulled into the right subtree erroneously as:
`x * (y * z)`.


that's why you have to do something like:


```
?sum: sum "+" product  -> add
    | sum "-" product  -> sub
    | product
```

which is what the original `calc.py` example shows.

having a lower precedent thing explicitly on the right and the the higher precedent thing on the left
makes sum always match first on the left side.


still don't know exactly why tho.



---

dumping some code that doesn't have a home

```python
exprs = """
1 / 2 * x
2**50 + 1
1 * 1 + 2 * 2
2 * 1 + 4
2 - 3 + 1
(cos(x**(2 + sqrt(1))) + 1) / 2
-sin(x)**2 = 2 * a
x * -2 * (sqrt(100) * 0)
""".strip().split('\n')

```


----


further stuff: more simplfication rules,

constraints system ????????????????????????????????

user defined functions

bigints

recursive user-defined functions (with memoziation)


