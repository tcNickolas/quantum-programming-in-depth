namespace AnalyzeStates {
  open Microsoft.Quantum.Intrinsic;

  operation ReadInformation(qs : Qubit[]) : Result[] {
    mutable res = [];
    for q in qs {
      set res += [M(q)];
    }
    return res;
  }
}
