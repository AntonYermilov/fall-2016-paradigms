import sys
import unittest
import io
from model import *

class ScopeTest(unittest.TestCase):
    def test_isInScope(self):
        scope = Scope()
        scope["a"] = 2
        self.assertEqual(scope["a"], 2)
    def test_isInParent(self):
        parent = Scope()
        scope = Scope(parent)
        parent["a"] = 2
        scope["b"] = 3
        self.assertEqual(scope["a"], 2)
    def test_isInCurrentScope(self):
        parent = Scope()
        scope = Scope(parent)
        parent["a"] = 2
        scope["a"] = 3
        self.assertEqual(scope["a"], 3)

class NumberTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        self.scope["a"] = Number(2)
    def test_isNumber(self):
        self.assertIsInstance(self.scope["a"], Number)
        self.assertIsInstance(self.scope["a"].evaluate(self.scope), Number)
    def test_equal(self):
        self.assertEqual(self.scope["a"].value, 2)
        self.assertEqual(self.scope["a"].evaluate(self.scope), self.scope["a"])
        
class ReferenceTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_reference(self):
        self.scope["a"] = Number(100500)
        self.assertIsInstance(Reference("a").evaluate(self.scope), Number)
        self.assertEqual(Reference("a").evaluate(self.scope).value, 100500)

class FunctionTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        self.scope["func1"] = Function(["a", "b", "c"], [Number(5), Number(3), Number(2)])
        self.scope["func2"] = Function(["arg"], [])
    def test_instances(self):
        self.assertIsInstance(self.scope["func1"].args, list)
        self.assertIsInstance(self.scope["func1"].body, list)
        self.assertIsInstance(self.scope["func1"].evaluate(self.scope), Number)
    def test_results(self):
        self.assertEqual(self.scope["func1"].evaluate(self.scope).value, 2)
        self.assertEqual(self.scope["func2"].evaluate(self.scope), None)
    
class FunctionDefinitionTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        self.function = Function(["arg"], [Number(1), Number(2)])
        self.definition = FunctionDefinition("func", self.function)
    def test_functionDefinition(self):
        self.assertIsInstance(self.definition.name, str)
        self.assertIsInstance(self.definition.function, Function)
        self.assertIsInstance(self.definition.evaluate(self.scope), Function)
        self.assertIsInstance(self.scope["func"], Function)
        self.assertEqual(self.scope["func"], self.function)

class FunctionCallTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_functionCallNotEmpty(self):
        function = Function(["a", "b"], [Reference("a"), Reference("b")])
        definition = FunctionDefinition("func", function)
        call = FunctionCall(definition, [Number(2), Number(3)])
        self.assertIsInstance(call.evaluate(self.scope), Number)
        self.assertEqual(call.evaluate(self.scope).value, 3)
    def test_functionCallEmpty(self):
        function = Function(["a", "b"], [])
        definition = FunctionDefinition("func", function)
        call = FunctionCall(definition, [])
        call.evaluate(self.scope)


class ConditionalTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_iftrue_bothNotEmpty(self):
        cond = Conditional(Number(1), [Number(2), Number(3)], [Number(5)])
        self.assertEqual(cond.evaluate(self.scope).value, 3)
    def test_iffalse_bothNotEmpty(self):
        cond = Conditional(Number(0), [Number(2)], [Number(3), Number(5)])
        self.assertEqual(cond.evaluate(self.scope).value, 5)
    def test_iftrue_bothEmpty(self):
        Conditional(Number(1), [], []).evaluate(self.scope)
    def test_iffalse_bothEmpty(self):
        Conditional(Number(0), [], []).evaluate(self.scope)
    def test_iftrue_bothNone(self):
        Conditional(Number(1), None, None).evaluate(self.scope)
    def test_iffalse_bothNone(self):
        Conditional(Number(0), None, None).evaluate(self.scope)

class BinaryOperationTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_operations(self):
        a = Number(5)
        b = Number(2)
        c = Number(0)
        self.assertEqual(BinaryOperation(a, '+', b).evaluate(self.scope).value, 7)
        self.assertEqual(BinaryOperation(a, '-', b).evaluate(self.scope).value, 3)
        self.assertEqual(BinaryOperation(a, '*', b).evaluate(self.scope).value, 10)
        self.assertEqual(BinaryOperation(a, '/', b).evaluate(self.scope).value, 2)
        self.assertEqual(BinaryOperation(a, '%', b).evaluate(self.scope).value, 1)
        self.assertEqual(BinaryOperation(a, '==', b).evaluate(self.scope).value, 0)
        self.assertEqual(BinaryOperation(a, '!=', b).evaluate(self.scope).value, 1)
        self.assertEqual(BinaryOperation(a, '>', b).evaluate(self.scope).value, 1)
        self.assertEqual(BinaryOperation(a, '<', b).evaluate(self.scope).value, 0)
        self.assertEqual(BinaryOperation(a, '>=', b).evaluate(self.scope).value, 1)
        self.assertEqual(BinaryOperation(a, '<=', b).evaluate(self.scope).value, 0)
        self.assertEqual(BinaryOperation(a, '&&', c).evaluate(self.scope).value, 0)
        self.assertEqual(BinaryOperation(a, '||', c).evaluate(self.scope).value, 1)
        
class UnaryOperationTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_operations(self):
        a = Number(0)
        b = Number(1)
        c = Number(5)
        d = Number(-3)
        self.assertEqual(UnaryOperation('-', a).evaluate(self.scope).value, 0)
        self.assertEqual(UnaryOperation('-', b).evaluate(self.scope).value, -1)
        self.assertEqual(UnaryOperation('-', c).evaluate(self.scope).value, -5)
        self.assertEqual(UnaryOperation('-', d).evaluate(self.scope).value, 3)
        self.assertEqual(UnaryOperation('!', a).evaluate(self.scope).value, 1)
        self.assertEqual(UnaryOperation('!', b).evaluate(self.scope).value, 0)
        self.assertEqual(UnaryOperation('!', c).evaluate(self.scope).value, 0)
        self.assertEqual(UnaryOperation('!', d).evaluate(self.scope).value, 0)


class ReadTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        sys.stdin = io.StringIO(u'100500\n')
    def test_read(self):
        num = Read("a").evaluate(self.scope)
        self.assertIsInstance(num, Number)
        self.assertEqual(num.value, 100500)

if __name__ == '__main__':
    unittest.main()
