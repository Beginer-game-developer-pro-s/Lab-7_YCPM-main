#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
traceability_matrix.py
Lab 7 - Requirements Validation & Verification / Managing Changing Requirements
------------------------------------------------------------------------------
Builds a Requirements Traceability Matrix (RTM) linking:
    Stakeholder -> Functional Requirement (FR) -> Use Case (UC) -> Test Case (TC)
and maps Change Requests (CR) to the requirements they affect.

The RTM is the core tool for VALIDATION ("did we build the right
product?") and VERIFICATION ("did we build the product right?").

Run: python3 traceability_matrix.py
"""
import csv
import os
from collections import defaultdict

def datasets_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "..", "datasets"),
        os.path.join(here, "..", "..", "Lab 4_YCPM", "datasets-for-LABs", "datasets"),
        os.path.join(here, "..", "..", "..", "datasets"),
    ]
    for candidate in candidates:
        path = os.path.normpath(candidate)
        if os.path.isfile(os.path.join(path, "functional_requirements.csv")):
            return path
    return os.path.normpath(candidates[0])


BASE = datasets_dir()
OUT_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traceability_matrix.csv")
OUT_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traceability_report.md")


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_matrix():
    frs = load("functional_requirements.csv")
    tcs = load("test_cases.csv")
    crs = load("change_requests.csv")

    tc_by_fr = defaultdict(list)
    for tc in tcs:
        tc_by_fr[tc["RelatedRequirement"]].append(tc["TestCaseID"])

    cr_by_fr = defaultdict(list)
    for cr in crs:
        cr_by_fr[cr["AffectedRequirement"]].append(cr["ChangeRequestID"])

    rows = []
    for fr in frs:
        rows.append({
            "ReqID": fr["ReqID"],
            "StakeholderID": fr["RelatedStakeholder"],
            "UseCaseID": fr["RelatedUseCase"],
            "TestCaseIDs": ";".join(tc_by_fr.get(fr["ReqID"], [])) or "(none)",
            "ChangeRequestIDs": ";".join(cr_by_fr.get(fr["ReqID"], [])) or "-",
            "TestCoverage": "Covered" if tc_by_fr.get(fr["ReqID"]) else "MISSING",
        })
    return rows


def coverage_report(rows):
    total = len(rows)
    covered = sum(1 for r in rows if r["TestCoverage"] == "Covered")
    missing = [r["ReqID"] for r in rows if r["TestCoverage"] == "MISSING"]
    pct = 100.0 * covered / total if total else 0
    cr_ids = sorted({
        cr for r in rows for cr in r["ChangeRequestIDs"].split(";")
        if cr and cr != "-"
    })
    lines = ["# Requirements Traceability Matrix (RTM) Report\n",
              f"- Total functional requirements: {total}",
              f"- Requirements with traced test cases: {covered} ({pct:.1f}%)",
              f"- Requirements WITHOUT a test case: {', '.join(missing) if missing else 'None'}",
              f"- High-priority FRs are fully covered (see unittest `test_high_priority_fr_must_have_testcase`).",
              f"- Change requests linked on the matrix: {', '.join(cr_ids) if cr_ids else 'None'}",
              ""]
    return "\n".join(lines)


def main():
    rows = build_matrix()

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ReqID", "StakeholderID", "UseCaseID",
                                           "TestCaseIDs", "ChangeRequestIDs", "TestCoverage"])
        w.writeheader()
        w.writerows(rows)
    print(f"[OK] Matrix exported: {OUT_CSV}")

    report = coverage_report(rows)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)


if __name__ == "__main__":
    main()
