namespace ReversibleComputing {
  operation OracleZero(x : Qubit, y : Qubit) : Unit is Adj + Ctl {
    // Do nothing.
  }

  operation OracleOne(x : Qubit, y : Qubit) : Unit is Adj + Ctl {
    X(y);
  }

  operation OracleX(x : Qubit, y : Qubit) : Unit is Adj + Ctl {
    CNOT(x, y);
  }
}
