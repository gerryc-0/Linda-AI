import z3

# if AI collects medical info, it must have disclosed to the patient
ai_disclosure = z3.Bool('ai_disclosure')
collect_medical_info = z3.Bool('collect_medical_info')

s = z3.Solver()

# Deontological rule: implication
# medical info cannot be collected unless AI disclosed
s.add(z3.Implies(collect_medical_info, ai_disclosure))

# Test scenario
s.add(collect_medical_info == True)

print(s.check())  
print(s.model())