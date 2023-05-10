import unittest
from unittest.mock import patch

import app
import fixtures.MockData as mock_html


class TestAppFunctions(unittest.TestCase):
    maxDiff = None  # make failing tests easier to debug

    @patch("app.get_bs4_soup")
    def test_endpoints_returned_by_get_region_paths(self, mock_get):
        expected = {
            1: "/RaceGroups/95983/Groups/1",
            2: "/RaceGroups/95983/Groups/2",
            3: "/RaceGroups/95983/Groups/3",
            4: "/RaceGroups/95983/Groups/4",
            5: "/RaceGroups/95983/Groups/5",
            6: "/RaceGroups/95983/Groups/6",
            7: "/RaceGroups/95983/Groups/7",
            8: "/RaceGroups/95983/Groups/8",
            9: "/RaceGroups/95983/Groups/9",
            10: "/RaceGroups/95983/Groups/10",
            11: "/RaceGroups/95983/Groups/11",
            12: "/RaceGroups/95983/Groups/12",
        }

        # Configue Mock object's return value
        mock_get.return_value = mock_html.mock_soup

        # Assertion.
        self.assertDictEqual(app.get_region_paths("mock_team_name"), expected)

    @patch("app.requests.get")
    def test_info_returned_by_get_identifiers_is_correct(self, mock_get):
        input_href = "mock/href/query/?resultSetId=212380#U44542375"
        expected = ("Lin Manuel", "Miranda", "M", 54, "Munster", "IN")
        mock_json_response = {
            "participants": [
                {
                    "user_id": 44542375,
                    "first_name": "Lin Manuel",
                    "last_name": "Miranda",
                    "event_id": 420484,
                    "event": "Region 1 - Running",
                    "bib_num": "2164",
                    "profile_filename_url": None,
                    "registration_id": 45016484,
                    "gender": "M",
                    "age": 54,
                    "city": "Munster",
                    "state": "IN",
                }
            ]
        }

        # Configue Mock object's return value.
        mock_get.return_value.json.return_value = mock_json_response

        # Assertion.
        self.assertEqual(app.get_identifiers(input_href), expected)

    @patch("app.requests.post")
    def test_miles_returned_by_get_miles_is_correct(self, mock_post):
        input_href = "mock/href/query//?resultSetId=212380#U44542375"
        expected = 442.71
        mock_json_response = {
            "mock_key1": {},
            "mock_key2": {},
            "results": [
                {
                    "result_tally_value": 442.71,
                    "result_tally_label": "Distance in Miles",
                    "result_tally_value_in_meters": 712472.683,
                }
            ],
        }

        # Configue Mock object's return value.
        mock_post.return_value.json.return_value = mock_json_response

        # Assertion.
        self.assertEqual(app.get_miles(input_href), expected)

    @patch("app.get_identifiers")
    @patch("app.get_miles")
    @patch("app.get_bs4_soup")
    @patch("app.get_region_paths")
    def test_data_is_organized_correctly_by_get_participant_data(
        self, mock_region_paths, mock_soup, mock_miles, mock_id
    ):
        # Configure mock return value.
        mock_region_paths.return_value = {
            1: "mock/RaceGroups/95983/Groups/802853",
            2: "mock/RaceGroups/95983/Groups/813501",
            3: "mock/RaceGroups/95983/Groups/832629",
            4: "mock/RaceGroups/95983/Groups/843369",
            5: "mock/RaceGroups/95983/Groups/855643",
            6: "mock/RaceGroups/95983/Groups/861224",
            7: "mock/RaceGroups/95983/Groups/894179",
            8: "mock/RaceGroups/95983/Groups/894180",
            9: "mock/RaceGroups/95983/Groups/894181",
            10: "mock/RaceGroups/95983/Groups/894182",
            11: "mock/RaceGroups/95983/Groups/894183",
            12: "mock/RaceGroups/95983/Groups/894184",
        }

        # Configure mock side-effects.
        #   * Alternate 2 sets of mock HTML between 12 regions.
        #   * Scrape HTML 1 for 2 participants.
        #   * Scrape HTML 2 for 3 participants.
        #   * Mock HTTP resp. for mileage results of each participant (5 results).
        #   * Mock HTTP resp. for ID of each unique participant (4 unique).
        #       - note: should be 3 unique, but there is entity resolution issue.

        mock_sp1, mock_sp2 = mock_html.bs4_objs
        mock_soup.side_effect = [mock_sp1, mock_sp2] * 6
        mock_miles.side_effect = [100.50, 200.50, 300.50, 400.50, 80.50] * 6
        mock_id.side_effect = [
            ("Christopher", "Jackson", "M", 47, "Indian Mound", "TN"),
            ("Karen", "Olivo", "F", 54, "Munster", "IN"),
            ("Chris", "Jackson", "M", 48, "Indian Mound", "TN"),
            ("Jonathon", "Groff", "M", 58, "Portage", "IN"),
        ]

        # TESTS->
        # Test data structures returned by get_participant_data.
        (
            participant_names,
            monthly_mileage_results,
            participant_identifiers,
        ) = app.get_participant_data("mock_team_name")

        results_to_test = [
            # tuples contain: given result, expected result.
            (
                participant_names,
                {
                    "Chris Jackson",
                    "Christopher Jackson",
                    "Jonathon Groff",
                    "Karen Olivo",
                },
            ),
            (
                monthly_mileage_results,
                {
                    1: {
                        "Christopher Jackson": 100.50,
                        "Karen Olivo": 200.50,
                    },
                    2: {
                        "Chris Jackson": 300.50,
                        "Karen Olivo": 400.50,
                        "Jonathon Groff": 80.50,
                    },
                    3: {
                        "Christopher Jackson": 100.50,
                        "Karen Olivo": 200.50,
                    },
                    4: {
                        "Chris Jackson": 300.50,
                        "Karen Olivo": 400.50,
                        "Jonathon Groff": 80.50,
                    },
                    5: {
                        "Christopher Jackson": 100.50,
                        "Karen Olivo": 200.50,
                    },
                    6: {
                        "Chris Jackson": 300.50,
                        "Karen Olivo": 400.50,
                        "Jonathon Groff": 80.50,
                    },
                    7: {
                        "Christopher Jackson": 100.50,
                        "Karen Olivo": 200.50,
                    },
                    8: {
                        "Chris Jackson": 300.50,
                        "Karen Olivo": 400.50,
                        "Jonathon Groff": 80.50,
                    },
                    9: {
                        "Christopher Jackson": 100.50,
                        "Karen Olivo": 200.50,
                    },
                    10: {
                        "Chris Jackson": 300.50,
                        "Karen Olivo": 400.50,
                        "Jonathon Groff": 80.50,
                    },
                    11: {
                        "Christopher Jackson": 100.50,
                        "Karen Olivo": 200.50,
                    },
                    12: {
                        "Chris Jackson": 300.50,
                        "Karen Olivo": 400.50,
                        "Jonathon Groff": 80.50,
                    },
                },
            ),
            (
                participant_identifiers,
                [
                    ("Christopher", "Jackson", "M", 47, "Indian Mound", "TN"),
                    ("Karen", "Olivo", "F", 54, "Munster", "IN"),
                    ("Chris", "Jackson", "M", 48, "Indian Mound", "TN"),
                    ("Jonathon", "Groff", "M", 58, "Portage", "IN"),
                ],
            ),
        ]

        # Assertion.
        for result, expected in results_to_test:
            with self.subTest('"result" -> "expected"'):
                self.assertEqual(result, expected)


