# Linda-AI
Reflective ethical analysis and Z3 modelling of Linda AI, an AI receptionist system used in dental clinics.

This repository contains a set of small Python scripts that model ethical decision scenarios for **Linda AI**, an AI receptionist used in dental clinics.

The scripts use the **Z3 constraint solver** to represent how different ethical frameworks influence decisions made by the AI assistant.

## Scripts

* `linda-ai-utilitarianism.py` – prioritising patients based on overall harm reduction.
* `linda-ai-prioritarianism.py` – prioritising vulnerable or disadvantaged patients.
* `linda-ai-deontology.py` – enforcing rule-based duties such as disclosure and consent.
* `linda-ai-virtue.py` – modelling virtuous professional behaviour (e.g., avoiding unnecessary treatment recommendations).
