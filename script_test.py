import unittest
from unittest.case import skip
import script
import requests

class TestScript(unittest.TestCase):
    maxDiff = None # make failing tests easier to debug

    def test_that_files_are_properly_sorted_by_region(self): 
        expected = [   
            "participants/connie-karras/20210829-Region1Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210829-Region2Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210829-Region3Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210829-Region4Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210829-Region5Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210829-Region6Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210829-Region7Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210829-Region8Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210829-Region9Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210829-Region10Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210829-Region11Running_Karras_loggedActivities.csv",
            "participants/connie-karras/20210907-Region12Running_Karras_loggedActivities.csv"
        ]
        self.assertListEqual(
            script.sort_files_by_region("Connie Karras"), 
            expected
        )


    def test_that_files_are_properly_sorted_by_region2(self):
        expected = [   
            "participants/joshua-fosberg/20210824-Region1Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210824-Region2Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210824-Region3Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210824-Region4Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210824-Region5Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210824-Region6Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210824-Region7Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210824-Region8Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210824-Region9Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210824-Region10Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210824-Region11Running_Fosberg_loggedActivities.csv",
            "participants/joshua-fosberg/20210907-Region12Running_Fosberg_loggedActivities.csv"
        ] 
        self.assertListEqual(
            script.sort_files_by_region("Joshua Fosberg"), 
            expected
        )


    def test_that_participant_information_is_properly_formatted(self):
        expected = [
            "Connie Karras", 
            442.71, 
            418.51, 
            513.05, 
            611.71, 
            470.31, 
            408.6, 
            436.63,
            272.41, 
            186.51, 
            248.56, 
            290.56, 
            14.06
        ]

        data = script.sort_files_by_region("Connie Karras")

        self.assertListEqual(
            script.format_participant_data("Connie Karras", data), 
            expected
        )


    def test_that_participant_information_is_properly_formatted(self):
        expected = [
            "Joshua Fosberg", 
            0, 
            0, 
            234.72, 
            247.23, 
            154.7, 
            116.4, 
            61.08,
            98.68, 
            308.57, 
            407.1, 
            242.28, 
            136.85
        ]

        data = script.sort_files_by_region("Joshua Fosberg")

        self.assertListEqual(
            script.format_participant_data("Joshua Fosberg", data), 
            expected
        )


    @skip
    def test_that_total_milleage_is_calculated_well(self):
        expected = 4310.31
        # self.assertEqual()


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


    def test_get_participant_data_func(self):
        participant_names, monthly_mileage_results, participant_identifiers \
        = script.get_participant_data()

        results_to_test = [
            # tuples contain two elements: given result, expected result.
            (
                participant_names,
                {
                    'David E', 'Steven K', 'Zack L', 'Zachary L', 'Frank B', \
                    'Sketch D', 'Tim P', 'Ashley B', 'David R', 'Phil E', \
                    'Salley H', 'Norm W', 'Joshua F', 'Connie K', 'Shawn R', \
                    'James H', 'Micha S','David R', 'Chris H', 'Don W'
                }
            ),
            (
                monthly_mileage_results,
                {
                    1: {
                            'Connie K': 442.71,
                            'David R': 348.87,
                            'David E': 381.96,
                            'Steven K': 149.36,
                            'Zachary L': 363.21,
                            'Ashley B': 162.26,
                            'Norm W': 91.25,
                            'Tim P': 250.75,
                            'Shawn R': 241.91,
                            'Phil E': 79.743
                        },

                    11: {
                            'Zack L': 294.77,
                            'Don W': 345.23,
                            'Connie K': 290.56,
                            'David R': 376.09,
                            'David E': 422.12,
                            'Joshua F': 242.28,
                            'Salley H': 359.25,
                            'James H': 85.21,
                            'Sketch D': 269.49
                        },

                    10: {
                            'Zachary L': 311.39,
                            'Salley H': 350.61,
                            'Connie K': 248.56,
                            'David R': 293.94,
                            'David E': 324.82,
                            'Joshua F': 407.1,
                            'James H': 240.16,
                            'Don W': 296.29,
                            'Sketch D': 225.63
                        },

                    9: {'Zachary L': 281.88, 'Connie K': 186.51, 'David R': 256.89, 'Salley H': 275.59, 'David E': 250.24, 'Don W': 291.48, 'Sketch D': 278.86, 'Joshua F': 308.57, 'James H': 188.98},
                    8: {'Connie K': 272.41, 'David R': 195.3, 'Phil E': 10.24, 'Sketch D': 173.41, 'Salley H': 218.62, 'James H': 80.83, 'David E': 150.04, 'Don W': 221.49, 'Zachary L': 239.98, 'Joshua F': 98.68},
                    7: {'Zack L': 233.36, 'Salley H': 278.68, 'Don W': 265.75, 'Joshua F': 61.08, 'Connie K': 436.63, 'Phil E': 48.604, 'David R': 188.13, 'David E': 236.28, 'Sketch D': 164.14, 'James H': 76.35},
                    6: {'Zachary L': 250.66, 'Connie K': 408.6, 'Phil E': 47.38, 'Salley H': 287.52, 'Don W': 333.597, 'James H': 119.1, 'David E': 256.74, 'Joshua F': 116.4, 'David R': 227.29, 'Sketch D': 40.75},
                    5: {'Zachary L': 283.47, 'Connie K': 470.31, 'Frank B': 255.67, 'Don W': 443.21, 'David R': 172.07, 'Salley H': 287.01, 'James H': 151.7, 'Sketch D': 199.29, 'Joshua F': 154.7, 'David E': 220.57},
                    4: {'Zachary L': 355.02, 'Connie K': 611.71, 'David R': 227.06, 'James H': 209.25, 'Don W': 533.474, 'David E': 204.64, 'Joshua F': 247.23, 'Salley H': 487.7, 'Sketch D': 200.29, 'Micha S': 219.63},
                    3: {'Zack L': 300.09, 'Connie K': 513.05, 'James H': 195.12, 'Don W': 447.329, 'Joshua F': 234.72, 'David E': 261.24, 'Salley H': 427.57, 'Chris H': 266.3, 'Sketch D': 236.83, 'David R': 290.85},
                    2: {'Zachary L': 290.56, 'Connie K': 418.51, 'David R': 284.77, 'David E': 290.61, 'Ashley B': 242.43, 'Tim P': 206.16, 'Don W': 421.369, 'Chris H': 252.952, 'Salley H': 380.77, 'Sketch D': 305.89},
                    12: {'Connie K': 14.06, 'Zack L': 271.38, 'David R': 301.25, 'David E': 379.11, 'Don W': 180.21, 'Sketch D': 193.55, 'James H': 138.35, 'Phil E': 96.554, 'Salley H': 345.73, 'Joshua F': 136.85}
                }
            ),
            (
                participant_identifiers,
                [
                    ('Connie K', 'F', '54'),
                    ('David R', 'M', '75'),
                    ('David E', 'M', '50'),
                    ('Steven K', 'M', '36'),
                    ('Zachary L', 'M', '47'),
                    ('Ashley B', 'F', '37'),
                    ('Norm W', 'M', '58'),
                    ('Tim P', 'M', '41'),
                    ('Shawn R', 'M', '39'),
                    ('Phil E', 'M', '58'),
                    ('Zack L', 'M', '48'),
                    ('Don W', 'M', '55'),
                    ('Joshua F', 'M', '33'),
                    ('Salley H', 'F', '55'),
                    ('James H', 'M', '49'),
                    ('Sketch D', 'M', '43'),
                    ('Frank B', 'M', '76'),
                    ('Micha S', 'F', '49'),
                    ('Chris H', 'M', '36')
                ]
            )
        ]

        with self.subTest(self):
            for result, expected in results_to_test:
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()