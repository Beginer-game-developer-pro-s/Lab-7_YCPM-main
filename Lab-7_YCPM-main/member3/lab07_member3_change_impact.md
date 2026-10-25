# Lab 7 — Member 3: Change-management Analyst

- **Member:** Cấn Đại Dương
- **Role:** Author a change request, analyse its impact through the RTM, and complete the team self-assessment

## Section 6. Impact Analysis of a Self-authored Change Request

**CR-006** — *Require TOTP two-factor authentication when a doctor opens medical records from a new device or browser.*

| Field | Value |
| --- | --- |
| ChangeRequestID | CR-006 |
| DateProposed | 2026-10-23 |
| ProposedBy | SH-06 (Hospital IT department) |
| AffectedRequirement (primary) | FR-007 (Doctor views and updates medical records) |
| Priority | High |
| Status | Under review |
| EstimatedImpact | Touches FR-007, FR-012, NFR-003 and NFR-004; needs identity service, session policy, and extra tests; estimated +5 working days |

### Why this change

FR-007 is High priority and clinically sensitive: a doctor on a borrowed workstation can currently open visit history after a single login. SH-07 (health regulator) and NFR-003/NFR-004 already demand encryption and data minimisation, but they do not constrain *session* assurance. CR-006 closes that gap without rewriting the clinical workflow.

### Forward trace from the RTM

| Artefact | Link | Effect of CR-006 |
| --- | --- | --- |
| Stakeholder | SH-02 (Doctor), SH-06 (IT), SH-07 (Regulator) | Doctors gain a second factor; IT owns the authenticator; the regulator’s privacy duty is strengthened. |
| Primary FR | FR-007 → UC-07 → TC-012 | UC-07 preconditions must include a trusted device or a completed TOTP challenge. TC-012 remains valid for the “happy path” on a known device; a negative test is still missing. |
| Secondary FR | FR-012 → UC-12 → TC-009 | RBAC still decides *which* role may open records; 2FA decides *whether the session is trusted*. TC-009 (patient hitting admin API) is unaffected. |
| NFRs | NFR-003 (Security), NFR-004 (Privacy) | Complements AES-256/TLS; does not replace them. Measurement: 100% of new-device doctor sessions must complete TOTP before `visit_result` is returned. |
| Existing CRs | none on FR-007 | No collision with CR-001…CR-005. |
| Unrelated flows | UC-01…UC-06, UC-08…UC-11 | Booking, search, reminders, insurance and catalog stay unchanged → **localised risk**. |

### Impact verdict

- **Scope:** identity/session layer plus the medical-record screen; not the booking engine.
- **Schedule:** about five working days (authenticator library, device register, two extra test cases, privacy notice).
- **Verification debt:** add TC-013 (new device → TOTP required) and TC-014 (known device within TTL → no extra prompt). Until those exist, CR-006 must not be marked `Approved`.
- **Recommendation:** **approve for phase 2**, after FR-007’s current TC-012 stays green and the two new tests are written. Do not fold this into phase-1 booking work.

The row is stored in `datasets/change_requests.csv` so later RTM refreshes keep CR-006 visible on FR-007.

## Section 7. Self-assessment

| Criterion | Max | Self score | Notes |
| --- | --- | --- | --- |
| Complete, accurate RTM | 2.0 | 2.0 | Stakeholder → FR → UC → TC → CR rebuilt after Member 2’s CSV repairs; CR-006 appears on FR-007. |
| Dataset fixed, tests PASS | 3.0 | 3.0 | Pre-fix: 7 tests, 2 failures. Post-fix: 9 tests, 0 failures (7 original + 2 CR rules). |
| New test cases + new rule | 2.5 | 2.5 | TC-011, TC-012 (Member 2); `test_approved_cr_has_estimated_impact` and `test_cr_references_valid_requirement` (Member 1). |
| Self-authored CR + impact | 1.5 | 1.5 | CR-006 analysed through the RTM; phase-2 recommendation with explicit verification debt. |
| Presentation | 1.0 | 1.0 | English team report follows the Lab 07 sample section order. |
| **Total** | **10.0** | **10.0** | Honest residual: Medium/Low FRs FR-005, FR-006, FR-009, FR-010, FR-011 still lack tests; they sit outside the High-priority quality rule. |
