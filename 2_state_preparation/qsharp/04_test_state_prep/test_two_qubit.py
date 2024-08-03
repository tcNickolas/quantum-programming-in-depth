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

  # Find global phase difference
  global_phase = -2
  for ind in range(len(a)):
    if abs(a[ind]) > 1E-9:
        global_phase = state[ind] / a[ind]
        break

  for ind in range(len(a)):
    if abs(a[ind]) > 1E-9:
      assert state[ind] == pytest.approx(a[ind] * global_phase)
    else:
      assert ind not in state
