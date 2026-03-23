# Linda-AI
Reflective ethical analysis and Z3 modelling of Linda AI, an AI receptionist system used in dental clinics.

This repository contains a set of small Python scripts that model ethical decision scenarios for **Linda AI**, an AI receptionist used in dental clinics.

The scripts use the **Z3 constraint solver** to represent how different ethical frameworks influence decisions made by the AI assistant.

## Functional Goals
- Maximise Revenue/Bookings
    - [utilitarian\utilitarian_functional-UNSAT.py](utilitarian\utilitarian_functional-UNSAT.py)
- Reduce FTA rates
- Capturing and on-boarding new patients
    - 
- Patient reactivation
- Enforce practice policies
- Triage and prioritise appointments
- Free up receiptionist time for clinical matters


## To-do
- [ ] Failure-to-attend workflow
- [ ] Medical Card vs Practice Owner
    - Correct implementation of booking policies
- [ ] Patient vs Receptionist
    - Expedient vs Accurate triage
- [ ] Patient vs Practice Owner
    - Appropriate Care, no overtreatment
- [ ] Dentist vs Practice Owner
    - Appointment length and workload