namespace AnalyzeUnitaries.Test {
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;

  open AnalyzeUnitaries;

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
}