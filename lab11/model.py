import operator

class Scope(object):
    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def __getitem__(self, item):
        if item in self.dict:
            return self.dict[item]
        if self.parent:
            return self.parent[item]
        else:
            raise Exception

    def __setitem__(self, key, value):
        self.dict[key] = value


class Number:
    def __init__(self, value):
        self.value = int(value)

    def evaluate(self, scope):
        return self


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class UnaryOperation:
    ops = {"-": operator.neg,
            "!":operator.not_}

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        a = self.expr.evaluate(scope).value
        return Number(self.ops[self.op](a))


class BinaryOperation:
    ops = {"+": operator.add,
            "-":operator.sub,
            "*":operator.mul,
            "/":operator.floordiv,
            "%":operator.mod,
            "==":operator.is_,
            "!=":operator.is_not,
            "<":operator.lt,
            ">":operator.gt,
            "<=":operator.le,
            ">=":operator.ge,
            "&&":lambda x, y: bool(x and y),
            "||":lambda x, y: bool(x or y)}

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self, scope):
        l = self.lhs.evaluate(scope).value
        r = self.rhs.evaluate(scope).value
        return Number(self.ops[self.op](l, r))


class Function:
    def __init__(self, args, body):
        self.body = body
        self.args = args

    def evaluate(self, scope):
        last = Number(0)
        for x in self.body:
            last = x.evaluate(scope)
        return last


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.func = function

    def evaluate(self, scope):
        scope[self.name] = self.func
        return self.func


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.args = args
        self.fun_expr = fun_expr

    def evaluate(self, scope):
        func = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        results = [x.evaluate(scope) for x in self.args]
        for i, x in enumerate(func.args):
            call_scope[x] = results[i]
        return func.evaluate(call_scope)


class Conditional:
    def __init__(self, condition, if_true, if_false = None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        val = self.condition.evaluate(scope).value
        if val:
            body = self.if_true
        elif self.if_false:
            body = self.if_false
        else:
            body = []
        res = None
        for stmt in body:
            res = stmt.evaluate(scope)
        return res


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        a = self.expr.evaluate(scope)
        print(a.value)
        return a


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        a = int(input())
        scope[self.name] = a
        return Number(a)


def test():
    #Example
    parent = Scope()
    parent["bar"] = Number(10)
    scope = Scope(parent)
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'), '+', Reference('world')))])
    assert type(FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)) == Number
    assert scope["bar"].value == 10
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    assert type(scope["bar"]) == Number

    assert BinaryOperation(Number(5), "&&", Number(0)).evaluate(scope).value == 0
    assert BinaryOperation(Number(5), "&&", Number(-2)).evaluate(scope).value == 1
    assert UnaryOperation("!", Number(5)).evaluate(scope).value == 0


def test_number():
    scope = Scope()
    scope["bar"] = Number(20)
    assert type(scope["bar"]) == Number and Reference("bar").evaluate(scope).value == 20

def test_unary():
    scope = Scope()
    scope["a"] = Number(3)
    scope["b"] = Number(-5)
    scope["c"] = Number(0)
    r1 = UnaryOperation("-", Reference("a")).evaluate(scope).value
    r2 = UnaryOperation("!", Reference("a")).evaluate(scope).value
    r3 = UnaryOperation("-", Reference("b")).evaluate(scope).value
    r4 = UnaryOperation("!", Reference("b")).evaluate(scope).value
    r5 = UnaryOperation("-", Reference("c")).evaluate(scope).value
    r6 = UnaryOperation("!", Reference("c")).evaluate(scope).value
    assert r1 == -3
    assert r2 == 0
    assert r3 == 5
    assert r4 == 0
    assert r5 == 0
    assert r6 == 1

def test_conditional():
    scope = Scope()
    scope["a"] = Number(5)
    scope["b"] = Number(-3)
    cond1 = Conditional(BinaryOperation(Reference("a"), ">=", Reference("b")), [Reference("b"), Reference("a")], [Reference("a"), Reference("b")])
    cond2 = Conditional(BinaryOperation(Reference("a"), "<", Reference("b")), [Reference("b"), Reference("a")], [Reference("a"), Reference("b")])
    assert cond1.evaluate(scope).value == 5
    assert cond2.evaluate(scope).value == -3


if __name__ == '__main__':
    test()
    test_number()
    test_unary()
    test_conditional()
