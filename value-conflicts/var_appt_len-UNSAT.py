import z3
import random
# traige patients appropriately based on pain and infection, and appointment length

# set number of patients and hours
# simple 1 hour per appoitment in this model, may extend if we have time
num_patients = 20
num_hours = 9  # Available appointment slots

# store data as in grid problem
patients_data = []

# Generate synthetic patient data
random.seed(42) # seed make sure same unsat is produced each time
for i in range(num_patients):
    revenue = random.randint(1, 10)*100
    pain = random.randint(0, 10)
    # Infection and pain levels are correlated
    if pain > 5:
        infection = random.randint(5, 10)
    else:
        infection = random.randint(0, 5)
    time = random.choice([15,30,45,60])
    patients_data.append({'id': i, 'pain': pain,
                        'infection': infection,
                        'priority': z3.IntVal(pain + infection),
                        'revenue': revenue,
                        'time': time})

# optimiser

optimizer = z3.Optimize()

# var for each patient each hour to decide if they are scheduled or not
# use ints for mult below
see_patient = [z3.Int(f"see_patient_{i}") for i in range(num_patients)]


# constrain to 0 or 1 as in grid problem
for i in range(num_patients):
    v = see_patient[i]
    optimizer.assert_and_track(
        z3.Or(v == 0, v == 1),
        f"See patient {i}"
    )

# score is sum product of revenues and schedule
utilitarian_score = z3.Sum([
    see_patient[i] * patients_data[i]['revenue']
    for i in range(num_patients)
])

total_time = z3.Sum([
    see_patient[i] * patients_data[i]['time']
    for i in range(num_patients)
])

optimizer.maximize(utilitarian_score)

result = optimizer.check()

if result == z3.sat:
    model = optimizer.model()

    scheduled = []
    unscheduled = []

    for i in range(num_patients):
        if model[see_patient[i]] == 1:
            scheduled.append(patients_data[i])
        else:
            unscheduled.append(patients_data[i])

    print("\n===Results===")
    print(f"Patients Scheduled: {len(scheduled)}/{num_patients}")
    print(f"Patients Deferred:  {len(unscheduled)}/{num_patients}")

    scheduled_revenue = sum(p['revenue'] for p in scheduled)
    deferred_revenue  = sum(p['revenue'] for p in unscheduled)

    scheduled_time = sum(p['time'] for p in scheduled)

    print(f"\nTotal Revenue (Scheduled): {scheduled_revenue}")
    print(f"Total time (Scheduled): {scheduled_time/60}/{num_hours} Hours")
    print(f"\nTotal Revenue (Deferred):  {deferred_revenue}")
  
    print("\n---unscheduled patients---")
    for p in sorted(unscheduled, key=lambda x: -x['revenue']):
        print(f"  Patient {p['id']}: revenue={p['revenue']}, priority={p['priority']}, time={p['time']}")

    s = z3.Solver()

    s.assert_and_track(z3.BoolVal(scheduled_time <= num_hours*60), "Scheduled time greater than total hours. Dentist burnout inevitable!")
    print(s.check())
    print(s.unsat_core())
else:
    print("UNSAT")
    print("Core:", optimizer.unsat_core())
