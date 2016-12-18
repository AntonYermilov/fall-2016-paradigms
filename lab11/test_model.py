import sys
import unittest
from unittest.mock import patch
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
        with patch('sys.stdout', new_callable = io.StringIO) as mock_stdout:
            Print(self.scope["a"]).evaluate(self.scope)
            self.assertEqual(mock_stdout.getvalue(), '2\n')
            self.assertEqual(self.scope["a"].evaluate(self.scope), self.scope["a"])
        
class ReferenceTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_reference(self):
        with patch('sys.stdout', new_callable = io.StringIO) as mock_stdout: 
            self.scope["a"] = Number(100500)
            self.assertIsInstance(Reference("a").evaluate(self.scope), Number)
            Print(self.scope["a"]).evaluate(self.scope)
            self.assertEqual(mock_stdout.getvalue(), '100500\n')

class FunctionTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        self.scope["func1"] = Function(["a", "b", "c"], [Number(5), Number(3), Number(2)])
        self.scope["func2"] = Function(["arg"], [])
    def test_instances(self):
        self.assertIsInstance(self.scope["func1"].evaluate(self.scope), Number)
    def test_results(self):
        with patch('sys.stdout', new_callable = io.StringIO) as mock_stdout:
            Print(self.scope["func1"].evaluate(self.scope)).evaluate(self.scope)
            self.assertEqual(mock_stdout.getvalue(), '2\n')
    
class FunctionDefinitionTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        self.function = Function(["arg"], [Number(1), Number(2)])
        self.definition = FunctionDefinition("func", self.function)
    def test_functionDefinition(self):
        self.assertIsInstance(self.definition.evaluate(self.scope), Function)
        self.assertIsInstance(self.scope["func"], Function)
        self.assertEqual(self.scope["func"], self.function)

class FunctionCallTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_functionCallNotEmpty(self):
        with patch('sys.stdout', new_callable = io.StringIO) as mock_stdout: 
            function = Function(["a", "b"], [Reference("a"), Reference("b")])
            definition = FunctionDefinition("func", function)
            call = FunctionCall(definition, [Number(2), Number(3)])
            self.assertIsInstance(call.evaluate(self.scope), Number)
            Print(call.evaluate(self.scope)).evaluate(self.scope)
            self.assertEqual(mock_stdout.getvalue(), '3\n')
    def test_functionCallEmpty(self):
        function = Function(["a", "b"], [])
        definition = FunctionDefinition("func", function)
        call = FunctionCall(definition, [Number(2), Number(3)])
        call.evaluate(self.scope)


class ConditionalTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_iftrue_bothNotEmpty(self):
        with patch('sys.stdout', new_callable = io.StringIO) as mock_stdout:
            cond = Conditional(Number(1), [Number(2), Number(3)], [Number(5)])
            Print(cond.evaluate(self.scope)).evaluate(self.scope)
            self.assertEqual(mock_stdout.getvalue(), '3\n')
    def test_iffalse_bothNotEmpty(self):
        with patch('sys.stdout', new_callable = io.StringIO) as mock_stdout:
            cond = Conditional(Number(0), [Number(2)], [Number(3), Number(5)])
            Print(cond.evaluate(self.scope)).evaluate(self.scope)
            self.assertEqual(mock_stdout.getvalue(), '5\n')
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
        for lhs in range(-10, 10):
            for rhs in range(-10, 10):
                for op in ['+', '-', '*', '/', '%', '==', '!=', '>', '<', '>=', '<=', '&&', '||']:
                    if rhs == 0 and (op == '/' or op == '%'):
                        continue
                    with patch('sys.stdout', new_callable = io.StringIO) as mock_stdout:
                        res = BinaryOperation(Number(lhs), op, Number(rhs)).evaluate(self.scope)
                        Print(res).evaluate(self.scope)
                        if op == '+':
                            self.assertEqual(int(mock_stdout.getvalue()), lhs + rhs)
                        if op == '-':
                            self.assertEqual(int(mock_stdout.getvalue()), lhs - rhs)
                        if op == '*':
                            self.assertEqual(int(mock_stdout.getvalue()), lhs * rhs)
                        if op == '/':
                            self.assertEqual(int(mock_stdout.getvalue()), lhs // rhs)
                        if op == '%':
                            self.assertEqual(int(mock_stdout.getvalue()), lhs % rhs)
                        if op == '==':
                            self.assertEqual(int(mock_stdout.getvalue()) != 0, lhs == rhs)
                        if op == '!=':
                            self.assertEqual(int(mock_stdout.getvalue()) != 0, lhs != rhs)
                        if op == '>':
                            self.assertEqual(int(mock_stdout.getvalue()) != 0, lhs > rhs)
                        if op == '<':
                            self.assertEqual(int(mock_stdout.getvalue()) != 0, lhs < rhs)
                        if op == '>=':
                            self.assertEqual(int(mock_stdout.getvalue()) != 0, lhs >= rhs)
                        if op == '<=':
                            self.assertEqual(int(mock_stdout.getvalue()) != 0, lhs <= rhs)
                        if op == '&&':
                            self.assertEqual(int(mock_stdout.getvalue()) != 0, lhs != 0 and rhs != 0)
                        if op == '||':
                            self.assertEqual(int(mock_stdout.getvalue()) != 0, lhs != 0 or rhs != 0)
        
class UnaryOperationTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_operations(self):
        for val in range(-10, 10):
            for op in ['-', '!']:
                with patch('sys.stdout', new_callable = io.StringIO) as mock_stdout:
                    res = UnaryOperation(op, Number(val)).evaluate(self.scope)
                    Print(res).evaluate(self.scope)
                    if op == '-':
                        self.assertEqual(int(mock_stdout.getvalue()), -val)
                    if op == '!':
                        self.assertEqual(int(mock_stdout.getvalue()) != 0, not val)
            
class ReadTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_read(self):
        with patch('sys.stdin', new = io.StringIO('100500\n')), patch('sys.stdout', new_callable = io.StringIO) as mock_stdout:
            num = Read('a').evaluate(self.scope)
            self.assertIsInstance(num, Number)
            self.assertEqual(num, self.scope['a'])
            Print(num).evaluate(self.scope)
            self.assertEqual(mock_stdout.getvalue(), '100500\n')

class PrintTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    def test_print(self):
        with patch('sys.stdout', new_callable = io.StringIO) as mock_stdout:
            Print(Number(5)).evaluate(self.scope)
            self.assertEqual(mock_stdout.getvalue(), '5\n')

if __name__ == '__main__':
    unittest.main()
