import Std.Convert.IntAsDouble;
import Std.Math.*;
import GroversSearch.*;
import NQueens.*;

operation Main() : Bool[] {
  let nRows = 10;
  let nBits = nRows ^ 2;
  let M = 724;
  let N = nRows ^ nRows;
  let nIter = Round(PI() / 4.0 / ArcSin(IntAsDouble(M) / Sqrt(IntAsDouble(N))) - 0.5);
  Message($"{nIter}");
  return RunGroversSearch(nBits, Oracle_Bits(nRows, _, _), 
    PrepareMean_Bits(nRows, _), nIter);
}
