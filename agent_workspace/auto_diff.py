from sympy import symbols, diff, sin

# Define the variable and the function
x = symbols('x')
function = x**2 * sin(x)

# Calculate the derivative
derivative = diff(function, x)

# Print the result
print(derivative)