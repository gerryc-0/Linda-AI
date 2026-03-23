# Linda-AI
Our implemtation of various functional and ethical goals of Linda-AI virtual dental receptionist.

## Functional Goals
- Maximise Revenue/Bookings
    - [utilitarian/utilitarian_functional-UNSAT.py](utilitarian/utilitarian_functional-UNSAT.py)
- Reduce FTA rates
    - [deontology/deontology_functional.py](deontology/deontology_functional.py)
- Capturing and on-boarding new patients
    - Medical Card vs Practice Owner (deontology)
- Patient reactivation
    - avoid spam phonecalls: how recently did we call
- Enforce practice policies (deontology)
    - [deontology/deontology_functional.py](deontology/deontology_functional.py)
- Triage and prioritise appointments
    - [utilitarian](utilitarian) and [prioritarian](prioritarian)
- Free up receiptionist time for clinical matters
    - follows from all the above

## Ethical Goals
- Increase access to dental healthcare.
- Work with receptionist staff, don't replace them.
- Adhere to all data protection and dental laws and best practices.

## To-do
### Functional
- [x] Failure-to-attend workflow
    - covered by [deontology/deontology_functional.py](deontology/deontology_functional.py)
    - [ ] short notice cancellation: add fee to their account
- [ ] No spam phone calls
### Value Conflicts
- [ ] Medical Card vs Practice Owner
    - Correct implementation of booking policies
- [ ] Patient vs Receptionist
    - Expedient vs Accurate triage
- [ ] Patient vs Practice Owner
    - Appropriate Care, no overtreatment
- [ ] Dentist vs Practice Owner
    - Appointment length and workload