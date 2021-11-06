import unittest
from unittest.mock import patch
import script

class TestScript(unittest.TestCase):
    maxDiff = None # make failing tests easier to debug


    # makes API calls
    def test_get_region_paths_func(self):
        expected = {
            1: '/RaceGroups/95983/Groups/802853',
            11: '/RaceGroups/95983/Groups/894183',
            10: '/RaceGroups/95983/Groups/894182',
            9: '/RaceGroups/95983/Groups/894181',
            8: '/RaceGroups/95983/Groups/894180',
            7: '/RaceGroups/95983/Groups/894179',
            6: '/RaceGroups/95983/Groups/861224',
            5: '/RaceGroups/95983/Groups/855643',
            4: '/RaceGroups/95983/Groups/843369',
            3: '/RaceGroups/95983/Groups/832629',
            2: '/RaceGroups/95983/Groups/813501',
            12: '/RaceGroups/95983/Groups/894184'
        }

        self.assertDictEqual(
            script.get_region_paths(),
            expected
        )


    @patch("script.requests.get")
    def test_info_returned_by_get_identifiers_is_correct(self, mock_get):
        input_href = "mock/href/query/?resultSetId=212380#U44542375"
        expected = ("Lin Manuel", "Miranda", "M", 54, "Munster", "IN")
        mock_json_response = {
            "participants":[
                {
                    "user_id":44542375,
                    "first_name":"Lin Manuel",
                    "last_name":"Miranda",
                    "event_id":420484,
                    "event":"Region 1 - Running",
                    "bib_num":"2164",
                    "profile_filename_url":None,
                    "registration_id":45016484,
                    "gender":"M",
                    "age":54,
                    "city":"Munster",
                    "state":"IN"
                }
            ]
        }

        # Configue Mock object's return value.
        mock_get.return_value.json.return_value = mock_json_response

        # Assertion.
        self.assertEqual(
            script.get_identifiers(input_href),
            expected
        )


    @patch("script.requests.post")
    def test_miles_returned_by_get_miles_is_correct(self, mock_post):
        input_href = "mock/href/query//?resultSetId=212380#U44542375"
        expected = 442.71
        mock_json_response = {
            "mock_key1":{},
            "mock_key2":{},
            "results":[
                {
                    "result_tally_value":442.71,
                    "result_tally_label":"Distance in Miles",
                    "result_tally_value_in_meters":712472.683,

                }
            ]
        }

        # Configue Mock object's return value.
        mock_post.return_value.json.return_value = mock_json_response

        # Assertion.
        self.assertEqual(
            script.get_miles(input_href),
            expected
        )


    @patch("script.get_identifiers")
    @patch("script.get_miles")
    @patch("script.get_bs4_soup")
    @patch("script.get_region_paths")
    def test_data_is_organized_correctly_by_get_participant_data(self, mock_region_paths, mock_soup, mock_miles, mock_id):
        import MockBs4Objs

        # Configure mock return value.
        mock_region_paths.return_value = {
            1: 'mock/RaceGroups/95983/Groups/802853',
            2: 'mock/RaceGroups/95983/Groups/894183',
            3: 'mock/RaceGroups/95983/Groups/894182',
            4: 'mock/RaceGroups/95983/Groups/894181',
            5: 'mock/RaceGroups/95983/Groups/894180',
            6: 'mock/RaceGroups/95983/Groups/894179',
            7: 'mock/RaceGroups/95983/Groups/861224',
            8: 'mock/RaceGroups/95983/Groups/855643',
            9: 'mock/RaceGroups/95983/Groups/843369',
            10: 'mock/RaceGroups/95983/Groups/832629',
            11: 'mock/RaceGroups/95983/Groups/813501',
            12: 'mock/RaceGroups/95983/Groups/894184'
        }

        # Configure mock side-effects.
        #   * Split 2 sets of mock HTML between 12 regions.
        #   * Scrape HTML 1 for data on 2 participants.
        #   * Scrape HTML 2 for data on 3 participants.
        #   * Mock HTTP resp. for mile results of each participant (5 results).
        #   * Mock HTTP resp. for ID of each unique participant (4 unique).
        #       - note: should be 3 unique, but there is entity resolution issue.

        mock_sp1, mock_sp2 = MockBs4Objs.bs4_objs
        mock_soup.side_effect = [mock_sp1, mock_sp2] * 6
        mock_miles.side_effect = [100.50, 200.50, 300.50, 400.50, 80.50] * 6
        mock_id.side_effect = [
            ("Christopher", "Jackson", "M", 47, "Indian Mound", "TN"),
            ("Karen", "Olivo", "F", 54, "Munster", "IN"),
            ("Chris", "Jackson", "M", 48, "Indian Mound", "TN"),
            ("Jonathon", "Groff", "M", 58, "Portage", "IN"),
        ]

        # TESTS->
        # Test data structure returned by get_participant_data.
        participant_names, monthly_mileage_results, participant_identifiers \
        = script.get_participant_data()

        results_to_test = [
            # tuples contain: given result, expected result.
            (
                participant_names,
                {
                    'Chris Jackson',
                    'Christopher Jackson',
                    'Jonathon Groff',
                    'Karen Olivo',
                }
            ),
            (
                monthly_mileage_results,
                {
                    1: {
                            'Christopher Jackson': 100.50,
                            'Karen Olivo': 200.50,
                        },
                    2: {
                            'Chris Jackson': 300.50,
                            'Karen Olivo': 400.50,
                            'Jonathon Groff': 80.50,
                        },
                    3: {
                            'Christopher Jackson': 100.50,
                            'Karen Olivo': 200.50,
                        },
                    4: {
                            'Chris Jackson': 300.50,
                            'Karen Olivo': 400.50,
                            'Jonathon Groff': 80.50,
                        },
                    5: {
                            'Christopher Jackson': 100.50,
                            'Karen Olivo': 200.50,
                        },
                    6: {
                            'Chris Jackson': 300.50,
                            'Karen Olivo': 400.50,
                            'Jonathon Groff': 80.50,
                        },
                    7: {
                            'Christopher Jackson': 100.50,
                            'Karen Olivo': 200.50,
                        },
                    8: {
                            'Chris Jackson': 300.50,
                            'Karen Olivo': 400.50,
                            'Jonathon Groff': 80.50,
                        },
                    9: {
                            'Christopher Jackson': 100.50,
                            'Karen Olivo': 200.50,
                        },
                    10: {
                            'Chris Jackson': 300.50,
                            'Karen Olivo': 400.50,
                            'Jonathon Groff': 80.50,
                        },
                    11: {
                            'Christopher Jackson': 100.50,
                            'Karen Olivo': 200.50,
                        },
                    12: {
                            'Chris Jackson': 300.50,
                            'Karen Olivo': 400.50,
                            'Jonathon Groff': 80.50,
                        },
                }
            ),
            (
                participant_identifiers,
                [
                    ("Christopher", "Jackson", "M", 47, "Indian Mound", "TN"),
                    ("Karen", "Olivo", "F", 54, "Munster", "IN"),
                    ("Chris", "Jackson", "M", 48, "Indian Mound", "TN"),
                    ("Jonathon", "Groff", "M", 58, "Portage", "IN"),
                ]
            )
        ]

        # Assertion.
        for result, expected in results_to_test:
            with self.subTest("\"result\" -> \"expected\""):
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
