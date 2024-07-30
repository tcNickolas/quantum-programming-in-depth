namespace UnitaryImplementation.Test {
  open Microsoft.Quantum.Arithmetic;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Random;
  open Microsoft.Quantum.Synthesis;

  open UnitaryImplementation;

  operation ApplyUnitaryWrap(
    qs : Qubit[], u : Double[][]
  ) : Unit is Adj + Ctl {
    let doubleAsComplex = d -> Complex(d, 0.0);
    let doubleAAsComplexA = arr -> Mapped(doubleAsComplex, arr);
    let coefComplex = Mapped(doubleAAsComplexA, u);
    ApplyUnitary(coefComplex, LittleEndian(qs));
  }

  operation ValidateOneQubitUnitary(u : Double[][]) : Unit {
    Fact(Length(u) == 2, 
      "The matrix should be 2x2");
    for row in u {
      Fact(Length(row) == 2, "The matrix should be 2x2");
    }

    NearEqualityFactD(
      u[0][0] ^ 2. + u[1][0] ^ 2., 1.);
    NearEqualityFactD(
      u[0][1] ^ 2. + u[1][1] ^ 2., 1.);
    NearEqualityFactD(
      u[0][0] * u[0][1] + u[1][0] * u[1][1], 0.);
  }

  operation TestApplyOneQubit(u : Double[][]) : Unit {
    ValidateOneQubitUnitary(u);

    let testOp = ApplyOneQubit(_, u);
    let refOp = ApplyUnitaryWrap(_, u);
    AssertOperationsEqualReferenced(1, testOp, refOp);
  }

  @Test("QuantumSimulator")
  operation TestDiagAntiDiagOneQubit() : Unit {
    TestApplyOneQubit([[1., 0.], [0., 1.]]);
    TestApplyOneQubit([[1., 0.], [0., -1.]]);
    TestApplyOneQubit([[-1., 0.], [0., 1.]]);
    TestApplyOneQubit([[-1., 0.], [0., -1.]]);
    TestApplyOneQubit([[0., 1.], [1., 0.]]);
    TestApplyOneQubit([[0., 1.], [-1., 0.]]);
    TestApplyOneQubit([[0., -1.], [1., 0.]]);
    TestApplyOneQubit([[0., -1.], [-1., 0.]]);
  }

  operation RandomOneQubitUnitary() : Double[][] {
    let theta = DrawRandomDouble(0., 2. * PI());
    let sign = DrawRandomBool(0.5) ? +1. | -1.;
    return [[Cos(theta), sign * Sin(theta)], 
           [-Sin(theta), sign * Cos(theta)]];
  }

  @Test("QuantumSimulator")
  operation TestDenseOneQubit() : Unit {
    for _ in 1 .. 20 {
      TestApplyOneQubit(RandomOneQubitUnitary());
    }
  }
}