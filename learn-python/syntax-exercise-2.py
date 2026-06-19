# ============================================================
# PYTHON SYNTAX EXERCISE 2 — For experienced devs new to Python
# Topics: data structures, comprehensions, unpacking,
#         functions, and classic Python gotchas
# ============================================================
# Run with: python probabilistic-reasoning/syntax-exercise-2.py


# ------ SECTION 1: Lists, Dicts, Tuples, Sets ------
#
# Python's core collections — learn when to use each.
#
# TASK 1a: Create a list of 5 strings (agent names).
#          Then append one more, remove the second element,
#          and print the final list.
# TODO:
some_list = ["hello", "world", "this", "is", "ashutosh"]
some_list.append("sangwan")
some_list.pop(1)
print(f"{some_list=}")

# TASK 1b: Create a dict mapping each agent name to a score (int).
#          Print only the names whose score is above 70.
# TODO:
agent_scores = {"agent_1": 10, "agent_2": 20, "agent_3": 30, "agent_4": 85}
for key in agent_scores:
    if agent_scores[key] > 70:
        print(f"{key=}")

# TASK 1c: A tuple is immutable. Create a tuple of (x, y) coordinates.
#          Try to change one value — observe (and then comment out) the error.
# TODO:
my_tuple = ("hello", "this", "is")
print(f"{my_tuple=}")
# my_tuple[1] = "that"
print(f"{my_tuple=}")


# TASK 1d: Create two sets of sensor readings and print:
#          - readings in both sets (intersection)
#          - readings in either set (union)
#          - readings only in the first set (difference)
# TODO:
my_set = {1, 12, 45, 21, 34, 44, 55}
my_set2 = {1, 13, 55, 12}
set_intersection = my_set.intersection(my_set2)
print(f"{set_intersection=}")
set_union = my_set.union(my_set2)
print(f"{set_union=}")
set_difference = my_set.difference(my_set2)
print(f"{set_difference=}")

# ------ SECTION 2: Comprehensions ------
#
# Python lets you build collections in a single readable line.
# Equivalent to map/filter in other languages but more idiomatic here.
#
# TASK 2a: Given the list below, use a LIST COMPREHENSION to produce
#          a new list with every value doubled.
values = [1, 5, 3, 8, 2, 9, 4]
# TODO: doubled = [...]

doubled = [2 * x for x in values]
print(f"{doubled=}")

# TASK 2b: From `values`, use a list comprehension to keep only even numbers.
# TODO: evens = [...]
even = [x for x in values if x % 2 == 0]
print(f"{even=}")

# TASK 2c: Given the agent scores dict from Task 1b, use a DICT COMPREHENSION
#          to build a new dict with scores normalised to 0–1 (divide by 100).
# TODO: normalised = {...}
normalised = {k: v / 100 for k, v in agent_scores.items()}
print(f"{normalised=}")

# TASK 2d: Combine filter + transform: from `values`, square every odd number.
# TODO: odd_squares = [...]
squaredList = [x * x for x in values if x % 2 == 1]
print(f"{squaredList=}")


# ------ SECTION 3: Unpacking & the * operator ------
#
# Python can destructure sequences directly into variables.
#
# TASK 3a: Unpack this tuple into three separate variables in one line.
coords = (42.3, -71.0, 15)
# TODO: lat, lon, alt = ...
# Then print each variable.
lat, lon, alt = coords
print(f"{lat=}")
print(f"{lon=}")
print(f"{alt=}")

# TASK 3b: Use * (starred assignment) to capture the "rest":
readings = [10, 20, 30, 40, 50]
# Unpack so that `first` = 10, `last` = 50, and `middle` = [20, 30, 40]
# TODO: first, *middle, last = ...
first, *middle, last = readings
print(f"{first=}")
print(f"{middle=}")
print(f"{last=}")

# TASK 3c: Swap two variables WITHOUT a temp variable (pure Python idiom).
a = "hello"
b = "world"
# TODO: swap a and b in one line, then print both.
b, a = a, b
print(f"{a=}")
print(f"{b=}")


# ------ SECTION 4: Functions — defaults, *args, **kwargs ------
#
# TASK 4a: Write a function `describe_agent(name, score=100)` that prints
#          "Agent <name> scored <score>."
#          Call it with and without the score argument.
# TODO:
def describe_agent(name, score=100):
    print(f"Agent {name} scored {score}")


describe_agent("Cooper")
describe_agent("Dane", 25)


# TASK 4b: Write a function `total(*scores)` that accepts any n umber of
#          integer arguments and returns their sum. Do NOT use the built-in sum().
# TODO:


def total(*scores):
    sum = 0
    for score in scores:
        sum += score
    print(f"{sum=}")
    return sum


total(1, 2, 3, 4, 5, 6)


# TASK 4c: Write a function `log_event(**details)` that accepts keyword
#          arguments and prints each key-value pair on its own line.
#          Call it like: log_event(agent="R2D2", action="scan", result="clear")
# TODO:
def log_event(**details):
    for key, val in details.items():
        print(f"{key=}//{val=}")


log_event(agent="Cooper", action="Recce", result="Successful")


# TASK 4d: Combine them — write `report(name, *scores, **meta)` that prints:
#          - the agent name
#          - the average of all scores
#          - each metadata key/value pair
# TODO:
def report(name, *scores, **meta):
    describe_agent(name)
    if len(scores) > 0:
        print(f"Average score is {total(*scores)/len(scores)}")
    log_event(**meta)


report("Cooper", 1, 2, 3, 4, agent="Cooper", action="Recce", result="SuccessfulReally")


# ------ SECTION 5: Python Gotchas for experienced devs ------
#
# These behaviours surprise almost everyone coming from another language.
#
# TASK 5a — Mutable default argument trap:
# The function below has a classic bug. Run it three times and observe the output.
# Then fix it so each call gets a fresh list.


def add_reading(value, history=None):  # <-- this is the bug
    if history is None:
        history = []
    history.append(value)
    return history


print(f"{add_reading(1)=}")  # expected: [1]
print(f"{add_reading(2)=}")  # expected: [2]  — but what do you actually get?
print(f"{add_reading(3)=}")  # expected: [3]  — and now?

# TODO: fix add_reading below (keep the default-argument interface)

# TASK 5b — `is` vs `==`:
# `==` checks value equality; `is` checks object identity (same object in memory).
# Predict the output of each line before running.

x = [1, 2, 3]
y = [1, 2, 3]
z = x

# TODO: what do you expect for each? Add a comment with your prediction, then run.
print(f"{x == y=}")  # prediction: True?
print(f"{x is y=}")  # prediction: False?
print(f"{x is z=}")  # prediction: True?

# TASK 5c — Truthiness:
# In Python many values are "falsy" beyond just False and 0.
# Predict which branch each print reaches, then run to verify.

for val in [0, "", [], None, {}, "hello", [0], 1]:
    if val:
        # "hello", [0], 1
        print(f"{repr(val):12} -> truthy")
    else:
        # 0, "", [], None,{}
        print(f"{repr(val):12} -> falsy")

# TASK 5d — Integer interning quirk (optional, just observe):
# Python caches small integers. Run this and explain WHY the results differ.
print(256 is 256)  # True
print(
    257 is 257
)  # may be True or False depending on context — why? I am getting true for this
