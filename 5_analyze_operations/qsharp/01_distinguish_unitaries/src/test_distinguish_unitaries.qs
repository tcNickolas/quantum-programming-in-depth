namespace AnalyzeUnitaries.Test {
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Random;
  open AnalyzeUnitaries;

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
}