import z3
import random

# Patient attributes
pain_level_A = z3.Int('pain_A')
pain_level_B = z3.Int('pain_B')

vulnerable_A = z3.Bool('vulnerable_A')
vulnerable_B = z3.Bool('vulnerable_B')

A_gets_slot = z3.Bool('A_gets_slot')

s = z3.Solver()

s.add(pain_level_A >= 0, pain_level_A <= 10)
s.add(pain_level_B >= 0, pain_level_B <= 10)

# Prioritarian rule:
# vulnerable patients is prioritised if pain equal
# medical card holders / elderly / children get priority if pain equal

# patient A is prioritised as they are vulnerable, patient B is not
s.add(
    z3.If(z3.And(pain_level_A == pain_level_B, vulnerable_A == True),
       A_gets_slot == True,
       A_gets_slot == False)
)

print(s.check()) # should be satisfiable
print(s.model())
