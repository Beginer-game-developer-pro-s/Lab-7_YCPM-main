#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_requirements_consistency.py
Lab 7 - VERIFICATION testing of requirements-set consistency
--------------------------------------------------------------------------
Uses Python's standard unittest library to automatically check
consistency rules across the requirements dataset - e.g. every
High-priority FR must have at least one test case; every use case
must map to a valid FR; etc.

This is an example of "testing the requirements document itself"
(requirements-based / static verification), distinct from testing
the running system.

Run:  python3 -m unittest test_requirements_consistency.py -v
"""
import csv
import os
import unittest

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


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestRequirementsConsistency(unittest.TestCase):
    """Check the consistency / completeness of the requirements dataset."""

    @classmethod
    def setUpClass(cls):
        cls.frs = load("functional_requirements.csv")
        cls.nfrs = load("nonfunctional_requirements.csv")
        cls.ucs = load("use_cases.csv")
        cls.tcs = load("test_cases.csv")
        cls.shs = load("stakeholders.csv")
        cls.crs = load("change_requests.csv")
        cls.fr_ids = {r["ReqID"] for r in cls.frs}
        cls.uc_ids = {r["UseCaseID"] for r in cls.ucs}
        cls.sh_ids = {r["StakeholderID"] for r in cls.shs}
        cls.nfr_ids = {r["NFRID"] for r in cls.nfrs}

    def test_every_fr_has_a_valid_stakeholder(self):
        """Every FR must reference an existing stakeholder."""
        for fr in self.frs:
            self.assertIn(fr["RelatedStakeholder"], self.sh_ids,
                           f"{fr['ReqID']} references a non-existent stakeholder")

    def test_every_fr_has_a_valid_usecase(self):
        """Every FR must reference an existing use case."""
        for fr in self.frs:
            self.assertIn(fr["RelatedUseCase"], self.uc_ids,
                           f"{fr['ReqID']} references a non-existent use case")

    def test_every_usecase_has_a_referencing_fr(self):
        """Every use case must be referenced back by at least one FR."""
        fr_uc_links = {fr["RelatedUseCase"] for fr in self.frs}
        orphan = self.uc_ids - fr_uc_links
        self.assertEqual(orphan, set(),
                          f"Use cases with no referencing FR: {orphan}")

    def test_high_priority_fr_must_have_testcase(self):
        """Every High-priority FR must have at least one traced test case (quality rule)."""
        tc_fr_ids = {tc["RelatedRequirement"] for tc in self.tcs}
        missing = [fr["ReqID"] for fr in self.frs
                   if fr["Priority"] == "High" and fr["ReqID"] not in tc_fr_ids]
        self.assertEqual(missing, [],
                          f"High-priority FRs with NO test case: {missing}")

    def test_no_duplicate_requirement_ids(self):
        """Requirement IDs (ReqID) must not be duplicated."""
        ids = [fr["ReqID"] for fr in self.frs]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate requirement ID detected")

    def test_nfr_has_smart_measurement_criterion(self):
        """Every NFR must have a non-empty SMART measurement criterion."""
        for nfr in self.nfrs:
            self.assertTrue(nfr["SMARTMeasurementCriterion"].strip(),
                             f"{nfr['NFRID']} is missing a SMART measurement criterion")

    def test_testcase_references_valid_requirement(self):
        """Every test case must reference an existing FR or NFR."""
        valid_ids = self.fr_ids | self.nfr_ids
        for tc in self.tcs:
            self.assertIn(tc["RelatedRequirement"], valid_ids,
                           f"{tc['TestCaseID']} references a non-existent requirement")

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

    def test_cr_references_valid_requirement(self):
        """Every CR must reference an existing FR or NFR."""
        valid_ids = self.fr_ids | self.nfr_ids
        for cr in self.crs:
            self.assertIn(
                cr["AffectedRequirement"], valid_ids,
                f"{cr['ChangeRequestID']} references a non-existent requirement",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
