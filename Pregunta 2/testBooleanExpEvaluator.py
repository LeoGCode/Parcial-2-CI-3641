import unittest
import networkx as nx
from unittest.mock import patch
from BooleanExpEvaluator import BooleanExpressions


class MyTestCase(unittest.TestCase):

    def test_is_const_correct(self):
        be = BooleanExpressions()
        self.assertTrue(be.is_constant(["True"]))
        self.assertTrue(be.is_constant(["False"]))
        self.assertTrue(be.is_constant(["t"]))
        self.assertTrue(be.is_constant(["f"]))
        self.assertTrue(be.is_constant(["1"]))
        self.assertTrue(be.is_constant(["0"]))

    def test_is_const_incorrect(self):
        be = BooleanExpressions()
        self.assertFalse(be.is_constant(["a"]))
        self.assertFalse(be.is_constant(["b","a"]))

    def test_eval_pre(self):
        be = BooleanExpressions()
        evaluation_graph = nx.DiGraph()
        self.assertTrue(be.evaluate_pre("| & => true true false true".split(" "), evaluation_graph))

    def test_eval_post(self):
        be = BooleanExpressions()
        self.assertFalse(be.evaluate_post("true false => false | true false ^ | &".split(" ")))

    @patch('builtins.print')
    def test_show_pre(self, mock_print):
        be = BooleanExpressions()
        be.show_pre("| & => true true false true".split(" "))
        mock_print.assert_called_with("(True => True) & False | True")

    @patch('builtins.print')
    def test_show_post(self, mock_print):
        be = BooleanExpressions()
        be.show_post("true false => false | true false ^ | &".split(" "))
        mock_print.assert_called_with("(True => False) | False & (True | ^ False)")

    def test_begin_program(self):
        be = BooleanExpressions()
        test_cases_correct = ["EVAL PRE | & => true true false true",
                              "EVAL POST true false => false | true false ^ | &",
                              "MOSTRAR PRE | & => true true false true",
                              "MOSTRAR POST true false => false | true false ^ | &",
                              "SALIR"]

        with patch('builtins.input', side_effect=test_cases_correct):
            be.begin_program()
            self.assertEqual(be.operators, ["&", "|", "=>", "^"])
            self.assertEqual(be.precedence, {None: 4, "^": 3, "&": 2, "|": 2, "=>": 1})
            self.assertEqual(be.constants, ["true", "false", "t", "f", "1", "0"])




if __name__ == '__main__':
    unittest.main()
