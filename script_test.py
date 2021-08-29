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
            "participants/connie-karras/20210829-Region12Running_Karras_loggedActivities.csv"
        ]
        self.assertListEqual(
            script.sort_files_by_region("Connie Karras"), 
            expected
        )
    

    def test_that_participant_information_is_properly_formatted(self):
        expected = [
            'Karras, Connie', 
            442.71, 
            418.51, 
            513.05, 
            611.71, 
            470.31, 
            408.6, 
            436.63, 
            186.51, 
            272.41, 
            248.56, 
            290.56, 
            10.75
        ]

        data = script.sort_files_by_region("Connie Karras")

        self.assertListEqual(
            script.format_participant_data("Connie Karras", data), 
            expected
        )


    @skip
    def test_that_total_milleage_is_calculated_well(self):
        expected = 4310.31
        # self.assertEqual()


if __name__ == "__main__":
    unittest.main()