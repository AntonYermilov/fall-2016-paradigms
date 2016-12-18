class Scope:
    
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}

    def __getitem__(self, key):
        if not key in self.values:
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

        if if_true == None:
            if_true = []
        self.if_true = if_true
        
        if if_false == None:
            if_false = []
        self.if_false = if_false

    def evaluate(self, scope):
        res = None
        for expr in self.if_true if self.condition.evaluate(scope).value != 0 else self.if_false:
            res = expr.evaluate(scope)
        return res


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        num = self.expr.evaluate(scope)
        print(num.value)
        return num


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
        for name, arg in zip(function.args, self.args):
            call_scope[name] = arg.evaluate(scope)
        return function.evaluate(call_scope)


class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

class Operation:
    binary = {
                '+': lambda x, y: x + y,
                '-': lambda x, y: x - y,
                '*': lambda x, y: x * y,
                '/': lambda x, y: x // y,
                '%': lambda x, y: x % y,
                '==': lambda x, y: x == y,
                '!=': lambda x, y: x != y,
                '<': lambda x, y: x < y,
                '>': lambda x, y: x > y,
                '<=': lambda x, y: x <= y,
                '>=': lambda x, y: x >= y,
                '&&': lambda x, y: x != 0 and y != 0,
                '||': lambda x, y: x != 0 or y != 0,
             }
    unary  = {
                '-': lambda x: -x,
                '!': lambda x: not x
             }

class BinaryOperation:

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        return Number(int(Operation.binary[self.op](self.lhs.evaluate(scope).value, self.rhs.evaluate(scope).value)))

class UnaryOperation:

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        return Number(int(Operation.unary[self.op](self.expr.evaluate(scope).value)))
