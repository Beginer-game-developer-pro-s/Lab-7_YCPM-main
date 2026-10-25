# PHENIKAA UNIVERSITY
## SCHOOL OF INFORMATION SYSTEMS
### COURSE CSE703095 — SOFTWARE REQUIREMENTS

# LAB 07 REPORT  
## Validation, Verification & Change Management

- **Topic:** Requirements-set verification, traceability, and change-impact analysis for MedBook
- **Case study:** MedBook – Online Medical Appointment Booking System
- **Prepared by:** Hồ Điền Hùng (Member 1), Trần Doãn Việt Anh (Member 2), Cấn Đại Dương (Member 3)
- **Date:** 2026-10-23

Prepared for teaching & practice in the Software Requirements course.

---

## Contents

1. Initial Result: Dataset Bugs Found  
2. Root Cause & Fix  
3. Added Test Cases  
4. New Rule for Change Requests  
5. Result After Fixing  
6. Impact Analysis of a Self-authored Change Request  
7. Self-assessment  

---

## 1 Initial Result: Dataset Bugs Found

*(Member 1 — Hồ Điền Hùng)*

Running `python -m unittest test_requirements_consistency.py -v` against the original Lab 07 dataset produced **2 failures in 7 tests**:

1. `test_every_fr_has_a_valid_usecase` … FAIL  
   `AssertionError: FR-011 references a non-existent use case`
2. `test_high_priority_fr_must_have_testcase` … FAIL  
   `AssertionError: High-priority FRs with NO test case: ['FR-002', 'FR-007']`

`Ran 7 tests … FAILED (failures=2)`

FR-012 exhibited the same missing-use-case class of error (UC-12). The other five consistency rules already passed.

## 2 Root Cause & Fix

*(Member 2 — Trần Doãn Việt Anh)*

| Bug | Root cause | Fix |
| --- | --- | --- |
| FR-011 → UC-11 (and FR-012 → UC-12) | The FR catalogue used forward identifiers that were never added to `use_cases.csv` (only UC-01 … UC-10 existed). | Added **UC-11** (insurance coverage check) and **UC-12** (RBAC enforcement). FR identifiers were kept, because rewriting FR-011 onto UC-03/UC-05 would hide insurance verification inside booking. |
| FR-002, FR-007 missing TC | Labs 3/4 concentrated tests on booking, cancellation, allergy, registration, and RBAC; search and record-update were omitted even though both FRs are High priority. TC-006 measures NFR-001 search *performance*, not FR-002 functional correctness. | Added **TC-011** (FR-002) and **TC-012** (FR-007). |

`traceability_matrix.py` was re-run after the CSV updates.

## 3 Added Test Cases

*(Member 2 — Trần Doãn Việt Anh)*

| ID | Requirement | Test case name |
| --- | --- | --- |
| TC-011 | FR-002 | Search doctors by specialty and location returns matching results |
| TC-012 | FR-007 | Doctor updates a patient's medical record after a visit |

Existing IDs TC-001 … TC-010 were not modified.

## 4 New Rule for Change Requests

*(Member 1 — Hồ Điền Hùng)*

Approved change requests must record impact before they become baseline. Two automated rules were added to `test_requirements_consistency.py`:

- `test_approved_cr_has_estimated_impact` — every `Status == Approved` row needs a non-empty `EstimatedImpact`.
- `test_cr_references_valid_requirement` — every CR must point at an existing FR or NFR.

On the current file, CR-001, CR-002 and CR-005 already satisfy the first rule; CR-006 is `Under review` and is therefore excluded from that gate until the CCB decides.

## 5 Result After Fixing

*(Member 1 — Hồ Điền Hùng)*

`Ran 9 tests in … OK`

All original consistency tests plus the two CR rules PASS. The RTM still marks FR-005, FR-006, FR-009, FR-010 and FR-011 as `MISSING` test coverage; those FRs are Medium/Low priority, so they do not trip `test_high_priority_fr_must_have_testcase`. They remain a documented verification backlog.

## 6 Impact Analysis of a Self-authored Change Request

*(Member 3 — Cấn Đại Dương)*

**CR-006:** Require TOTP two-factor authentication when a doctor opens medical records from a new device or browser.

Using the RTM:

- **Direct:** FR-007 / UC-07 / TC-012 (clinical record access).
- **Indirect:** FR-012 (RBAC still applies), NFR-003 and NFR-004 (security and privacy).
- **Not affected:** booking, search, reminders, insurance, catalog (UC-01…UC-06, UC-08…UC-11).

Risk is **localised** to the identity/session layer. Estimated effort is **+5 working days**. Recommendation: **approve for phase 2**, after adding TC-013 (new device must challenge TOTP) and TC-014 (trusted device within TTL skips the extra prompt). The request stays `Under review` until those tests exist.

## 7 Self-assessment

*(Member 3 — Cấn Đại Dương, on behalf of the team)*

| Criterion | Max | Self score | Notes |
| --- | --- | --- | --- |
| Complete, accurate RTM | 2.0 | 2.0 | Bidirectional SH → FR → UC → TC → CR links, including CR-006. |
| Dataset fixed, tests PASS | 3.0 | 3.0 | 9/9 PASS after CSV repair and new CR rules. |
| New test cases + new rule | 2.5 | 2.5 | TC-011, TC-012; two CR quality rules. |
| Self-authored CR + impact | 1.5 | 1.5 | CR-006 with RTM impact and a phase-2 recommendation. |
| Presentation | 1.0 | 1.0 | English report; Vietnamese explanation in the submission notes. |
| **Total** | **10.0** | **10.0** | Residual: five non-High FRs still lack tests. |
