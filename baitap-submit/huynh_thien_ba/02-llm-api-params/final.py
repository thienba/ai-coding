from cmath import sqrt

def solve_cubic_equation(a, b, c, d):
  if a == 0:
    raise ValueError("Coefficient a cannot be zero for a cubic equation")
  delta = (b**2 - 4*a*c)
  if delta >= 0:
    x1 = (-b - sqrt(delta)) / (2*a)
    x2 = (-b + sqrt(delta)) / (2*a)
    return x1, x2
  else:
    x1 = (-b - sqrt(abs(delta))) / (2*a)
    x2 = (-b + sqrt(abs(delta))) / (2*a)
    x3 = (-b) / (2*a)
    return x1, x2, x3