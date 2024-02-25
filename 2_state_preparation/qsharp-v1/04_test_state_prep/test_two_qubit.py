import pytest
import qsharp
from math import sqrt

@pytest.mark.parametrize("a",
    [ [1., 0., 0., 0.],
      [0., 1., 0., 0.],
      [0., 0., 1., 0.],
      [0., 0., 0., 1.],
      [0.5, 0.5, 0.5, 0.5],
      [-0.5, 0.5, 0.5, -0.5],
      [0.5, -0.5, 0.5, 0.5],
      [0.5, 0.5, -0.5, 0.5],
      [0.5, 0.5, 0.5, -0.5],
      [1. / sqrt(2.), 0., 0., 1. / sqrt(2.)],
      [1. / sqrt(2.), 0., 0., -1. / sqrt(2.)],
      [0., 1. / sqrt(2.), 1. / sqrt(2.), 0.],
      [0., 1. / sqrt(2.), -1. / sqrt(2.), 0.],
      [0.36, 0.48, 0.64, -0.48],
      [1. / sqrt(3.), -1. / sqrt(3.), 1. / sqrt(3.), 0.]
    ])
def test_prep_two_qubit(a):
  qsharp.init(project_root='.')
  qsharp.eval(f"use qs = Qubit[2]; StatePreparation.PrepTwoQubits(qs, {a});")
  state = qsharp.dump_machine()
  first_ind = -1
  first_amp_cp = 0
  for ind in range(4):
    if abs(a[ind]) > 1E-9:
      (real, imag) = state[ind]
      if first_ind == -1:
        first_ind = ind
        first_amp_cp = complex(real, imag)
      assert complex(real, imag) / first_amp_cp == pytest.approx(a[ind] / a[first_ind])
