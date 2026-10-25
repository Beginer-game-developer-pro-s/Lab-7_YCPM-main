# Lab 7 — Member 1: Verification & Quality Engineer

- **Member:** Hồ Điền Hùng
- **Role:** Execute requirements-set verification, add a change-request quality rule, and record PASS/FAIL evidence

## Section 1. Initial Result: Dataset Bugs Found

Static verification was performed with Python’s `unittest` library on `code/test_requirements_consistency.py`. This checks the *requirements document itself* (completeness, consistency, and traceability), not a running MedBook application.

**Command.** `python -m unittest test_requirements_consistency.py -v` (working directory: `code/`)

**Pre-fix outcome (historical, before Member 2’s CSV repairs).** 7 tests ran; **2 failed**:

| Test | Result | Evidence |
| --- | --- | --- |
| `test_every_fr_has_a_valid_usecase` | FAIL | `FR-011` pointed to **UC-11**, which was absent from `use_cases.csv` (only UC-01 … UC-10 existed). The same class of error applied to FR-012 → UC-12. |
| `test_high_priority_fr_must_have_testcase` | FAIL | High-priority **FR-002** (doctor search) and **FR-007** (medical-record update) had no traced test case. |
| Remaining five consistency tests | PASS | Stakeholder links, duplicate IDs, NFR SMART criteria, reverse UC→FR links, and TC→requirement links were already valid. |

These two failures are verification defects: the specification could not prove that every functional requirement maps to a specified user goal, nor that every High-priority FR is testable through the current test-case set.

## Section 4. New Rule for Change Requests

Approved change requests must not enter the baseline without an impact statement. An empty `EstimatedImpact` field would let the CCB approve work whose cost, schedule, and test ripple are unknown.

The following quality rule was added to `TestRequirementsConsistency`:

```python
def test_approved_cr_has_estimated_impact(self):
    """Every Approved change request must have a non-empty EstimatedImpact field."""
    missing = [
        cr["ChangeRequestID"] for cr in self.crs
        if cr["Status"] == "Approved" and not cr["EstimatedImpact"].strip()
    ]
    self.assertEqual(
        missing, [],
        f"Approved CRs missing EstimatedImpact: {missing}",
    )
```

A companion rule, `test_cr_references_valid_requirement`, rejects change requests that point at a non-existent FR or NFR. Together they turn change control into an automated gate rather than a manual spreadsheet check.

CR-001, CR-002 and CR-005 are `Approved` and already carry non-empty impact text, so the new rule PASSes on the current dataset.

## Section 5. Result After Fixing

After Member 2 restored UC-11/UC-12 and added TC-011/TC-012, and after Member 1 registered the two CR rules, the same command was re-run.

**Post-fix outcome.** 9 tests ran; **0 failed**.

| Test | Result |
| --- | --- |
| `test_cr_references_valid_requirement` | ok |
| `test_every_fr_has_a_valid_stakeholder` | ok |
| `test_every_fr_has_a_valid_usecase` | ok |
| `test_every_usecase_has_a_referencing_fr` | ok |
| `test_high_priority_fr_must_have_testcase` | ok |
| `test_nfr_has_smart_measurement_criterion` | ok |
| `test_no_duplicate_requirement_ids` | ok |
| `test_testcase_references_valid_requirement` | ok |
| `test_approved_cr_has_estimated_impact` | ok |

`Ran 9 tests … OK`

The requirements set is now internally consistent under the expanded quality gate. Residual product-level risk remains: five Medium/Low FRs (FR-005, FR-006, FR-009, FR-010, FR-011) still have `TestCoverage = MISSING` on the RTM; they are outside the High-priority rule and are noted for later labs rather than being silently treated as verified.
