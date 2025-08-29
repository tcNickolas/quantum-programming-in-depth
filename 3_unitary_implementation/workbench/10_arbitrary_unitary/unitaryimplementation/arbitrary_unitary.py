from math import atan2, isclose
from scipy.linalg import cossin
from psiqworkbench import Qubits, Qubrick, Units

class ApplyArbitraryUnitary(Qubrick):
    '''Apply an arbitrary unitary given by its real-valued matrix'''
    def __init__(self, name=None, **kwargs):
        super().__init__(name, never_uncompute=True, allow_multi_qubit_ctrl=True, **kwargs)

    @classmethod
    def _extract_blocks(cls, matrix: list[list[float]]):
        block_len = len(matrix) // 2
        a = [row[0 : block_len] for row in matrix[0 : block_len]]
        b = [row[block_len : ] for row in matrix[block_len : ]]
        return a, b
    
    def _apply_one_qubit(self, reg: Qubits, u: list[list[float]], ctrl: Qubits=0) -> None:
        if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
            reg.z(cond=ctrl)
        theta = atan2(u[1][0], u[0][0])
        reg.ry(2 * theta * Units.rad, cond=ctrl)
    
    def _apply_block_diagonal(self, reg: Qubits, a: list[list[float]], b: list[list[float]], ctrl: Qubits=0) -> None:
        self._compute(reg[:-1], b, ctrl=reg[-1] | ctrl)
        self._compute(reg[:-1], a, ctrl=~reg[-1] | ctrl)

    def _apply_cs_matrix(self, reg: Qubits, cs: list[tuple[float, float]], ctrl: Qubits=0) -> None:
        for (k, (c, s)) in enumerate(cs):
            m = [[c, -s], [s, c]]
            with reg[:-1] == k as cond:
                self._apply_one_qubit(reg[-1], m, ctrl=ctrl | cond)
    
    def _compute(self, reg: Qubits, u: list[list[float]], ctrl: Qubits=0) -> None:
        n = reg.num_qubits
        if n == 1:
            self._apply_one_qubit(reg, u, ctrl=ctrl)
            return
        
        # Get the cosine-sine decomposition.
        left, cs, right = cossin(u, p=len(u) / 2, q=len(u) / 2) 

        # Apply right - a two-block-diagonal unitary.
        ar, br = self._extract_blocks(right)
        self._apply_block_diagonal(reg, ar, br, ctrl=ctrl)

        # Apply cs - an arbitrary cs matrix.
        cs_pairs = []
        for i in range(len(cs) // 2):
            cs_pairs += [(cs[i][i], cs[i + len(cs) // 2][i])]
        self._apply_cs_matrix(reg, cs_pairs, ctrl=ctrl)

        # Apply left - a two-block-diagonal unitary.
        al, bl = self._extract_blocks(left)
        self._apply_block_diagonal(reg, al, bl, ctrl=ctrl)
