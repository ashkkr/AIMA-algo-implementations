# ============================================================
# PYTHON SYNTAX EXERCISE
# Topics: Comments, Variables, Indentation
# ============================================================


# ------ TASK 1: Comments ------
# A comment starts with # and is ignored by Python.
# Your job: add a comment on the line above the print() below
# that explains what it does in plain English.

# The line below is printing a text to the standard console
print("Hello, I am a robot!")


# ------ TASK 2: Variables ------
# In Python you create a variable just by assigning a value to a name.
# No need to declare a type — Python figures it out.
#
# Create these three variables:
#   robot_name   — a string (str),  e.g. "R2D2"
#   battery_level — an integer (int), e.g. 75
#   is_active     — a boolean (bool), either True or False
#
# TODO: write the three assignments below

robot_name = "wumpus"
battery_level = 75
is_active = True 

# robot_name    = ...
# battery_level = ...
# is_active     = ...


# ------ TASK 3: Print variables ------
# Use print() to display each variable on its own line.
# Bonus: use an f-string to print something like:
#   "Robot name: R2D2"
#
# TODO: write three print() calls below

print(robot_name)
print(battery_level)
print(is_active)


# ------ TASK 4: Fix the indentation ------
# Python uses indentation (4 spaces) to define blocks.
# The code below is BROKEN — fix the indentation so it runs.
#
# (Tip: every line inside an if/else block must be indented.)

if battery_level > 50:
    print("Battery is sufficient.")     # <-- fix this line
else:
    print("Battery is low, recharge!")  # <-- fix this line


# ------ TASK 5: Write your own if/else ------
# If is_active is True, print "Robot is ON."
# Otherwise, print "Robot is OFF."
#
# TODO: write the if/else block below

if is_active:
    print("Robot is ON.")
else:
    print("Robot is OFF.")
