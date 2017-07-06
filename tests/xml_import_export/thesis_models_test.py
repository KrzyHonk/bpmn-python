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

        with open(self.output_directory + "metrics", "w") as file:
            # write header
            file.write("Model name,Activities,Gateways\n")

            for model_name in names:
                bpmn_diagram = diagram.BpmnDiagramGraph()
                bpmn_diagram.load_diagram_from_xml_file(self.input_directory + model_name + ".bpmn")
                bpmn_diagram.export_xml_file(self.output_directory, model_name + "-output.bpmn")
                activities_count = metrics.all_activities_count(bpmn_diagram)
                gateways_count = metrics.all_gateways_count(bpmn_diagram)
                # metrics.all_control_flow_elements_count(bpmn_diagram)
                file.write(model_name + "," + str(activities_count) + "," + str(gateways_count) + "\n")

if __name__ == '__main__':
    unittest.main()
