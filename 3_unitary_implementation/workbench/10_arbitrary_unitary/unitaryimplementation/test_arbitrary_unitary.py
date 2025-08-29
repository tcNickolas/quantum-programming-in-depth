from numpy import identity, matmul
from numpy.linalg import qr
from numpy.random import default_rng
from psiqworkbench import QPU, Qubits
from .arbitrary_unitary import ApplyArbitraryUnitary
import pytest

def run_test_arbitrary_unitary(n, u):
    qpu = QPU(num_qubits=n, filters=">>unitary>>")
    reg = Qubits(n, "reg", qpu)

    apply_unitary = ApplyArbitraryUnitary()
    apply_unitary.compute(reg, u)

    ufilter = qpu.get_filter_by_name('>>unitary>>')
    matrix = ufilter.get()

    for actual, expected in zip(matrix, u):
        assert actual == pytest.approx(expected)


def test_apply_arbitrary_unitary():
    rng = default_rng()
    for n in range(1, 6):
        for _ in range(50):
            t = rng.standard_normal((2**n, 2**n))
            u, _ = qr(t)
            # Double-check that u is unitary
            assert matmul(u, u.transpose()) == pytest.approx(identity(2**n))
            run_test_arbitrary_unitary(n, u)