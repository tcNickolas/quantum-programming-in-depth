operation Negation(x : Qubit[], y : Qubit) : Unit is Adj + Ctl {
  CNOT(x[0], y);
  X(y);
}

operation Xor(x : Qubit[], y : Qubit) : Unit is Adj + Ctl {
  CNOT(x[0], y);
  CNOT(x[1], y);
}

operation And(x : Qubit[], y : Qubit) : Unit is Adj + Ctl {
  CCNOT(x[0], x[1], y);
}

operation Or(x : Qubit[], y : Qubit) : Unit is Adj + Ctl {
  ApplyControlledOnInt(0, X, x, y);
  X(y);
}

operation Equality(x : Qubit[], y : Qubit) : Unit is Adj + Ctl {
  CNOT(x[0], y);
  CNOT(x[1], y);
  X(y);
}

operation MultiAnd(x : Qubit[], y : Qubit) : Unit is Adj + Ctl {
  Controlled X(x, y);
}

operation MultiOr(x : Qubit[], y : Qubit) : Unit is Adj + Ctl {
  ApplyControlledOnInt(0, X, x, y);
  X(y);
}
