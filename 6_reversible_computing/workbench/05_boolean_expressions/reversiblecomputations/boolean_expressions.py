from psiqworkbench import Qubits, Qubrick

def q_and(x: Qubits, y: Qubits):
    y.x(cond=x)

def q_or(x: Qubits, y: Qubits):
    y.x(cond=~x)
    y.x()


class EvaluateClause(Qubrick):
    'Qubrick that evaluates one SAT clause'
    def _compute(self, x: Qubits, y: Qubits, literals: list[tuple[int, bool]]) -> None:
        # Build a mask of control qubits for this clause
        ind, pos = literals[0]
        controls = x[ind] if pos else ~x[ind]
        for ind, pos in literals[1:]:
            controls |= x[ind] if pos else ~x[ind]

        # Calculate OR of the literals in the clause
        q_or(controls, y)


class EvaluateFormula(Qubrick):
    'Qubrick that evaluates a SAT formula'
    def _compute(self, x: Qubits, y: Qubits, clauses: list[list[tuple[int, bool]]]) -> None:
        num_clauses = len(clauses)
        # Allocate auxiliary qubits for clause evaluation
        a = self.alloc_temp_qreg(num_clauses, "a", release_after_compute=True)

        clause_evaluator = EvaluateClause()

        # Evaluate clauses and store results in corresponding auxiliary qubits
        for ind, clause in enumerate(clauses):
            clause_evaluator.compute(x, a[ind], clause)

        # Evaluate the formula as the AND of auxiliary qubits
        q_and(a, y)

        # Uncompute clauses evaluation
        for _ in range(num_clauses):
            clause_evaluator.uncompute()
        