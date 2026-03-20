from z3 import *

# pain variables for two patients - basic example
pain_level_A = Int('pain_level_A')
pain_level_B = Int('pain_level_B')

infection_level_A = Int('infection_level_A')
infection_level_B = Int('infection_level_B')

# prioritise welfare of the patient (utilitarian measure)
priority_A = pain_level_A + infection_level_A
priority_B = pain_level_B + infection_level_B

# identify who gets appointment
A_gets_slot = Bool('A_gets_slot')

s = Solver()

# Constraints for realistic ranges
s.add(pain_level_A >= 0, pain_level_A <= 10)
s.add(pain_level_B >= 0, pain_level_B <= 10)

s.add(infection_level_A >= 0, infection_level_A <= 10)
s.add(infection_level_B >= 0, infection_level_B <= 10)

# Utilitarian rule
# Prioritise patient with higher combined pain and infection score
s.add(If(priority_A > priority_B, A_gets_slot == True, A_gets_slot == False))

print(s.check())
print(s.model())