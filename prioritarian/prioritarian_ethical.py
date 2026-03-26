from z3 import *
import random

# keep emergency slots for the most high priority patients
people = [f"person_{i}" for i in range(10)]
slots = 6
Person, persons = EnumSort('Person', people)

# Predicate: Pregnant maps a Person to True/False
Priority = Function('Priority', Person, IntSort())
Booked = Function('Booked', Person, BoolSort())
s = Solver()

priorities = {}
random.seed(42)
for i, p in enumerate(persons):
    priority = random.randint(0,10)
    priorities[i]=priority
    s.add(Priority(p) == priority)

#first 5 people are already booked
for i in range(5):
    s.add(Booked(persons[i]) == True)

# prioritary above 8 they need to be booked
# p = Const('p', Person)
# s.assert_and_track(ForAll([p], Implies(Priority(p) >= 8, Booked(p))),\
#                    "Patients with priority geq 8 should be booked")
# do with for loop so we see in unsat core
for i,p in enumerate(persons):
    s.assert_and_track(Implies(Priority(p) >= 8, Booked(p)),\
                       f"Patients {p} has priority {priorities[i]} and is not booked.")

# only 1 emergency slot left
s.add(Sum([If(Booked(p), 1, 0) for p in persons]) <= slots)

# check model
result = s.check()

if result == sat:
    m = s.model()
    print("Result: SAT — a valid assignment was found.")
    for i, p in enumerate(persons):
        print(f"Booked({p}) = {m.evaluate(Booked(p))}, Priority({p}) = {m.evaluate(Priority(p))}")
else:
    print(f"Result: {result} — no solution exists.")
    print("Unsat core:", s.unsat_core())