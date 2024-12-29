import Std.Math.*;

operation PrepOneQubit(
  q : Qubit, alpha : Double, beta : Double
) : Unit is Adj + Ctl {
  let theta = 2.0 * ArcTan2(beta, alpha);
  Ry(theta, q);
}


operation PrepArbitrary(
  qs : Qubit[], 
  a : Double[]
) : Unit is Adj + Ctl {
  if Length(qs) == 1 {
    PrepOneQubit(qs[0], a[0], a[1]);
  } else {
    let N = Length(qs);
    let evenAmps = a[0 .. 2 ...];
    let oddAmps = a[1 .. 2 ...];

    let m0 = PNorm(2.0, evenAmps);
    let m1 = PNorm(2.0, oddAmps);

    PrepOneQubit(qs[N - 1], m0, m1);

    ApplyControlledOnInt(0, PrepArbitrary, [qs[N - 1]], (qs[... N - 2], evenAmps));

    ApplyControlledOnInt(1, PrepArbitrary, [qs[N - 1]], (qs[... N - 2], oddAmps));
  }
}
