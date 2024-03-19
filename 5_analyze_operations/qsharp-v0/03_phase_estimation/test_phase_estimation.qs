namespace AnalyzeUnitaries.Test {
  open Microsoft.Quantum.Arithmetic;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Preparation;

  open AnalyzeUnitaries;

  @Test("QuantumSimulator")
  operation TestOneBitPhaseEstimation() : Unit {
    let eigenphases = [0.0, 0.5];
    for ind in 0 .. 1 {
      for _ in 0 .. 50 {
        let estimatedPhase = OneBitPhaseEstimation(
          1, ZEigenvector(_, ind), ZGate);
        Fact(AbsD(eigenphases[ind] - estimatedPhase) < 1E-5, 
          $"Expected phase {eigenphases[ind]}, got {estimatedPhase}");
      }
    }
  }

  @Test("QuantumSimulator")
  operation TestIterativePhaseEstimation() : Unit {
    for (nQubits, unitary, eigenstatePrep, eigenphases) in [
      (1, ZGate, ZEigenvector, [0.0, 0.5]),
      (2, IncrementGate, IncrementEigenvector, [0.0, 0.5, 0.25]),
      (1, TGate, ZEigenvector, [0.0, 0.125])
    ] {
      Message($"Running IterativePhaseEstimation for {unitary}");
      for ind in 0 .. Length(eigenphases) - 1 {
        for _ in 0 .. 10 {
          let estimatedPhase = IterativePhaseEstimation(
            nQubits, eigenstatePrep(_, ind), unitary);
          Fact(AbsD(eigenphases[ind] - estimatedPhase) < 1E-2, 
            $"Expected phase {eigenphases[ind]}, got {estimatedPhase}");
        }
      }
    }
  }

  @Test("QuantumSimulator")
  operation TestAdaptivePhaseEstimation() : Unit {
    for (nQubits, unitary, eigenstatePrep, eigenphases) in [
      (1, ZGate, ZEigenvector, [0.0, 0.5]),
      (2, IncrementGate, IncrementEigenvector, [0.0, 0.5, 0.25, 0.75])
    ] {
      Message($"Running AdaptivePhaseEstimation for {unitary}");
      for ind in 0 .. Length(eigenphases) - 1 {
        for _ in 0 .. 10 {
          let estimatedPhase = TwoBitAdaptivePhaseEstimation(
            nQubits, eigenstatePrep(_, ind), unitary);
          Fact(AbsD(eigenphases[ind] - estimatedPhase) < 1E-2, 
            $"Expected phase {eigenphases[ind]}, got {estimatedPhase}");
        }
      }
    }
  }

  @Test("QuantumSimulator")
  operation TestQuantumPhaseEstimation() : Unit {
    for (nQubits, unitary, eigenstatePrep, eigenphases) in [
      (1, ZGate, ZEigenvector, [0.0, 0.5]),
      (2, IncrementGate, IncrementEigenvector, [0.0, 0.5, 0.25, 0.75])
    ] {
      Message($"Running QuantumPhaseEstimation for {unitary}");
      for ind in 0 .. Length(eigenphases) - 1 {
        for _ in 0 .. 10 {
          let estimatedPhase = TwoBitQuantumPhaseEstimation(
            nQubits, eigenstatePrep(_, ind), unitary);
          Fact(AbsD(eigenphases[ind] - estimatedPhase) < 1E-2, 
            $"Expected phase {eigenphases[ind]}, got {estimatedPhase}");
        }
      }
    }
  }
}