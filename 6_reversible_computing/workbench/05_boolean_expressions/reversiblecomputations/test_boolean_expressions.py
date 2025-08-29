from functools import partial
from psiqworkbench import QPU, Qubits
from .boolean_expressions import *

def run_test_reversible(n_inputs: int, n_qubits: int, quantum_op: callable, f: callable):
    qpu = QPU(filters=['>>bit-qpu>>'])
    for input in range(2 ** n_inputs):
        qpu.reset(n_qubits)
        x = Qubits(n_inputs, "x", qpu)
        y = Qubits(1, "y", qpu)
        if input > 0:
            x.x(input)

        quantum_op(x, y)
       
        input_str = (f"{{:0>{n_inputs}b}}").format(input)
        input_le = [input_str[i] == '1' for i in range(n_inputs)][::-1]
        res_expected = f(input_le)

        res_x = x.read()
        res_y = y.read()

        if res_x != input:
            raise Exception(f"Error for x={input}: the state of the input qubit changed")
        if res_y != res_expected:
            raise Exception(f"Error for x={input}: expected {res_expected}, got {res_y}")                


def f_evaluate_clause(args: list[bool], literals: list[tuple[int, bool]]) -> bool:
    '''A classical function that evaluates one SAT clause.
    Each literal is a tuple of an int (the index of the variable) 
    and a bool (true if the variable is included as itself, false if it's included as a negation)'''
    for (ind, pos) in literals:
        if pos and args[ind] or not pos and not args[ind]:
            return True
    return False


def test_evaluate_clause():
    clause_evaluator = EvaluateClause()
    for num_inputs, clause in [
            (1, [(0, True)]),
            (1, [(0, False)]),
            (2, [(0, True), (1, True)]),
            (2, [(0, False), (1, True)]),
            (3, [(1, False), (2, False)])
        ]:
        f = partial(f_evaluate_clause, literals=clause)
        quantum_op = partial(clause_evaluator.compute, literals=clause)
        run_test_reversible(num_inputs, num_inputs + 1, quantum_op, f)


def f_evaluate_formula(args: list[bool], clauses: list[list[tuple[int, bool]]]) -> bool:
    '''A classical function that evaluates a SAT formula.'''
    for clause in clauses:
        if not f_evaluate_clause(args, clause):
            return False
    return True


def test_evaluate_formula():
    formula_evaluator = EvaluateFormula()
    for num_inputs, clauses in [
            (1, [[(0, True)], [(0, False)]]), # 0 solutions
            (1, [[(0, False)]]),              # 1 solution
            (2, [[(0, True)], [(1, True)]]),  # 1 solution
            (2, [[(0, False), (1, False)], [(0, True), (1, True)]]), # 2 solutions
            (2, [[(0, False), (1, False)]]),  # 3 solutions
            (3, [[(2, False), (1, True)], [(2, True), (1, False)]]), # 4 solutions
        ]:
        f = partial(f_evaluate_formula, clauses=clauses)
        quantum_op = partial(formula_evaluator.compute, clauses=clauses)
        run_test_reversible(num_inputs, num_inputs + len(clauses) + 1, quantum_op, f)