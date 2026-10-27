"""Offline checks that never call YouTube, OpenAI or Dropbox."""
import unittest
import pipeline


class TestCatalog(unittest.TestCase):
    def test_stable_existing_ids(self):
        rows = [
            {"speaker_id": "REB", "shiur_id": "REB-001",
             "verification_status": "transcript_extracted", "possible_duplicate_of": ""},
            {"speaker_id": "REB", "shiur_id": "",
             "verification_status": "metadata_found", "possible_duplicate_of": ""},
            {"speaker_id": "UNASSIGNED", "shiur_id": "",
             "verification_status": "attribution_unconfirmed", "possible_duplicate_of": ""},
            {"speaker_id": "REB", "shiur_id": "",
             "verification_status": "possible_alternate_upload", "possible_duplicate_of": "REB-001"}
        ]
        pipeline.assign_ids(rows)
        self.assertEqual(rows[0]["shiur_id"], "REB-001")
        self.assertEqual(rows[1]["shiur_id"], "REB-002")
        self.assertEqual(rows[2]["shiur_id"], "")
        self.assertEqual(rows[3]["shiur_id"], "")

    def test_attribution(self):
        self.assertEqual(
            pipeline.speaker_match("Torah 1 with David Reboh", ""), "REB")
        self.assertEqual(
            pipeline.speaker_match("Generic Torah 1", ""), "UNASSIGNED")

    def test_full_name_and_html_entity_attribution(self):
        self.assertEqual(
            pipeline.speaker_match(
                "R&#39; Chaim Menachem Kramer, Likutei Moharan Torah #1", ""),
            "KRA")
        self.assertEqual(
            pipeline.speaker_match(
                "R' Chaim Kramer explains Chen", ""), "KRA")
        self.assertEqual(
            pipeline.speaker_match("R' Chaim Menachem Kramer with David Reboh", ""),
            "UNASSIGNED")
        self.assertEqual(
            pipeline.speaker_match("Generic shiur", "List of guests: Chaim Kramer"),
            "UNASSIGNED")

    def test_reconcile_provisional_leads_without_reassigning_existing_ids(self):
        rows = [
            {"speaker_id": "KRA", "shiur_id": "KRA-001",
             "verification_status": "verified_metadata", "title": "Existing"},
            {"speaker_id": "UNASSIGNED", "shiur_id": "",
             "video_id": "testvideo01", "verification_status": "attribution_unconfirmed",
             "title": "R&#39; Chaim Menachem Kramer Torah #1"},
            {"speaker_id": "UNASSIGNED", "shiur_id": "",
             "video_id": "testvideo02", "verification_status": "attribution_unconfirmed",
             "title": "Likutei Moharan Introduction"},
        ]
        log = []
        pipeline.reconcile_speakers(rows, log)
        pipeline.assign_ids(rows)
        self.assertEqual(rows[0]["shiur_id"], "KRA-001")
        self.assertEqual(rows[1]["speaker_id"], "KRA")
        self.assertEqual(rows[1]["shiur_id"], "KRA-002")
        self.assertEqual(rows[1]["title"], "R' Chaim Menachem Kramer Torah #1")
        self.assertEqual(rows[2]["speaker_id"], "UNASSIGNED")
        self.assertEqual(rows[2]["shiur_id"], "")
        self.assertTrue(any("ATTRIBUTED [KRA]" in msg for msg in log))

    def test_timestamped_captions(self):
        data = [{"start": 0, "duration": 2, "text": "chen"},
                {"start": 50, "duration": 2, "text": "seichel"}]
        value = pipeline.timed_text(data)
        self.assertIn("[00:00:00] chen", value)
        self.assertIn("[00:00:45] seichel", value)


if __name__ == "__main__":
    unittest.main()
