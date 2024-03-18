namespace AnalyzeStates {
  open Microsoft.Quantum.Intrinsic;

  operation ReadInformationInt(qs : Qubit[]) : Int {
    mutable res = 0;
    for k in Length(qs) - 1 .. -1 .. 0 {
      set res = res * 2 + (M(qs[k]) == One ? 1 | 0);
    }
    return res;
  }

  operation DistinguishBellStates(qs : Qubit[]) : Int {
    CNOT(qs[0], qs[1]);
    H(qs[0]);
    let res = ReadInformationInt(qs);
    return res;
  }
}
