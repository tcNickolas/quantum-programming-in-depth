namespace AnalyzeUnitaries.Test {
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Unstable.StatePreparation;

  open AnalyzeUnitaries;

  // The set of gates and their eigenvectors to be used in testing.

  operation ZGate(qs : Qubit[]) : Unit is Adj + Ctl {
    Z(qs[0]);
  }

  operation TGate(qs : Qubit[]) : Unit is Adj + Ctl {
    T(qs[0]);
  }

  operation ZEigenvector(qs : Qubit[], ind : Int) : Unit is Adj {
    // Eigenvectors of the Z gate are |0> (+1) and |1> (-1)
    if ind == 1 {
      X(qs[0]);
    }
  }

  operation IncrementGate(qs : Qubit[]) : Unit is Adj + Ctl {
    CNOT(qs[1], qs[0]);
    X(qs[1]);
  }

  operation IncrementEigenvector(qs : Qubit[], ind : Int) : Unit is Adj {
    // Eigenvectors of the increment gate are more complicated
    let eigenAmps = [
      [(1., 0.), (1., 0.), (1., 0.), (1., 0.)],
      [(1., 0.), (-1., 0.), (1., 0.), (-1., 0.)],
      [(1., 0.), (0., -1.), (-1., 0.), (0., 1.)],
      [(1., 0.), (0., 1.), (-1., 0.), (0., -1.)]
    ];
    let cp = (a, b) -> ComplexAsComplexPolar(Complex(a, b));
    ApproximatelyPreparePureStateCP(0.0, Mapped(cp, eigenAmps[ind]), qs);
  }


  operation ValidateInputs() : Unit {
    // Check that all three sets of eigenvectors are indeed eigenvectors of the gates
    for (nQubits, nEigenstates, unitary, eigenstatePrep) in [
      (1, 2, ZGate, ZEigenvector),
      (2, 4, IncrementGate, IncrementEigenvector),
      (1, 2, TGate, ZEigenvector)
    ] {
      use qs = Qubit[nQubits];
      for ind in 0 .. nEigenstates - 1 {
        within {
            eigenstatePrep(qs, ind);
        } apply {
            unitary(qs);
        }
        if not CheckAllZero(qs) {
          fail "Not an eigenstate";
        }
      }
    }
  }
}