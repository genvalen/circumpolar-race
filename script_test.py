import unittest
from unittest.case import skip
import script

class TestScript(unittest.TestCase):
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
        self.assertDictEqual(
            script.get_region_paths(),
            {
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
        )


if __name__ == "__main__":
    unittest.main()