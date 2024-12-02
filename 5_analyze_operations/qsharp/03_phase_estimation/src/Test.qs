import Std.Arrays.Mapped;
import Std.Convert.ComplexAsComplexPolar;
import Std.Diagnostics.*;
import Std.Math.*;
import Microsoft.Quantum.Unstable.StatePreparation.ApproximatelyPreparePureStateCP;

import PhaseEstimation.*;

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


operation TestOneBitPhaseEstimation() : Unit {
  let eigenphases = [0.0, 0.5];
  for ind in 0 .. 1 {
    for _ in 0 .. 50 {
      let estimatedPhase = OneBitPhaseEstimation(
        1, ZEigenvector(_, ind), ZGate);
      Fact(AbsD(eigenphases[ind] - estimatedPhase) < 1e-5, 
        $"Expected phase {eigenphases[ind]}, got {estimatedPhase}");
    }
  }
}

operation TestIterativePhaseEstimation() : Unit {
  for (nQubits, unitary, unitaryStr, eigenstatePrep, eigenphases) in [
    (1, ZGate, "Z", ZEigenvector, [0.0, 0.5]),
    (2, IncrementGate, "INC", IncrementEigenvector, [0.0, 0.5, 0.25]),
    (1, TGate, "T", ZEigenvector, [0.0, 0.125])
  ] {
    Message($"Running IterativePhaseEstimation for {unitaryStr} gate");
    for ind in 0 .. Length(eigenphases) - 1 {
      for _ in 0 .. 10 {
        let estimatedPhase = IterativePhaseEstimation(
          nQubits, eigenstatePrep(_, ind), unitary);
        Fact(AbsD(eigenphases[ind] - estimatedPhase) < 1e-2, 
          $"Expected phase {eigenphases[ind]}, got {estimatedPhase}");
      }
    }
  }
}

operation TestAdaptivePhaseEstimation() : Unit {
  for (nQubits, unitary, unitaryStr, eigenstatePrep, eigenphases) in [
    (1, ZGate, "Z", ZEigenvector, [0.0, 0.5]),
    (2, IncrementGate, "INC", IncrementEigenvector, [0.0, 0.5, 0.25, 0.75])
  ] {
    Message($"Running AdaptivePhaseEstimation for {unitaryStr}");
    for ind in 0 .. Length(eigenphases) - 1 {
      for _ in 0 .. 10 {
        let estimatedPhase = TwoBitAdaptivePhaseEstimation(
          nQubits, eigenstatePrep(_, ind), unitary);
        Fact(AbsD(eigenphases[ind] - estimatedPhase) < 1e-2, 
          $"Expected phase {eigenphases[ind]}, got {estimatedPhase}");
      }
    }
  }
}

operation TestQuantumPhaseEstimation() : Unit {
  for (nQubits, unitary, unitaryStr, eigenstatePrep, eigenphases) in [
    (1, ZGate, "Z", ZEigenvector, [0.0, 0.5]),
    (2, IncrementGate, "INC", IncrementEigenvector, [0.0, 0.5, 0.25, 0.75])
  ] {
    Message($"Running QuantumPhaseEstimation for {unitaryStr}");
    for ind in 0 .. Length(eigenphases) - 1 {
      for _ in 0 .. 10 {
        let estimatedPhase = TwoBitQuantumPhaseEstimation(
          nQubits, eigenstatePrep(_, ind), unitary);
        Fact(AbsD(eigenphases[ind] - estimatedPhase) < 1e-2, 
          $"Expected phase {eigenphases[ind]}, got {estimatedPhase}");
      }
    }
  }
}