operation ReadInformationInt(qs : Qubit[]) : Int {
  mutable res = 0;
  for k in Length(qs) - 1 .. -1 .. 0 {
    set res = res * 2 + (MResetZ(qs[k]) == One ? 1 | 0);
  }
  return res;
}

operation DistinguishStates(qs : Qubit[]) : Int {
  let res = ReadInformationInt(qs);
  return res < 4 ? res | 7 - res;
}
