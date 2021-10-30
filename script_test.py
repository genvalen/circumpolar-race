import unittest
from unittest.case import skip
import script
import requests

class TestScript(unittest.TestCase):
    maxDiff = None # make failing tests easier to debug

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


    @skip("WIP")
    def test_api_call(self):
        url = "https://runsignup.com/Race/Results/95983/LookupParticipant/?resultSetId=212380&userId=44542375#U44542375"
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Accept' : 'application/json, */*; q=0.01',
            'Accept-Language' : 'en-US,en;q=0.5',
            'X-Requested-With' : 'XMLHttpRequest',
            'Connection' : 'keep-alive',
            'Referer' : f'https://runsignup.com/Race/Results/95983/IndividualResult/?resultSetId=212380',
            'Cookie' : 'winWidth=1680; _ga=GA1.2.279797247.1629283759; __atuvc=128%7C36%2C6%7C37%2C11%7C38%2C38%7C39%2C4%7C40; cookie_policy_accepted=T; analytics={"asset":"a1ca985c-904e-459a-bfd7-7480afe5b588","source":1,"medium":1}; PHPSESSID=9r2ImrtyrSszLIsWF2YCV3widCfGI9RJ; _mkto_trk=id:350-KBZ-109&token:_mch-runsignup.com-1632559648074-71989; _gid=GA1.2.2082540081.1633160300; __atuvs=615a3572229b618f002',
        }

        expected = {
            "participants":[
                {
                    "user_id":44542375,
                    "first_name":"Connie",
                    "last_name":"Karras",
                    "event_id":420484,
                    "event":"Region 1 - Running",
                    "bib_num":"2164",
                    "profile_filename_url":None,
                    "registration_id":45016484,
                    "digitalBibUrl":"/Race\/Public\/Certificates\/PreRaceBib\/CHH\/AnywhereAnyPlace\/CircumpolarRaceAroundtheWorld?registrationId=45016484",
                    "gender":"F",
                    "age":54,
                    "city":"Munster",
                    "state":"IN"
                }
            ]
        }

        self.assertEqual(requests.get(url, headers=headers).json(), expected)


    def test_get_identifiers_func(self):
        path = '/Race/Results/95983/IndividualResult/?resultSetId=212380#U44542375'
        expected = ('Connie', 'Karras', 'F', 54, 'Munster', 'IN')

        self.assertEqual(
            script.get_identifiers(path),
            expected
        )


    def test_get_miles_func(self):
        path = "/Race/Results/95983/IndividualResult/?resultSetId=212380#U44542375"
        expected = 442.71

        self.assertEqual(
            script.get_miles(path),
            expected
        )

    def test_that_edit_distance_algo_returns_correct_similarity_value(self):
        # Testcase tuples:
        # (str1, str2, expected_result)
        testcases = [
            ("cat", "can", 1),
            ("", "cat", 3),
            ("walrus", "", 6),
            ("walrus", "walnut", 2),
            ("fizzy", "frizzy", 1),
            ("bonniekarras54MunsterIN", "conniekarras53MunsterIN", 2),
            ("conniekarras54MunsterIN", "Conniekarras53MunsterIN", 1),
            ("JohnSmithM48IndianMoundTN", "JanetRodriguezF50IndianMoundTN", 11)
        ]

        for str1, str2, expected in testcases:
            with self.subTest(f"\"{str1}\", \"{str2}\" -> {expected}"):
                self.assertEqual(
                    script.edit_distance(str1, str2),
                    expected
                )


    @skip("WIP")
    def test_that_entity_resolution_recognizes_two_people_are_the_same(self):
        pass


    def test_get_participant_data_func(self):
        participant_names, monthly_mileage_results, participant_identifiers \
        = script.get_participant_data()

        results_to_test = [
            # tuples contain two elements: given result, expected result.
            (
                participant_names,
                {
                    'David Eckardt',
                    'Steven Kornhaus',
                    'Zack Lever',
                    'Zachary Lever',
                    'Frank Bozanich',
                    'Sketch Ditty',
                    'Tim Post',
                    'Ashley Blake',
                    'David Ralston',
                    'Phil Essam',
                    'Salley Hernandez',
                    'Norm Williams',
                    'Joshua Fosberg',
                    'Connie Karras',
                    'Shawn Roberts',
                    'James Huller',
                    'Micha Shines',
                    'Chris Head',
                    'Don Willis'
                }
            ),
            (
                monthly_mileage_results,
                {
                    1: {
                            'Connie Karras': 442.71,
                            'David Ralston': 348.87,
                            'David Eckardt': 381.96,
                            'Steven Kornhaus': 149.36,
                            'Zachary Lever': 363.21,
                            'Ashley Blake': 162.26,
                            'Norm Williams': 91.25,
                            'Tim Post': 250.75,
                            'Shawn Roberts': 241.91,
                            'Phil Essam': 79.743
                        },

                    11: {
                            'Zack Lever': 294.77,
                            'Don Willis': 345.23,
                            'Connie Karras': 290.56,
                            'David Ralston': 376.09,
                            'David Eckardt': 422.12,
                            'Joshua Fosberg': 242.28,
                            'Salley Hernandez': 359.25,
                            'James Huller': 85.21,
                            'Sketch Ditty': 269.49
                        },

                    10: {
                            'Zachary Lever': 311.39,
                            'Salley Hernandez': 350.61,
                            'Connie Karras': 248.56,
                            'David Ralston': 293.94,
                            'David Eckardt': 324.82,
                            'Joshua Fosberg': 407.1,
                            'James Huller': 240.16,
                            'Don Willis': 296.29,
                            'Sketch Ditty': 225.63
                        },

                    9: {
                            'Zachary Lever': 281.88,
                            'Connie Karras': 186.51,
                            'David Ralston': 256.89,
                            'Salley Hernandez': 275.59,
                            'David Eckardt': 250.24,
                            'Don Willis': 291.48,
                            'Sketch Ditty': 278.86,
                            'Joshua Fosberg': 308.57,
                            'James Huller': 188.98
                        },

                    8: {
                            'Connie Karras': 272.41,
                            'David Ralston': 195.3,
                            'Phil Essam': 10.24,
                            'Sketch Ditty': 173.41,
                            'Salley Hernandez': 218.62,
                            'James Huller': 80.83,
                            'David Eckardt': 150.04,
                            'Don Willis': 221.49,
                            'Zachary Lever': 239.98,
                            'Joshua Fosberg': 98.68
                        },

                    7: {
                            'Zack Lever': 233.36,
                            'Salley Hernandez': 278.68,
                            'Don Willis': 265.75,
                            'Joshua Fosberg': 61.08,
                            'Connie Karras': 436.63,
                            'Phil Essam': 48.604,
                            'David Ralston': 188.13,
                            'David Eckardt': 236.28,
                            'Sketch Ditty': 164.14,
                            'James Huller': 76.35
                        },

                    6: {
                            'Zachary Lever':250.66,
                            'Connie Karras': 408.6,
                            'Phil Essam': 47.38,
                            'Salley Hernandez': 287.52,
                            'Don Willis': 333.597,
                            'James Huller': 119.1,
                            'David Eckardt': 256.74,
                            'Joshua Fosberg': 116.4,
                            'David Ralston': 227.29,
                            'Sketch Ditty': 40.75
                        },

                    5: {
                            'Zachary Lever': 283.47,
                            'Connie Karras': 470.31,
                            'Frank Bozanich': 255.67,
                            'Don Willis': 443.21,
                            'David Ralston': 172.07,
                            'Salley Hernandez': 287.01,
                            'James Huller': 151.7,
                            'Sketch Ditty': 199.29,
                            'Joshua Fosberg': 154.7,
                            'David Eckardt': 220.57
                        },

                    4: {
                            'Zachary Lever': 355.02,
                            'Connie Karras': 611.71,
                            'David Ralston': 227.06,
                            'James Huller': 209.25,
                            'Don Willis': 533.474,
                            'David Eckardt': 204.64,
                            'Joshua Fosberg': 247.23,
                            'Salley Hernandez': 487.7,
                            'Sketch Ditty': 200.29,
                            'Micha Shines': 219.63
                        },

                    3: {
                            'Zack Lever': 300.09,
                            'Connie Karras': 513.05,
                            'James Huller': 195.12,
                            'Don Willis': 447.329,
                            'Joshua Fosberg': 234.72,
                            'David Eckardt': 261.24,
                            'Salley Hernandez': 427.57,
                            'Chris Head': 266.3,
                            'Sketch Ditty': 236.83,
                            'David Ralston': 290.85
                        },

                    2: {
                            'Zachary Lever': 290.56,
                            'Connie Karras': 418.51,
                            'David Ralston': 284.77,
                            'David Eckardt': 290.61,
                            'Ashley Blake': 242.43,
                            'Tim Post': 206.16,
                            'Don Willis': 421.369,
                            'Chris Head': 252.952,
                            'Salley Hernandez': 380.77,
                            'Sketch Ditty': 305.89
                        },

                    12: {
                            'Connie Karras': 14.06,
                            'Zack Lever': 271.38,
                            'David Ralston': 301.25,
                            'David Eckardt': 379.11,
                            'Don Willis': 180.21,
                            'Sketch Ditty': 193.55,
                            'James Huller': 138.35,
                            'Phil Essam': 96.554,
                            'Salley Hernandez': 345.73,
                            'Joshua Fosberg': 136.85
                        }
                }
            ),
            (
                participant_identifiers,
                [
                    ('Connie', 'Karras', 'F', 54, 'Munster', 'IN'),
                    ('David', 'Ralston', 'M', 75, 'Hammond', 'IN'),
                    ('David', 'Eckardt', 'M', 50, 'Evansville', 'IN'),
                    ('Steven', 'Kornhaus', 'M', 36, 'Deer Lodge', 'TN'),
                    ('Zachary', 'Lever', 'M', 47, 'Indian Mound', 'TN'),
                    ('Ashley', 'Blake', 'F', 37, 'Oak Ridge', 'TN'),
                    ('Norm', 'Williams', 'M', 58, 'Portage', 'IN'),
                    ('Tim', 'Post', 'M', 41, 'Chesterton', 'IN'),
                    ('Shawn', 'Roberts', 'M', 39, 'Clemmon', 'NC'),
                    ('Phil', 'Essam', 'M', 58, 'Casey', None),
                    ('Zack', 'Lever', 'M', 48, 'Indian Mound', 'TN'),
                    ('Don', 'Willis', 'M', 55, 'Bentonville', 'AR'),
                    ('Joshua', 'Fosberg', 'M', 33, 'Virginia Beach', 'VA'),
                    ('Salley', 'Hernandez', 'F', 55, 'Atoka', 'TN'),
                    ('James', 'Huller', 'M', 49, 'Jacksonville', 'NC'),
                    ('Sketch', 'Ditty', 'M', 43, 'Canton', 'GA'),
                    ('Frank', 'Bozanich', 'M', 76, 'Reno', 'NV'),
                    ('Micha', 'Shines', 'F', 49, 'Alexandria', 'VA'),
                    ('Chris', 'Head', 'M', 36, 'Molena', 'GA')
                ]
            )
        ]

        for result, expected in results_to_test:
            with self.subTest("Output order is \"result\" -> \"expected\""):
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()