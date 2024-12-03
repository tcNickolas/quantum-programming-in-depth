import Std.Arrays.*;
import Std.ResourceEstimation.*;

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
    // BeginEstimateCaching allows to cache estimates for unchanging code fragments,
    // in this case for Grover's search iterations, to speed up resource estimation.
    if BeginEstimateCaching("Grover iteration", 0) {
      phaseOracle(qs);

      within {
        Adjoint prepareMeanOp(qs);
        ApplyToEachA(X, qs);
      } apply {
        Controlled Z(Rest(qs), qs[0]);
      }

      EndEstimateCaching();
    }
  }

  let meas = MResetEachZ(qs);
  return Mapped(m -> m == One, meas);
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
