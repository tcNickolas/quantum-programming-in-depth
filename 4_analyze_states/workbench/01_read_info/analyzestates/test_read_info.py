from random import randint
from psiqworkbench import QPU, Qubits
from .read_info import read_info

def run_test_read_info(n: int, basis_state: int) -> None:
    qpu = QPU()
    for _ in range(100):
        qpu.reset(n)
        reg = Qubits(n, "reg", qpu)

        reg.write(basis_state)

        res = read_info(reg)
        assert res == basis_state


def test_read_info():
    for _ in range(1, 20):
        n = randint(1, 5)
        num = randint(0, 2 ** n - 1)
        run_test_read_info(n, num)