from model import *


class PrettyPrinterVisitor:

    def __init__(self):
        self.depth = 0

    def visit(self, tree, is_sentence = True):
        name = tree.__class__.__name__

        try:
            func = getattr(self, 'visit' + name)
        except:
            print("Method for {} not found!".format(name))
            raise NotImplementedError

        if is_sentence:
            print("    " * self.depth, end = "")
        func(tree)
        if is_sentence:
            print(";")


class PrettyPrinter(PrettyPrinterVisitor):

    def visitNumber(self, num):
        print(num.value, end = "")

    def visitFunction(self, fun):
        print("(", end = "")
        for i, arg in enumerate(fun.args):
            print(arg, end = "")
            if i + 1 != len(fun.args):
                print(", ", end = "")
        print(") {")

        if fun.body is not None:
            self.depth += 1
            for expr in fun.body:
                self.visit(expr)
            self.depth -= 1
        print("    " * self.depth + "}", end = "")

    def visitFunctionDefinition(self, fun_def):
        print("def {}".format(fun_def.name), end = "")
        self.visit(fun_def.function, False)

    def visitConditional(self, cond):
        print("if (", end = "")
        self.visit(cond.condition, False)
        print(") {")
        if cond.if_true is not None:
            self.depth += 1
            for expr in cond.if_true:
                self.visit(expr)
            self.depth -= 1
        print("    " * self.depth + "}", end = "")
        if cond.if_false is not None and len(cond.if_false) != 0:
            print(" else {")
            self.depth += 1
            for expr in cond.if_false:
                self.visit(expr)
            self.depth -= 1
            print("    " * self.depth + "}", end = "")

    def visitPrint(self, my_print):
        print("print ", end = "")
        self.visit(my_print.expr, False)

    def visitRead(self, my_read):
        print("read " + my_read.name, end = "")

    def visitFunctionCall(self, fun_call):
        print(fun_call.fun_expr.name + "(", end = "")
        for i, arg in enumerate(fun_call.args):
            self.visit(arg, False)
            if i + 1 != len(fun_call.args):
                print(", ", end = "")
        print(")", end = "")

    def visitReference(self, ref):
        print(ref.name, end = "")

    def visitBinaryOperation(self, op):
        print("(", end = "")
        self.visit(op.lhs, False)
        print(" " + op.op + " ", end = "")
        self.visit(op.rhs, False)
        print(")", end = "")

    def visitUnaryOperation(self, op):
        print("(" + op.op, end = "")
        self.visit(op.expr, False)
        print(")", end = "")


def example():
    printer = PrettyPrinter()

    number = Number(42)
    conditional = Conditional(number, [number], [])
    printer.visit(conditional)
    print("")

    function = Function([], [conditional])
    definition = FunctionDefinition("foo", function)
    printer.visit(definition)
    print("")

    my_print = Print(number)
    printer.visit(my_print)
    print("")

    my_read = Read("x")
    printer.visit(my_read)
    print("")

    printer.visit(number)
    print("")

    reference = Reference("f")
    printer.visit(reference)
    print("")

    n0, n1, n2 = Number(1), Number(2), Number(3)
    add = BinaryOperation(n1, '+', n2)
    mul = BinaryOperation(n0, '*', add)
    printer.visit(mul)
    print("")

    unary = UnaryOperation('-', mul)
    printer.visit(unary)
    print("")

    call = FunctionCall(reference, [n0, n1, n2])
    printer.visit(call)
    print("")


def my_tests():
    scope = Scope()
    printer = PrettyPrinter()

    n, m = Read('n'), Read('m')
    printer.visit(n)
    n.evaluate(scope)
    printer.visit(m)
    m.evaluate(scope)

    out = Print(BinaryOperation(Reference('n'),  '*', Reference('m')))
    printer.visit(out)
    out.evaluate(scope)

    scope['g'] = Function(['n', 'm'],
                          [
                           Print(BinaryOperation(Reference('n'), '*', Reference('m'))),
                           Print(Reference('n')),
                           Print(Reference('m'))
                          ])
    g_definition = FunctionDefinition('g', scope['g'])
    printer.visit(g_definition)

    scope['f'] = Function(['n', 'm'],
                          [
                           Conditional(BinaryOperation(Reference('n'), '>=', Reference('m')),
                                       [
                                        Print(Reference('n')),
                                        FunctionCall(FunctionDefinition('g', scope['g']),
                                                     [Reference('m'), BinaryOperation(Reference('n'), '%', Reference('m'))])
                                       ],
                                       [
                                        Print(UnaryOperation('-', Reference('n')))
                                       ])
                          ])

    f_definition = FunctionDefinition('f', scope['f'])
    printer.visit(f_definition)

    call = FunctionCall(f_definition, [Reference('n'), Reference('m')])
    printer.visit(call)
    call.evaluate(scope)


if __name__ == "__main__":
    example()
    my_tests()
