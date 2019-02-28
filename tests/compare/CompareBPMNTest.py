import unittest
import os

from bpmn_python.bpmn_compare_similarity import CompareBPMN


class CompareBPMNTest(unittest.TestCase):
    """
    Test compare bpmn similarity
    """
    output_directory = "../compare_resource/output/"
    example_directory_1 = "../compare_resource/bpmn_file/"
    example_directory_2 = "../compare_resource/raw_bpmn_file/"

    def test_similarity_between_two_diagram(self):
        cb = CompareBPMN()
        cb.calculate_similarity(file_name1=os.path.abspath(self.example_directory_1 + "1.xml"),
                                file_name2=os.path.abspath(self.example_directory_2 + "1.xml"))

    def test_similarity_between_two_directory(self):
        cb = CompareBPMN(export_csv=True, export_excel=False)
        cb.calculate_batch_similarity(bpmn_file_path1=os.path.abspath(self.example_directory_1),
                                      bpmn_file_path2=os.path.abspath(self.example_directory_2),
                                      output_dir=os.path.abspath(self.output_directory)
                                      )
