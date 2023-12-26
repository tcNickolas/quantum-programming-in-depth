namespace AnalyzeStates {
  open Microsoft.Quantum.Measurement;

  operation StateParity(qs : Qubit[]) : Int {
    let res = MeasureAllZ(qs);
    return res == Zero ? 0 | 1;
  }
}
