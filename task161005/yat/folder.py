from model import *
from printer import *


class ConstantFolderVisitor:

    def visit(self, tree):
        name = tree.__class__.__name__

        try:
            func = getattr(self, 'visit' + name)
        except:
            print("Method for {} not found!".format(name))
            raise NotImplementedError

        return func(tree)


class ConstantFolder(ConstantFolderVisitor):

    def visitNumber(self, num):
        return num

    def visitFunction(self, fun):
        if fun.body is not None:
            for i in range(len(fun.body)):
                fun.body[i] = self.visit(fun.body[i])
        return fun

    def visitFunctionDefinition(self, fun_def):
        fun_def.function = self.visit(fun_def.function)
        return fun_def

    def visitConditional(self, cond):
        cond.condition = self.visit(cond.condition)
        if cond.if_true is not None:
            for i in range(len(cond.if_true)):
                cond.if_true[i] = self.visit(cond.if_true[i])
        if cond.if_false is not None:
            for i in range(len(cond.if_false)):
                cond.if_false[i] = self.visit(cond.if_false[i])
        return cond

    def visitPrint(self, my_print):
        my_print.expr = self.visit(my_print.expr)
        return my_print

    def visitRead(self, my_read):
        return my_read

    def visitFunctionCall(self, fun_call):
        for i in range(len(fun_call.args)):
            fun_call.args[i] = self.visit(fun_call.args[i])
        return fun_call

    def visitReference(self, ref):
        return ref

    def visitBinaryOperation(self, op):
        op.lhs = self.visit(op.lhs)
        op.rhs = self.visit(op.rhs)
        if isinstance(op.lhs, Number) and isinstance(op.rhs, Number):
            return op.evaluate(None)
        if isinstance(op.lhs, Number) and op.lhs.value == 0 and op.op == '*':
            return Number(0)
        if isinstance(op.rhs, Number) and op.rhs.value == 0 and op.op == '*':
            return Number(0)
        if isinstance(op.lhs, Reference) and isinstance(op.rhs, Reference) and op.op == '-' and op.lhs.name == op.rhs.name:
            return Number(0)
        return op

    def visitUnaryOperation(self, op):
        if isinstance(op.expr, Number):
            return op.evaluate(None)
        return op


def my_tests():
    scope = Scope()
    printer = PrettyPrinter()
    folder = ConstantFolder()

    scope['g'] = Function(['n', 'm'],
                          [
                           Print(BinaryOperation(Reference('n'), '*', Reference('m'))),
                           Print(BinaryOperation(BinaryOperation(BinaryOperation(Number(3), '*', Number(5)), '/', Reference('n')), '-', Number(7))),
                           Print(BinaryOperation(Reference('m'), '-', Reference('m')))
                          ])
    g_definition = FunctionDefinition('g', scope['g'])

    scope['f'] = Function(['n', 'm'],
                          [
                           Conditional(BinaryOperation(Reference('n'), '>=', Reference('m')),
                                       [
                                        g_definition,
                                        Print(BinaryOperation(Reference('n'), '*', Number(0))),
                                        FunctionCall(g_definition, [Reference('m'), BinaryOperation(Reference('n'), '%', Reference('m'))])
                                       ],
                                       [
                                        Print(UnaryOperation('!', Number(0)))
                                       ])
                          ])

    f_definition = FunctionDefinition('f', scope['f'])
    printer.visit(f_definition)

    print("\n====================================\n")

    f_definition = folder.visit(f_definition)
    printer.visit(f_definition)

if __name__ == "__main__":
    my_tests()
