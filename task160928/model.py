#!/usr/bin/env python3

class Scope:
    
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}

    def __getitem__(self, key):
        if self.values.get(key) == None:
            return self.parent[key]
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value


class Number:

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        res = None
        for expr in self.body:
            res = expr.evaluate(scope)
        return res


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        res = None
        if self.condition.evaluate(scope).value != 0:
            if self.if_true != None:
                for expr in self.if_true:
                    res = expr.evaluate(scope)
        else:
            if self.if_false != None:
                for expr in self.if_false:
                    res = expr.evaluate(scope)
        return res


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        print(self.expr.evaluate(scope).value)
        return self.expr.evaluate(scope)


class Read:
    
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))
        return scope[self.name]


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for i in range(len(function.args)):
            call_scope[function.args[i]] = self.args[i].evaluate(scope)
        return function.evaluate(call_scope)


class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        if self.op == '+':
            return Number(self.lhs.evaluate(scope).value + self.rhs.evaluate(scope).value)
        if self.op == '-':
            return Number(self.lhs.evaluate(scope).value - self.rhs.evaluate(scope).value)
        if self.op == '*':
            return Number(self.lhs.evaluate(scope).value * self.rhs.evaluate(scope).value)
        if self.op == '/':
            return Number(self.lhs.evaluate(scope).value // self.rhs.evaluate(scope).value)
        if self.op == '%':
            return Number(self.lhs.evaluate(scope).value % self.rhs.evaluate(scope).value)
        if self.op == '==':
            return Number(self.lhs.evaluate(scope).value == self.rhs.evaluate(scope).value)
        if self.op == '!=':
            return Number(self.lhs.evaluate(scope).value != self.rhs.evaluate(scope).value)
        if self.op == '<':
            return Number(self.lhs.evaluate(scope).value < self.rhs.evaluate(scope).value)
        if self.op == '>':
            return Number(self.lhs.evaluate(scope).value > self.rhs.evaluate(scope).value)
        if self.op == '<=':
            return Number(self.lhs.evaluate(scope).value <= self.rhs.evaluate(scope).value)
        if self.op == '>=':
            return Number(self.lhs.evaluate(scope).value >= self.rhs.evaluate(scope).value)
        if self.op == '&&':
            return Number(self.lhs.evaluate(scope).value != 0 and  self.rhs.evaluate(scope).value != 0)
        if self.op == '||':
            return Number(self.lhs.evaluate(scope).value != 0 or  self.rhs.evaluate(scope).value != 0)
        return None

class UnaryOperation:

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        if self.op == '-':
            return Number(-self.expr.value)
        if self.op == '!':
            return Number(0 if self.expr.value != 0 else 1)
        return None


def example():
    parent = Scope()
    parent['foo'] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent['bar'] = Number(10)
    scope = Scope(parent)
    assert 10 == scope['bar'].value
    scope['bar'] = Number(20)
    assert scope['bar'].value == 20
    assert parent['bar'].value == 10
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)

def my_tests():
    scope = Scope()
    Read('n').evaluate(scope)
    Read('m').evaluate(scope)
    Print(BinaryOperation(Reference('n'),  '*', Reference('m'))).evaluate(scope)

    scope['g'] = Function(('n', 'm'),
                          [Print(BinaryOperation(Reference('n'), '*', Reference('m'))),
                           Print(Reference('n')),
                           Print(Reference('m'))
                          ])

    scope['f'] = Function(('n', 'm'),
                          [Conditional(BinaryOperation(Reference('n'), '>=', Reference('m')),
                                     [Print(Reference('n')),
                                      FunctionCall(FunctionDefinition('g', scope['g']),
                                                   [Reference('m'), BinaryOperation(Reference('n'), '%', Reference('m'))]),
                                     ])
                          ])
    FunctionCall(FunctionDefinition('f', scope['f']),
                 [Reference('n'), Reference('m')]).evaluate(scope)


if __name__ = '__main__':
    example()
    my_tests()
