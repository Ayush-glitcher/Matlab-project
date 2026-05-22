open powershell type cd "C:\Users\Ayush\OneDrive\Documents 1\GitHub\Matlab-project"
then type .venv\Scripts\activate
then type python app.py

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