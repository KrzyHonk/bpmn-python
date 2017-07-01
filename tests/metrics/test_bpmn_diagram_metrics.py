# coding=utf-8
"""
Unit tests to test the complexity metrics implemented of BPMN models
"""
import os
import unittest

from bpmn_python import bpmn_diagram_metrics as metrics
from bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph


class BPMNComplexityMetricsTests(unittest.TestCase):

    def setUp(self):

        self.models = {name: BpmnDiagramGraph()
                       for name in ['SIMPLE', 'COMPLEX', 'WITH_CYCLES', 'WITH_CROSSING_POINT']
                       }

        self.models['SIMPLE'].load_diagram_from_xml_file(
            os.path.abspath("../examples/xml_import_export/bpmn_editor_simple_example.xml")),
        self.models['COMPLEX'].load_diagram_from_xml_file(
            os.path.abspath("../examples/xml_import_export/camunda_complex_example.bpmn")),
        self.models['WITH_CYCLES'].load_diagram_from_xml_file(
            os.path.abspath("../examples/metrics/cycles_test.bpmn")),
        self.models['WITH_CROSSING_POINT'].load_diagram_from_xml_file(
            os.path.abspath("../examples/metrics/crossing_point_test.bpmn")),

    def testTNSEMetricForSimpleModel(self):

        self.assertEqual(
            metrics.TNSE_metric(self.models['SIMPLE']), 1
        )

    def testTNSEMetricForComplexModel(self):

        self.assertEqual(
            metrics.TNSE_metric(self.models['COMPLEX']), 1
        )

    def testTNSEForModelWithCycles(self):

        self.assertEqual(
            metrics.TNSE_metric(self.models['WITH_CYCLES']), 1
        )

    def testTNSEForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.TNSE_metric(self.models['WITH_CROSSING_POINT']), 1
        )

    def testTNIEMetricForSimpleModel(self):

        self.assertEqual(
            metrics.TNIE_metric(self.models['SIMPLE']), 0
        )

    def testTNIEMetricForComplexModel(self):

        self.assertEqual(
            metrics.TNIE_metric(self.models['COMPLEX']), 2
        )

    def testTNIEForModelWithCycles(self):

        self.assertEqual(
            metrics.TNIE_metric(self.models['WITH_CYCLES']), 0
        )

    def testTNIEForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.TNIE_metric(self.models['WITH_CROSSING_POINT']), 0
        )

    def testTNEEMetricForSimpleModel(self):

        self.assertEqual(
            metrics.TNEE_metric(self.models['SIMPLE']), 1
        )

    def testTNEEMetricForComplexModel(self):

        self.assertEqual(
            metrics.TNEE_metric(self.models['COMPLEX']), 1
        )

    def testTNEEForModelWithCycles(self):

        self.assertEqual(
            metrics.TNEE_metric(self.models['WITH_CYCLES']), 2
        )

    def testTNEEForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.TNEE_metric(self.models['WITH_CROSSING_POINT']), 1
        )

    def testTNEMetricForSimpleModel(self):

        self.assertEqual(
            metrics.TNE_metric(self.models['SIMPLE']), 2
        )

    def testTNEMetricForComplexModel(self):

        self.assertEqual(
            metrics.TNE_metric(self.models['COMPLEX']), 4
        )

    def testTNEForModelWithCycles(self):

        self.assertEqual(
            metrics.TNE_metric(self.models['WITH_CYCLES']), 3
        )

    def testTNEForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.TNE_metric(self.models['WITH_CROSSING_POINT']), 2
        )

    def testNOAMetricForSimpleModel(self):

        self.assertEqual(
            metrics.NOA_metric(self.models['SIMPLE']), 4
        )

    def testNOAMetricForComplexModel(self):

        self.assertEqual(
            metrics.NOA_metric(self.models['COMPLEX']), 9
        )

    def testNOAMetricForModelWithCycles(self):
        self.assertEqual(
            metrics.NOA_metric(self.models['WITH_CYCLES']), 11
        )

    def testNOAMetricForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.NOA_metric(self.models['WITH_CROSSING_POINT']), 3
        )

    def testNOACMetricForSimpleModel(self):
        self.assertEqual(
            metrics.NOAC_metric(self.models['SIMPLE']), 8
        )

    def testNOACMetricForComplexModel(self):
        self.assertEqual(
            metrics.NOAC_metric(self.models['COMPLEX']), 21
        )

    def testNOACMetricForModelWithCycles(self):
        self.assertEqual(
            metrics.NOAC_metric(self.models['WITH_CYCLES']), 16
        )

    def testNOACMetricForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.NOAC_metric(self.models['WITH_CROSSING_POINT']), 7
        )

    def testNOAJSMetricForSimpleModel(self):
        self.assertEqual(
            metrics.NOAJS_metric(self.models['SIMPLE']), 6
        )

    def testNOAJSMetricForComplexModel(self):
        self.assertEqual(
            metrics.NOAJS_metric(self.models['COMPLEX']), 17
        )

    def testNOAJSMetricForModelWithCycles(self):
        self.assertEqual(
            metrics.NOAJS_metric(self.models['WITH_CYCLES']), 13
        )

    def testNOAJSMetricForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.NOAJS_metric(self.models['WITH_CROSSING_POINT']), 5
        )

    def testNumberOfNodesForSimpleModel(self):

        self.assertEqual(
            metrics.NumberOfNodes_metric(self.models['SIMPLE']), 8
        )

    def testNumberOfNodesForComplexModel(self):

        self.assertEqual(
            metrics.NumberOfNodes_metric(self.models['COMPLEX']), 21
        )

    def testNumberOfNodesForModelWithCycles(self):
        self.assertEqual(
            metrics.NumberOfNodes_metric(self.models['WITH_CYCLES']), 16
        )

    def testNumberOfNodesForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.NumberOfNodes_metric(self.models['WITH_CROSSING_POINT']), 7
        )

    def testGatewayHeterogenityMetricForSimpleModel(self):

        self.assertEqual(
            metrics.GatewayHeterogenity_metric(self.models['SIMPLE']), 1
        )

    def testGatewayHeterogenityMetricForComplexModel(self):

        self.assertEqual(
            metrics.GatewayHeterogenity_metric(self.models['COMPLEX']), 4
        )

    def testGatewayHeterogenityMetricForModelWithCycles(self):
        self.assertEqual(
            metrics.GatewayHeterogenity_metric(self.models['WITH_CYCLES']), 1
        )

    def testGatewayHeterogenityMetricForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.GatewayHeterogenity_metric(self.models['WITH_CROSSING_POINT']), 1
        )

    def testCoefficientOfNetworkComplexityMetricForSimpleModel(self):

        self.assertAlmostEqual(
            metrics.CoefficientOfNetworkComplexity_metric(self.models['SIMPLE']), 1.0,
            places=3
        )

    def testCoefficientOfNetworkComplexityMetricForComplexModel(self):

        self.assertAlmostEqual(
            metrics.CoefficientOfNetworkComplexity_metric(self.models['COMPLEX']), 1.143,
            places=3
        )

    def testCoefficientOfNetworkComplexityMetricForModelWithCycles(self):
        self.assertAlmostEqual(
            metrics.CoefficientOfNetworkComplexity_metric(self.models['WITH_CYCLES']), 1.0,
            places=3
        )

    def testCoefficientOfNetworkComplexityMetricForModelWithCrossingPoint(self):
        self.assertAlmostEqual(
            metrics.CoefficientOfNetworkComplexity_metric(self.models['WITH_CROSSING_POINT']), 1.0
        )

    def testAverageGatewayDegreeMetricForSimpleModel(self):

        self.assertAlmostEqual(
            metrics.AverageGatewayDegree_metric(self.models['SIMPLE']), 3.0,
            places=3
        )

    def testAverageGatewayDegreeMetricForComplexModel(self):

        self.assertAlmostEqual(
            metrics.AverageGatewayDegree_metric(self.models['COMPLEX']), 3.0,
            places=3
        )

    def testAverageGatewayDegreeForModelWithCycles(self):
        self.assertAlmostEqual(
            metrics.AverageGatewayDegree_metric(self.models['WITH_CYCLES']), 3.5,
            places=3
        )

    def testAverageGatewayDegreeForModelWithCrossingPoint(self):
        self.assertAlmostEqual(
            metrics.AverageGatewayDegree_metric(self.models['WITH_CROSSING_POINT']), 3.0
        )

    def testDurfeeSquareMetricForSimpleModel(self):

        self.assertEqual(
            metrics.DurfeeSquare_metric(self.models['SIMPLE']), 2
        )

    def testDurfeeSquareMetricForComplexModel(self):

        self.assertEqual(
            metrics.DurfeeSquare_metric(self.models['COMPLEX']), 2
        )

    def testDurfeeSquareForModelWithCycles(self):

        self.assertEqual(
            metrics.DurfeeSquare_metric(self.models['WITH_CYCLES']), 2
        )

    def testDurfeeSquareForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.DurfeeSquare_metric(self.models['WITH_CROSSING_POINT']), 2
        )

    def testPerfectSquareMetricForSimpleModel(self):

        self.assertEqual(
            metrics.PerfectSquare_metric(self.models['SIMPLE']), 2
        )

    def testPerfectSquareMetricForComplexModel(self):

        self.assertEqual(
            metrics.PerfectSquare_metric(self.models['COMPLEX']), 3
        )

    def testPerfectSquareForModelWithCycles(self):

        self.assertEqual(
            metrics.PerfectSquare_metric(self.models['WITH_CYCLES']), 4
        )

    def testPerfectSquareForModelWithCrossingPoint(self):
        self.assertEqual(
            metrics.PerfectSquare_metric(self.models['WITH_CROSSING_POINT']), 2
        )

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
