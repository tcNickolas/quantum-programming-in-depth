import Std.Convert.*;
import Std.Math.*;
import GroversSearch.RunGroversSearch;
import NQueens.*;

operation Main() : Bool[] {
  let nRows = 10;
  let nBits = nRows * BitSizeI(nRows - 1);
  let M = 724;
  let N = nRows ^ nRows;
  let nIter = Round(PI() / 4.0 / ArcSin(IntAsDouble(M) / Sqrt(IntAsDouble(N))) - 0.5);
  return RunGroversSearch(nBits, Oracle_Indices(nRows, _, _), PrepareMean_Indices(nRows, _), nIter);
}

