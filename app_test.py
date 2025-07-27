import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from bs4 import BeautifulSoup
import logging
from itertools import cycle

import app
import fixtures.MockData as mock_html

class QuietAsyncTestCase(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        logging.getLogger("asyncio").setLevel(logging.ERROR)  # silence asyncio logger
        logging.getLogger("app").setLevel(logging.ERROR)


class TestAsyncAppFunctions(QuietAsyncTestCase):
    maxDiff = None  # make failing tests easier to debug

    @patch("aiohttp.ClientSession.get")
    async def test_get_bs4_soup_returns_soup(self, mock_get):
        mock_html = "<html><body><p>Mock Team Name</p></body></html>"
        expected_text = "Mock Team Name"

        # Set up async mock response
        mock_resp = AsyncMock()
        mock_resp.text.return_value = mock_html

        # Set up mock get w/ __aenter__ (used to mimic a return from a context manager)
        mock_get.return_value.__aenter__.return_value = mock_resp

        url = "mock_url"
        group = "mock_payload"
        bs4_soup = await app.get_bs4_soup(url, group)

        self.assertIsInstance(bs4_soup, BeautifulSoup)
        self.assertEqual(bs4_soup.text, expected_text)

    async def test_info_returned_by_get_identifiers(self):
        input_href = "/mock/href/query/?resultSetId=212380#U44542375"
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

        # Configure mock response and context manager.
        mock_resp = AsyncMock()
        mock_resp.json.return_value = mock_json_response
        mock_resp.__aenter__.return_value = mock_resp

        # Configue mock session.
        mock_session = MagicMock()
        mock_session.get.return_value = mock_resp

        result = await app.get_identifiers(mock_session, input_href)

        # Assertion.
        self.assertEqual(result, expected)


    @patch("asyncio.sleep")
    async def test_miles_returned_by_get_miles(self, mock_sleep):
        input_href_200 = "/mock_200/href/query//?resultSetId=212380#U44542375"
        input_href_429 = "/mock_429/href/query//?resultSetId=212380#U44542375"
        expected_200 = 442.71
        expected_429 = 0
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

        mock_sleep.return_value = None # mock sleep to speed up testing output.

        # Configure 2 mock responses, one successful and one not.
        mock_resp_200 = AsyncMock()
        mock_resp_200.json = AsyncMock(return_value=mock_json_response)
        mock_resp_200.status = 200

        mock_resp_429 = AsyncMock()
        mock_resp_429.json = None
        mock_resp_429.status = 429

        # Configue mock session
        mock_session = MagicMock()

        # Configure multiple mock_session return values in order to test retry-logic.
        mock_session.post.side_effect = [
            AsyncMock(__aenter__ = AsyncMock(return_value=mock_resp_429)),  # initial request for input_href_429
            AsyncMock(__aenter__ = AsyncMock(return_value=mock_resp_429)),  # first retry
            AsyncMock(__aenter__ = AsyncMock(return_value=mock_resp_429)),  # second retry
            AsyncMock(__aenter__ = AsyncMock(return_value=mock_resp_429)),  # initial request for input_href_200
            AsyncMock(__aenter__ = AsyncMock(return_value=mock_resp_429)),  # first retry
            AsyncMock(__aenter__ = AsyncMock(return_value=mock_resp_429)),  # second retry
            AsyncMock(__aenter__ = AsyncMock(return_value=mock_resp_200)),  # third retry
        ]

        # Assertions.
        result = await app.get_miles(mock_session, input_href_429, max_retries=2)
        self.assertEqual(result, expected_429)

        result = await app.get_miles(mock_session, input_href_200, max_retries=3)
        self.assertEqual(result, expected_200)

    @patch("app.get_miles", new_callable=AsyncMock)  #default new_callable is MagicMock
    @patch("app.get_identifiers", new_callable=AsyncMock)
    @patch("app.get_bs4_soup", new_callable=AsyncMock)
    @patch("app.get_region_paths", new_callable=AsyncMock)
    async def test_get_participant_data(
        self, mock_region_paths, mock_soup, mock_ids, mock_miles
    ):
        # Configure mock return value for region URL paths.
        mock_region_paths.return_value = {
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

        # Configure mock return values with side-effects for app.get_bs4_soup.
        #   * Stub response for each of 12 regions by alternating 2 mock-soup (HTML) responses.
        #   * mock_soup1 contains data for 2 participants.
        #   * mock_soup2 contains data for 3  participants, some which overlap with mock_soup1.
        #   * Coordinate w/ mock html to correctly mock mile side-effects and identifer side-effects.
        #       - note: There are 3 unique participants, but there is an entity resolution issue, so expect 4.

        mock_soup1, mock_soup2 = mock_html.bs4_objs
        mock_soup.side_effect = [mock_soup1 if i % 2 == 0 else mock_soup2 for i in range(12)]

        # Configure mock return values with side-effects for app.get_identifiers.
        mock_ids.side_effect = [
            ("Christopher", "Jackson", "M", 47, "Indian Mound", "TN"),
            ("Karen", "Olivo", "F", 54, "Munster", "IN"),
            ("Chris", "Jackson", "M", 48, "Indian Mound", "TN"),
            ("Jonathon", "Groff", "M", 58, "Portage", "IN"),
        ]

        # Configure mock return values with side-effects for app.get_miles.
        mile_values = cycle([100.50, 200.50, 300.50, 400.50, 80.50])  # Cycle through integers as needed while preserving sequence order.
        mock_miles.side_effect = mile_values

        # EXPECTED RESPONSES.
        expected_names = {
                    "Chris Jackson",
                    "Christopher Jackson",
                    "Jonathon Groff",
                    "Karen Olivo",
                }

        expected_miles = {
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
                }

        expected_identifiers = [
            ("Christopher", "Jackson", "M", 47, "Indian Mound", "TN"),
            ("Karen", "Olivo", "F", 54, "Munster", "IN"),
            ("Chris", "Jackson", "M", 48, "Indian Mound", "TN"),
            ("Jonathon", "Groff", "M", 58, "Portage", "IN"),
        ]

        # TESTS: Test content of data structures returned by app.get_participant_data.
        (
            participant_names,
            monthly_mileage_results,
            participant_identifiers,
        ) = await app.get_participant_data("mock_team_name")

        test_cases = [
            # tuples contain: given result, expected result.
            (participant_names, expected_names),
            (monthly_mileage_results, expected_miles),
            (participant_identifiers, expected_identifiers),
        ]

        for result, expected in test_cases:
            with self.subTest('"result" -> "expected"'):
                self.assertEqual(result, expected)


class TestAppFunctions(unittest.TestCase):
    maxDiff = None  # make failing tests easier to debug

    @unittest.skip("Update to be async/ work with coroutine object")
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
            (resp, b"Please wait a few seconds"),
        )

        # Assert that content is as expected.
        for resp, expected in testcases:
            with self.subTest():
                self.assertTrue(expected in resp.data)
        self.assertEqual(resp.status_code, 200)

    @patch("app.send_from_directory")
    @patch("app.os.path.isfile")
    @patch("app.generate_spreadsheet")
    def test_post_response_from_index_page(self, mock_speadsheet, mock_is_file, mock_send):
        # Verify that a spreadsheet has been exported.
        mock_speadsheet.return_value = "foo"
        mock_is_file.return_value = True
        mock_send.return_value = "bar"

        url = "/"
        data = {"team-name": "mock name"}
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
