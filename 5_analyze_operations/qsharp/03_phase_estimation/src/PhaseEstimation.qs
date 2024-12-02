import Std.Convert.*;
import Std.Math.*;

operation OneBitPhaseEstimation(
  n : Int,
  eigenstatePrep : Qubit[] => Unit, 
  unitary : Qubit[] => Unit is Ctl
) : Double {
  use (phase, eigenstate) = (Qubit(), Qubit[n]);
  H(phase);
  eigenstatePrep(eigenstate);
  Controlled unitary([phase], eigenstate);
  ResetAll(eigenstate);
  H(phase);
  return MResetZ(phase) == Zero ? 0.0 | 0.5;
}


operation IterativePhaseEstimation(
  n : Int,
  eigenstatePrep : Qubit[] => Unit, 
  unitary : Qubit[] => Unit is Ctl
) : Double {
  use (phase, eigenstate) = (Qubit(), Qubit[n]);
  eigenstatePrep(eigenstate);
  let nTrials = 10000;
  mutable nZeros = 0;
  for _ in 1 .. nTrials {
    H(phase);
    Controlled unitary([phase], eigenstate);
    H(phase);
    set nZeros += MResetZ(phase) == Zero ? 1 | 0;
  }
  ResetAll(eigenstate);
  return ArcCos(Sqrt(IntAsDouble(nZeros) / IntAsDouble(nTrials))) / PI();
}


operation TwoBitAdaptivePhaseEstimation(
  n : Int,
  eigenstatePrep : Qubit[] => Unit, 
  unitary : Qubit[] => Unit is Ctl
) : Double {
  use (phase, eigenstate) = (Qubit(), Qubit[n]);
  mutable res_bits = [Zero, Zero];
  // Estimate the least significant bit
  H(phase);
  eigenstatePrep(eigenstate);
  Controlled unitary([phase], eigenstate);
  Controlled unitary([phase], eigenstate);
  H(phase);
  set res_bits w/= 0 <- MResetZ(phase);
  // Estimate the most significant bit
  H(phase);
  Controlled unitary([phase], eigenstate);
  if res_bits[0] == One {
    Adjoint S(phase);
  }
  H(phase);
  set res_bits w/= 1 <- MResetZ(phase);
  ResetAll(eigenstate);
  return IntAsDouble(ResultArrayAsInt(res_bits)) / 4.0;
}


operation TwoBitQuantumPhaseEstimation(
  n : Int,
  eigenstatePrep : Qubit[] => Unit, 
  unitary : Qubit[] => Unit is Ctl
) : Double {
  use (phase, eigenstate) = (Qubit[2], Qubit[n]);
  ApplyToEach(H, phase);
  eigenstatePrep(eigenstate);
  Controlled unitary([phase[1]], eigenstate);
  Controlled unitary([phase[0]], eigenstate);
  Controlled unitary([phase[0]], eigenstate);
  ResetAll(eigenstate);
  // Inverse QFT for 2 bits
  SWAP(phase[0], phase[1]);
  H(phase[1]);
  Controlled Adjoint S([phase[1]], phase[0]);
  H(phase[0]);
  let res = (MResetZ(phase[0]) == One ? 2 | 0) + 
            (MResetZ(phase[1]) == One ? 1 | 0);
  return IntAsDouble(res) / 4.0;
}
