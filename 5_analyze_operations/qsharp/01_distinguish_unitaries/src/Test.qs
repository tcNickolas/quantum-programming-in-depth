import Std.Diagnostics.Fact;
import Std.Math.PI;
import Std.Random.DrawRandomInt;

operation DistinguishTwoGatesTestLogic(
  gates : (Qubit => Unit is Adj+Ctl)[], 
  distinguisher : (Qubit => Unit is Adj+Ctl) => Int
) : Unit {
  for _ in 1 .. 100 {
    let gateInd = DrawRandomInt(0, 1);
    let resGate = distinguisher(gates[gateInd]);
    Fact(resGate == gateInd, 
      $"Expected state {gateInd}, got {resGate}");
  }
}

operation MinusX(q : Qubit) : Unit is Adj+Ctl {
  X(q);
  R(PauliI, 2. * PI(), q);
}
