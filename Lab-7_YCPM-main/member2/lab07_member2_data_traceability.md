# Lab 7 — Member 2: Data & Traceability Specialist

- **Member:** Trần Doãn Việt Anh
- **Role:** Analyze dataset errors, update CSV artifacts, and maintain the Requirements Traceability Matrix (RTM)

## Section 2. Root Cause & Fix Analysis

| ID | Symptom | Root cause | Impact on V&V / RTM | Fix applied | Files updated |
| --- | --- | --- | --- | --- | --- |
| RC-01 | FR-011 (`Verify health insurance coverage`) referenced **UC-11**, but `use_cases.csv` only contained UC-01 … UC-10. | Incomplete use-case catalog: FR-011 was added with a forward identifier (`UC-11`) while the corresponding use-case row was never generated. The same class of error existed for FR-012 → **UC-12**. | Validation fails: the FR cannot be traced to a specified user goal. `test_every_fr_has_a_valid_usecase` fails. Change request CR-005 (extra insurance partners) cannot be impact-analyzed against a use-case scenario. | Added UC-11 (insurance coverage check) and UC-12 (RBAC enforcement) instead of rewriting FR-011 to an existing, semantically wrong use case. | `datasets/use_cases.csv` |
| RC-02 | High-priority **FR-002** (doctor search) had **no** traced test case. | Test-case set was seeded around booking, cancellation, allergy warning, registration, and RBAC. Search (UC-02 / FR-002) was omitted even though it is High priority. TC-006 tests NFR-001 search *performance*, not FR-002 functional correctness. | Verification gap: “did we build the product right?” cannot be answered for search. Quality rule `test_high_priority_fr_must_have_testcase` fails. RTM `TestCoverage = MISSING`. | Added **TC-011** linked to FR-002 (filter-correct search results). | `datasets/test_cases.csv` |
| RC-03 | High-priority **FR-007** (view/update medical records) had **no** traced test case. | Coverage concentrated on safety/security TCs (FR-008, NFR-003, FR-012). Clinical record update (UC-07) was left without a functional test. | Same High-priority verification gap as FR-002; doctors’ core workflow is untested in the requirements set. | Added **TC-012** linked to FR-007 (view history and save a new visit result). | `datasets/test_cases.csv` |

**Decision note.** FR-011 was kept pointing to UC-11. Changing FR-011 to reuse UC-03/UC-05 would hide insurance verification inside booking/confirmation and break stakeholder SH-05 traceability. Adding the missing use cases restores 1-to-1 FR↔UC identifiers.

After the CSV updates, `traceability_matrix.py` was executed to refresh `code/traceability_matrix.csv` and `code/traceability_report.md`.

## Section 3. Additional Test Cases

| TestCaseID | RelatedRequirement | TestCaseName | Steps | ExpectedResult | Status | Why added |
| --- | --- | --- | --- | --- | --- | --- |
| TC-011 | FR-002 | Search doctors by specialty and location returns matching results | 1. Log in as patient; 2. Open doctor search; 3. Enter specialty=Cardiology and location=District 1; 4. Submit search | System displays only doctors whose specialty and location match the filters | Not run | Closes the High-priority functional gap for doctor search (distinct from NFR-001 load test TC-006). |
| TC-012 | FR-007 | Doctor updates a patient's medical record after a visit | 1. Log in as doctor; 2. Open the patient's visit history; 3. Add a new visit result and save | Visit history is displayed and the new result is stored in the medical record | Not run | Closes the High-priority functional gap for viewing and updating medical records. |

Existing IDs TC-001 … TC-010 were not modified. New IDs continue the series as required (TC-011, TC-012).