class TestFlaskRequests(unittest.TestCase):
    def setUp(self) -> None:
        app.app.testing = True
        self.test_client = app.app.test_client()

    def test_get_response_from_index_page(self):
        # Verify contents of the index page.
        url = "/"
        resp = self.test_client.get(url)
        testcases = (
            (resp, b"Spreadsheet Generator"),
            (resp, b"Please wait around 30 seconds"),
        )

        # Assert that content is as expected.
        for resp, expected in testcases:
            with self.subTest():
                self.assertTrue(expected in resp.data)
        self.assertEqual(resp.status_code, 200)

    @patch("app.send_from_directory")
    @patch("app.generate_spreadsheet")
    def test_post_response_from_index_page(self, mock_speadsheet, mock_send):
        # Verify that a spreadsheet has been exported.
        mock_speadsheet.return_value = "foo"
        mock_send.return_value = "bar"

        url = "/"
        data = {"Team Name": "mock name"}
        resp = self.test_client.post(
            url, data=data, content_type="application/x-www-form-urlencoded"
        )

        # Assertions.
        self.assertTrue(mock_send.called)
        self.assertEqual(resp.status_code, 200)

    @unittest.skip("function has been removed for the time being")
    def test_get_response_for_export_spreadsheet(self):
        # Verify content of the download page.
        url = "/download"
        resp = self.test_client.get(url)

        testcases = (
            (resp, b"Download"),
            (resp, b"An Excel spreadsheet is being exported. This"),
        )

        # Assertions.
        for resp, expected in testcases:
            with self.subTest():
                self.assertTrue(expected in resp.data)
        self.assertEqual(resp.status_code, 200)

    # TODO: Add tests for utilities: assert that spreadsheet is styled correctly.
        # add test for generate_spreadsheet.


if __name__ == "__main__":
    unittest.main()
