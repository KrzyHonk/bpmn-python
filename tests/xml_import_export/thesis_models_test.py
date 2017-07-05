# coding=utf-8
"""
Test unit, using simple graph made in Signavio editor for import/export operation
"""
import unittest

import bpmn_python.bpmn_diagram_metrics as metrics
import bpmn_python.bpmn_diagram_rep as diagram


class ThesisModelsTests(unittest.TestCase):
    input_directory = "../examples/xml_import_export/thesis-models/"
    output_directory = "./output/thesis-models/"

    def test_thesis_models(self):
        names = [
            "model1",
            "model2",
            "model3",
            "model4",
            "model5",
            "model6",
            "model7",
            "model8",
            "model9",
            "model10",
            "model11",
            "model12",
            "model13",
            "model14",
            "model15",
            "model16",
            "model17",
            "model18",
            "model19",
            "model20",
            "model21",
            "model22",
            "model23"
        ]

        for model_name in names:
            print(model_name)
            hand_made_bpmn = diagram.BpmnDiagramGraph()
            hand_made_bpmn.load_diagram_from_xml_file(self.input_directory + model_name + ".bpmn")
            hand_made_bpmn.export_xml_file(self.output_directory, model_name + "-output.bpmn")
            metrics.all_activities_count(hand_made_bpmn)
            metrics.all_gateways_count(hand_made_bpmn)
            # metrics.all_control_flow_elements_count(hand_made_bpmn)

if __name__ == '__main__':
    unittest.main()
