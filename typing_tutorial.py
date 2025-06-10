from typing import TypedDict, Union, Optional, Any

# ---------------------------------------------------- #

# TypedDict allows us to define a dictionary with specific keys and their types
class Movie(TypedDict):
  name: str
  year: int

movie = Movie(name="Inception", year=2010)

# --------------------------------------------------- #

# Union lets use multiple types for a variable
def square(x: Union[int, float]) -> float:
  return x * x

x1 = 5
result = square(x1)

x2 = 1.6
result = square(x2)

x3 = "5"  # This will cause a type error if checked with a type checker

# --------------------------------------------------- #

# Optional allows a variable to be of a specific type or None
def greet(name: Optional[str]) -> None:
    if name is None:
        print("Hello, World!")
    print(f"Hello, {name}!")

greet("Alice")
greet(None)

# --------------------------------------------------- #

# Any allows a variable to be of any type
def process_data(data: Any) -> None:
    print(f"Processing data: {data}")

process_data("A string")
process_data(42)

# --------------------------------------------------- #

# lamda functions are shortcut functions defined with the lambda keyword
cube = lambda x: x * x * x

cube(3)


