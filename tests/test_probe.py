import unittest

from examples.boom_probe import ALIASES, BOUNDARY, buggy_dirty_case, clean_case, dirty_case
from mcm.ir import Before, Guard
from mcm.merge import merge_equivalent_cases, normalize_case
from mcm.project import project_case


class ProbeProjectionTests(unittest.TestCase):
    def _project_normalize(self, case):
        return normalize_case(project_case(case, BOUNDARY), ALIASES)

    def test_clean_projects_internal_states_away(self):
        case = self._project_normalize(clean_case())
        self.assertIn(Before("ReleaseNotify", "ProbeResponse"), case.facts)
        self.assertNotIn("ProbeUnit.s_release", {x for f in case.facts for x in (f.src, f.dst)})

    def test_clean_and_dirty_merge_to_unconditional_boundary_case(self):
        clean = self._project_normalize(clean_case())
        dirty = self._project_normalize(dirty_case())
        merged = merge_equivalent_cases([clean, dirty])

        self.assertEqual(len(merged), 1)
        parent = merged[0]
        self.assertEqual(parent.guard, Guard.true())
        self.assertEqual(
            set(parent.facts),
            {
                Before("ProbeRecv", "ReleaseNotify"),
                Before("ReleaseNotify", "ProbeResponse"),
            },
        )

    def test_special_boundary_behavior_is_not_merged(self):
        clean = self._project_normalize(clean_case())
        buggy = self._project_normalize(buggy_dirty_case())
        merged = merge_equivalent_cases([clean, buggy])

        self.assertEqual(len(merged), 2)
        self.assertTrue(all(not case.guard.is_true() for case in merged))


if __name__ == "__main__":
    unittest.main()
