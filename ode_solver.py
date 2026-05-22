"""
ODE Solver - Python / SymPy
Solves ODEs and separates complementary + particular solutions.

Usage:
    python ode_solver.py

Input format — enter LHS = RHS  (natural math notation):
    diff(y(x), x, 2) + 4*y(x) = sin(2*x)
    diff(y(x), x) + 2*y(x) = exp(-x)
    diff(y(x), x, 2) - 3*diff(y(x), x) + 2*y(x) = exp(x)

You can also omit the RHS (assumed 0):
    diff(y(x), x, 2) + 4*y(x) - sin(2*x)

Requires:
    pip install sympy
"""
import sys
sys.setrecursionlimit(10000)
import sympy as sp
from sympy import symbols, Function, dsolve, simplify


# ── helpers ───────────────────────────────────────────────────────────────────

def _build_namespace(x, y):
    return {
        "x":    x,
        "y":    y,
        "diff": lambda f, *a: sp.diff(f, *a),
        "sin":  sp.sin,  "cos": sp.cos,  "tan": sp.tan,
        "exp":  sp.exp,  "ln":  sp.ln,   "log": sp.log,
        "sqrt": sp.sqrt, "Abs": sp.Abs,
        "pi":   sp.pi,   "E":   sp.E,
    }


def parse_ode(expr_str: str, x, y):
    """
    Accept:
      LHS = RHS   e.g.  diff(y(x),x,2) + 4*y(x) = sin(2*x)
      LHS == RHS  (same with double equals)
      LHS only    (RHS assumed 0)
    Returns sympy.Eq.
    """
    ns   = _build_namespace(x, y)
    safe = {"__builtins__": {}}

    normalised = expr_str.replace("==", "=")
    if "=" in normalised:
        left_str, right_str = normalised.split("=", 1)
        try:
            lhs = eval(left_str.strip(),  safe, ns)
            rhs = eval(right_str.strip(), safe, ns)
        except Exception as e:
            raise ValueError(f"Could not parse: {e}")
        return sp.Eq(lhs, rhs)
    else:
        try:
            expr = eval(expr_str.strip(), safe, ns)
        except Exception as e:
            raise ValueError(f"Could not parse: {e}")
        return sp.Eq(expr, 0)


def _has_y_deriv(expr, yx):
    for sub in sp.preorder_traversal(expr):
        if isinstance(sub, sp.Derivative) and sub.args[0] == yx:
            return True
    return False


def _forcing(ode_eq, x, y):
    """Return f(x) so the ODE is L[y] = f(x)."""
    yx   = y(x)
    full = sp.expand(ode_eq.lhs - ode_eq.rhs)
    force = sp.S.Zero
    for term in sp.Add.make_args(full):
        if not term.has(yx) and not _has_y_deriv(term, yx):
            force += term
    return -force


def _homogeneous_eq(ode_eq, x, y):
    f   = _forcing(ode_eq, x, y)
    lhs = sp.expand(ode_eq.lhs - ode_eq.rhs) + f
    return sp.Eq(lhs, 0)

def auxiliary_roots(ode_eq, x, y):
    """
    Find roots of the auxiliary equation for
    linear constant-coefficient homogeneous ODEs.
    """

    yx = y(x)

    # Convert equation to LHS = 0 form
    expr = sp.expand(ode_eq.lhs - ode_eq.rhs)

    # Build auxiliary polynomial
    m = sp.symbols('m')
    aux_expr = 0

    for term in sp.Add.make_args(expr):

        # y'' terms
        if term.has(sp.Derivative):
            for d in term.atoms(sp.Derivative):

                if d.expr == yx:
                    order = d.derivative_count

                    # coefficient of derivative
                    coeff = term / d

                    aux_expr += coeff * m**order

        # y terms
        elif term.has(yx):
            coeff = term / yx
            aux_expr += coeff

    aux_expr = sp.expand(aux_expr)

    # Find roots
    roots = sp.solve(aux_expr, m)

    return aux_expr, roots

# ── main solver ───────────────────────────────────────────────────────────────

def solve_ode(ode_str: str):
    x = symbols("x")
    y = Function("y")
    sep = "=" * 60

    print(f"\n{sep}\n  ODE SOLVER\n{sep}")

    try:
        ode_eq = parse_ode(ode_str, x, y)
    except ValueError as e:
        print(f"\n[ERROR] {e}")
        return

    print(f"\nGiven ODE:\n  {ode_eq}")
    try:
        aux_eq, roots = auxiliary_roots(
            _homogeneous_eq(ode_eq, x, y),
            x,
            y
        )
    
        print(f"\nAuxiliary Equation:")
        print(f"  {aux_eq} = 0")
    
        print(f"\nRoots:")
        for r in roots:
            print(f"  {r}")
    
    except Exception as e:
        print(f"\n[INFO] Could not determine auxiliary roots: {e}")
    # General solution
    try:
        gen_sol = dsolve(ode_eq, y(x))
        y_gen   = simplify(gen_sol.rhs)
    except Exception as e:
        print(f"\n[ERROR] Could not solve ODE: {e}")
        return

    print(f"\nGeneral Solution (y):\n  y(x) = {y_gen}")

    # Complementary solution
    homo_eq = _homogeneous_eq(ode_eq, x, y)
    yc = None
    try:
        yc = simplify(dsolve(homo_eq, y(x)).rhs)
    except Exception:
        try:
            yc = simplify(dsolve(sp.Eq(ode_eq.lhs, 0), y(x)).rhs)
        except Exception as e2:
            print(f"\n[ERROR] Could not find complementary solution: {e2}")

    if yc is not None:
        print(f"\nComplementary Solution (yc):\n  yc(x) = {yc}")

    # Particular solution
    if yc is not None:

        yp = simplify(y_gen - yc)

        leftovers = yp.free_symbols - {x}

        if leftovers:
            yp = simplify(
                yp.subs({c: 0 for c in leftovers})
            )

        print(f"\\nParticular Solution (yp):")
        print(f"  yp(x) = {yp}")
              
        result = {
            "general_solution":
                str(y_gen),

            "complementary_solution":
                str(yc),

            "particular_solution":
                str(yp),

            "auxiliary_equation":
                str(aux_eq),

            "roots":
                [str(r) for r in roots]
        }

        return result

    else:

        return {
            "error":
                "Could not separate particular solution."
        }

# ── interactive loop ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("""
============================================================
  ODE SOLVER  (Python / SymPy)
============================================================

Enter the ODE in natural  LHS = RHS  form.

  Variable  : x
  Function  : y   ->  write  y(x)
  Derivatives:
      diff(y(x), x)       1st order
      diff(y(x), x, 2)    2nd order
      diff(y(x), x, 3)    3rd order

  Examples:
    diff(y(x), x, 2) + 4*y(x) = sin(2*x)
    diff(y(x), x) + 2*y(x) = exp(-x)
    diff(y(x), x, 2) - 3*diff(y(x), x) + 2*y(x) = exp(x)
    diff(y(x), x, 2) + 4*diff(y(x), x) + 4*y(x) = x*exp(-2*x)
    diff(y(x), x, 2) + y(x) = 0           (homogeneous)

  Or enter just the LHS (RHS assumed 0):
    diff(y(x), x, 2) + 4*y(x) - sin(2*x)

Type  exit  to quit.
""")

    while True:
        try:
            user_input = input("Enter ODE:\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("exit", "quit", "q"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        solve_ode(user_input)