namespace AnalyzeUnitaries.Test {
  open Microsoft.Quantum.Arithmetic;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Preparation;

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
    CNOT(qs[0], qs[1]);
    X(qs[0]);
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
    PrepareArbitraryStateCP(Mapped(cp, eigenAmps[ind]), LittleEndian(qs));
  }

  @Test("QuantumSimulator")
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
        AssertAllZero(qs);
      }
    }
  }
}