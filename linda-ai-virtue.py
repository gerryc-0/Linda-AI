import z3

# variables: 
# Bool: AI recommends a medical procedure
# Bool: whether there is a clinical need for it (verified by dentist)
procedure_recommended = z3.Bool('procedure_recommended')
clinical_need = z3.Bool('clinical_need')

s = z3.Solver()

# Virtuous behaviour:
# recommend treatment only if medically justified
# reject unnecessary procedures (upselling)

s.add(z3.Implies(procedure_recommended, clinical_need))

# sample scenario
# AI recommends a procedure that is not clinically needed
# potentially upselling to patient for profit
s.add(procedure_recommended == True)
s.add(clinical_need == False)

print(s.check()) # should be unsat