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

    def test_timestamped_captions(self):
        data = [{"start": 0, "duration": 2, "text": "chen"},
                {"start": 50, "duration": 2, "text": "seichel"}]
        value = pipeline.timed_text(data)
        self.assertIn("[00:00:00] chen", value)
        self.assertIn("[00:00:45] seichel", value)


if __name__ == "__main__":
    unittest.main()
