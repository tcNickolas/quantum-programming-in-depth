namespace AnalyzeUnitaries {
  open Microsoft.Quantum.Intrinsic;

  operation DistinguishXZ(gate : Qubit => Unit is Adj+Ctl) : Int {
    use q = Qubit();
    gate(q);
    return M(q) == One ? 0 | 1;
  }

  operation DistinguishXH(gate : Qubit => Unit is Adj+Ctl) : Int {
    use q = Qubit();
    // HXH = Z, XXX = X
    gate(q);
    X(q);
    gate(q);
    return M(q) == One ? 0 | 1;
  }

  operation DistinguishXMinusX(gate : Qubit => Unit is Adj+Ctl) : Int {
    use qs = Qubit[2];
    H(qs[0]);
    H(qs[1]);
    Controlled gate([qs[0]], qs[1]);
    // If this was X, we're now in (|0> + |1>)(|0> + |1>), otherwise (|0> - |1>)(|0> + |1>)
    H(qs[0]);
    H(qs[1]);
    return M(qs[0]) == Zero ? 0 | 1;
  }
}
