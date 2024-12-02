import Std.Diagnostics.CheckAllZero;

function FZero(arg : Bool) : Bool {
  return false;
}

function FOne(arg : Bool) : Bool {
  return true;
}

function FX(arg : Bool) : Bool {
  return arg;
}

function FOneMinusX(arg : Bool) : Bool {
  return not arg;
}


operation AssertOperationImplementsFunction(
  op : (Qubit, Qubit) => Unit, 
  f : Bool -> Bool
) : Unit {
  use (x, y) = (Qubit(), Qubit());
  for input in [false, true] {
    if input {
      X(x);
    }

    op(x, y);

    let expected = f(input);
    if expected {
      X(y);
    }
    if input {
      X(x);
    }

    if not CheckAllZero([y]) {
      fail $"Error for x={input}: expected {expected}, got {not expected}";
    }
    if not CheckAllZero([x]) {
      fail $"Error for x={input}: the state of the input qubit changed";
    }
  }
}
