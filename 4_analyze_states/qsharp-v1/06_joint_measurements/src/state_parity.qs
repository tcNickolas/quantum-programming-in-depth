namespace AnalyzeStates {
  open Microsoft.Quantum.Measurement;

  operation StateParity(qs : Qubit[]) : Int {
    use parityQ = Qubit();
    for q in qs {
      CNOT(q, parityQ);
    }
    let res = MResetZ(parityQ);
    return res == Zero ? 0 | 1;
  }
}

namespace AnalyzeStates {
  open Microsoft.Quantum.Measurement;

  operation StateParityBuiltIn(qs : Qubit[]) : Int {
    let res = MeasureAllZ(qs);
    return res == Zero ? 0 | 1;
  }
}