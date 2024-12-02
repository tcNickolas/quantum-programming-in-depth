import Std.Arrays.*;

operation RunGroversSearch(
  nBits : Int,
  markingOracle : (Qubit[], Qubit) => Unit, 
  prepareMeanOp : Qubit[] => Unit is Adj,
  nIterations : Int
) : Bool[] {
  let phaseOracle = ApplyPhaseOracle(_, markingOracle);

  use qs = Qubit[nBits];
  prepareMeanOp(qs);

  for _ in 1 .. nIterations {
    phaseOracle(qs);

    within {
      Adjoint prepareMeanOp(qs);
      ApplyToEachA(X, qs);
    } apply {
      Controlled Z(qs[1...], qs[0]);
    }
  }

  let meas = MResetEachZ(qs);
  return Mapped(m -> m == One, meas);
}


operation MarkStates(x : Qubit[], y : Qubit, markedStates : Int[]) : Unit {
  for state in markedStates {
    // Use integers in big endian
    ApplyControlledOnInt(state, X, Reversed(x), y);
  }
}


operation ApplyPhaseOracle(x : Qubit[], markingOracle : (Qubit[], Qubit) => Unit) : Unit {
  use aux = Qubit();
  within {
    H(aux);
    Z(aux);
  } apply {
    markingOracle(x, aux);
  }
}
