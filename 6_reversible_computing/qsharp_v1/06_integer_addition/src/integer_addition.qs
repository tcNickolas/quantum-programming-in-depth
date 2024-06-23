namespace ReversibleComputing {
  open Microsoft.Quantum.Arrays;

  // Can be used to compute sum of two or three (with carry) bits
  operation SumModTwo(x : Qubit[], sum : Qubit) : Unit is Adj + Ctl {
    for q in x {
      CNOT(q, sum);
    }
  }

  // Can be used to compute carry of two or three (with carry) bits
  operation Carry(x : Qubit[], carry : Qubit) : Unit is Adj + Ctl {
    for i in 0 .. Length(x) - 2 {
      for j in i + 1 .. Length(x) - 1 {
        CCNOT(x[i], x[j], carry);
      }
    }
  }

  // Use big endian to store numbers
  operation Adder(x : Qubit[], y : Qubit[], sum : Qubit[]) : Unit is Adj + Ctl {
    let n = Length(x);
    if n == 1 {
      // No need for carry
      SumModTwo(x + y, sum[0]);
    } else {
      use carryBits = Qubit[n - 1];
      within {
        // Compute carry bits first
        Carry([x[n - 1], y[n - 1]], carryBits[n - 2]);
        for i in n - 2 .. -1 .. 1 {
          Carry([x[i], y[i], carryBits[i]], carryBits[i - 1]);
        }
      } apply {
        // Compute sum bits
        SumModTwo([x[n - 1], y[n - 1]], sum[n - 1]);
        for i in n - 2 .. -1 .. 0 {
          SumModTwo([x[i], y[i], carryBits[i]], sum[i]);
        }
      }
    }
  }
}
