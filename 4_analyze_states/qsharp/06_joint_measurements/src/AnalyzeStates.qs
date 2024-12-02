operation StateParity(qs : Qubit[]) : Int {
  use parityQ = Qubit();
  for q in qs {
    CNOT(q, parityQ);
  }
  return MResetZ(parityQ) == Zero ? 0 | 1;
}

operation StateParityBuiltIn(qs : Qubit[]) : Int {
  return MeasureAllZ(qs) == Zero ? 0 | 1;
}
