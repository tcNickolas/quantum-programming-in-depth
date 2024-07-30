namespace GroversSearch {
  open Microsoft.Quantum.Arrays;

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
}
