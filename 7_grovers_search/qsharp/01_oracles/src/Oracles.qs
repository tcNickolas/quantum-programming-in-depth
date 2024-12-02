import Std.Arrays.Reversed;
import Std.Diagnostics.DumpMachine;

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

operation Main() : Unit {
  use x = Qubit[3];
  ApplyToEach(H, x);
  let markingOracle = MarkStates(_, _, [1, 6]);
  ApplyPhaseOracle(x, markingOracle);
  DumpMachine();
  ResetAll(x);
}
