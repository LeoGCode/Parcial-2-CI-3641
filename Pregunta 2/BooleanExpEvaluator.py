import networkx as nx
import matplotlib.pyplot as plt


class BooleanExpressions:
    operators = ["&", "|", "=>", "^"]
    precedence = {None: 4, "^": 3, "&": 2, "|": 2, "=>": 1}
    constants = ["true", "false", "t", "f", "1", "0"]
    i = 0
    labels = {}

    def __init__(self):
        evaluation_graph = nx.DiGraph()
        self.evaluation_graph = evaluation_graph

    def begin_program(self):
        print("\nWelcome to the Boolean Expressions Program!")

        while True:
            action = input("Enter an action: ")
            param = action.split(" ")
            first_param = param.pop(0).lower()

            if first_param == "eval" or first_param == "evaluate" or first_param == "evaluar" or first_param == "1":
                second_param = param.pop(0).lower()
                self.i = 0
                self.labels = {}
                evaluation_graph = nx.DiGraph()
                if second_param == "pre" or second_param == "1":
                    if not self.is_constant(param):
                        print(self.evaluate_pre(param, evaluation_graph))
                        self.evaluation_graph = evaluation_graph
                elif second_param == "post" or second_param == "2":
                    if not self.is_constant(param):
                        print(self.evaluate_post(param))
                        self.evaluation_graph = evaluation_graph
                else:
                    print("Invalid order of evaluation")
            elif first_param == "show" or first_param == "mostrar" or first_param == "2":
                second_param = param.pop(0).lower()
                if second_param == "pre" or second_param == "1":
                    self.show_pre(param)
                elif second_param == "post" or second_param == "2":
                    self.show_post(param)
                else:
                    print("Invalid order of evaluation")
            elif first_param == "display graph" or first_param == "mostrar grafo" or first_param == "3":
                nx.draw(self.evaluation_graph, labels=self.labels, with_labels=True)
                plt.show()

            elif first_param == "exit" or first_param == "salir" or first_param == "4":
                print("\nThank you for using the Boolean Expressions Program!")
                break
            else:
                print("Invalid action")

    def is_constant(self, param):
        if len(param) == 1:
            constant = param[0].lower()
            if constant == "true" or constant == "t" or constant == "1":
                print("True")
            elif constant == "false" or constant == "f" or constant == "0":
                print("False")
            else:
                print("Invalid constant")
                return False
            return True
        else:
            return False

    def evaluate_pre(self, param, evaluation_graph):
        operand = param.pop(0).lower()

        if operand in self.constants:
            print("Error: Constant " + operand + " is not a valid operand")
            return None
        elif operand in self.operators:
            self.i += 1
            father = self.i
            evaluation_graph.add_node(self.i)
            self.labels[self.i] = operand
        else:
            print("Invalid symbol")
            return None

        first_result = param[0].lower()
        if first_result in self.constants:
            param.pop(0)
            self.i += 1
            evaluation_graph.add_node(self.i)
            self.labels[self.i] = first_result

            evaluation_graph.add_edge(father, self.i)
            if first_result == "true" or first_result == "t" or first_result == "1":
                r1 = True
            elif first_result == "false" or first_result == "f" or first_result == "0":
                r1 = False
        else:
            evaluation_graph.add_edge(father, father + 1)
            r1 = self.evaluate_pre(param, evaluation_graph)

        if operand != "^":
            second_result = param[0].lower()
            if second_result in self.constants:
                param.pop(0)
                self.i += 1
                evaluation_graph.add_node(self.i)
                self.labels[self.i] = second_result
                evaluation_graph.add_edge(father, self.i)
                if second_result == "true" or second_result == "t" or second_result == "1":
                    r2 = True
                elif second_result == "false" or second_result == "f" or second_result == "0":
                    r2 = False
            else:
                evaluation_graph.add_edge(father, self.i + 1)
                r2 = self.evaluate_pre(param, evaluation_graph)
            if operand == "&":
                return r1 and r2
            elif operand == "|":
                return r1 or r2
            elif operand == "=>":
                return not r1 or r2
        else:
            return not r1

    def evaluate_post(self, param):
        stack = []
        while len(param) != 0:
            operand = param.pop(0).lower()
            if operand in self.constants:
                if operand == "true" or operand == "t" or operand == "1":
                    stack.append(True)
                elif operand == "false" or operand == "f" or operand == "0":
                    stack.append(False)
            elif operand in self.operators:
                r2 = stack.pop()
                if operand == "^":
                    stack.append(not r2)
                else:
                    r1 = stack.pop()
                    if operand == "&":
                        stack.append(r1 and r2)
                    elif operand == "|":
                        stack.append(r1 or r2)
                    elif operand == "=>":
                        stack.append(not r1 or r2)
            else:
                print("Invalid symbol")
                return None
        return stack[0]

    def show_pre(self, param) -> None:
        stack_operators = []
        stack_operands = []
        while param:
            operand = param.pop().lower()
            if operand in self.constants:
                if operand == "true" or operand == "t" or operand == "1":
                    stack_operands.append("True")
                    stack_operators.append(None)
                elif operand == "false" or operand == "f" or operand == "0":
                    stack_operands.append("False")
                    stack_operators.append(None)
            elif operand in self.operators:
                if operand == "^":
                    r1 = stack_operands.pop()
                    o1 = stack_operators.pop()
                    tmp = ""
                    if o1 is not None:
                        tmp += operand + " (" + r1 + ")"
                    else:
                        tmp += operand + " " + r1
                    stack_operands.append(tmp)
                    stack_operators.append(None)
                else:
                    r1 = stack_operands.pop()
                    r2 = stack_operands.pop()
                    if len(stack_operators) == 0:
                        stack_operands.append(r1 + " " + operand + " " + r2)
                    else:
                        o1 = stack_operators.pop()
                        o2 = stack_operators.pop()
                        tmp = ""
                        if self.precedence[o1] < self.precedence[operand]:
                            tmp += "(" + r1 + ") " + operand
                        else:
                            tmp += r1 + " " + operand
                        if self.precedence[o2] <= self.precedence[operand]:
                            tmp += " (" + r2 + ")"
                        else:
                            tmp += " " + r2
                        stack_operands.append(tmp)
                        stack_operators.append(operand)

            else:
                print("Invalid symbol")
                return None
        print(stack_operands[0])

    def show_post(self, param) -> None:
        stack_operators = []
        stack_operands = []
        while param:
            operand = param.pop(0).lower()
            if operand in self.constants:
                if operand == "true" or operand == "t" or operand == "1":
                    stack_operands.append("True")
                    stack_operators.append(None)
                elif operand == "false" or operand == "f" or operand == "0":
                    stack_operands.append("False")
                    stack_operators.append(None)
            elif operand in self.operators:
                if operand == "^":
                    r1 = stack_operands.pop()
                    o1 = stack_operators.pop()
                    tmp = ""
                    if o1 is not None:
                        tmp += operand + " (" + r1 + ")"
                    else:
                        tmp += operand + " " + r1
                    stack_operands.append(tmp)
                    stack_operators.append(None)
                else:
                    r2 = stack_operands.pop()
                    r1 = stack_operands.pop()
                    if len(stack_operators) == 0:
                        stack_operands.append(r1 + " " + operand + " " + r2)
                    else:
                        o2 = stack_operators.pop()
                        o1 = stack_operators.pop()
                        tmp = ""
                        if self.precedence[o1] < self.precedence[operand]:
                            tmp += "(" + r1 + ") " + operand
                        else:
                            tmp += r1 + " " + operand
                        if self.precedence[o2] <= self.precedence[operand]:
                            tmp += " (" + r2 + ")"
                        else:
                            tmp += " " + r2
                        stack_operands.append(tmp)
                        stack_operators.append(operand)

            else:
                print("Invalid symbol")
                return None
        print(stack_operands[0])
