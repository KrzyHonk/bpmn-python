"""
Comparing the Similarity of Two BPMN Graphs
Implementation for Paper:
Similarity of business process models: Metrics and evaluation
"""

from Levenshtein import distance
from bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph
import os
import pandas as pd

class CompareBPMN(object):
    def __init__(self, export_csv=False, export_excel=True):
        """
        Comparing the Similarity of Two BPMN Graphs

        Implementation for Paper:
        《Similarity of business process models: Metrics and evaluation》
        Address: https://kodu.ut.ee/~dumas/pubs/BetaWPSimilarity.pdf

        :param export_csv: If true, export export csv file as final result
        :param export_excel: If true, export export excel file as final result
        """
        self.export_csv = export_csv
        self.export_excel = export_excel
        self.result_list = []

    def get_bpmn_nodes(self, bpmn):
        """
        :param bpmn:
        :return:
        """
        nodes = bpmn.get_nodes()
        return nodes

    def get_bpmn_file_list(self, bpmn_file_path):
        """
        :param bpmn_file_path:
        :return:
        """
        file_list = os.listdir(bpmn_file_path)
        for file in file_list:
            if file.find('.xml') == -1 and file.find('.bpmn') == -1:
                file_list.remove(file)
        return file_list

    def get_bpmn_flows(self, bpmn):
        edges = bpmn.get_flows()
        # edges = list(filter(lambda x: x[0] not in start_end_node and x[1] not in start_end_node, edges))
        return edges

    def calculate_similarity(self, file_name1, file_name2):
        try:
            raw_bpmn = BpmnDiagramGraph()
            raw_bpmn.load_diagram_from_xml_file(file_name1)
            raw_nodes = self.get_bpmn_nodes(raw_bpmn)
            raw_edges = self.get_bpmn_flows(raw_bpmn)

            bpmn = BpmnDiagramGraph()
            bpmn.load_diagram_from_xml_file(file_name2)
            nodes = self.get_bpmn_nodes(bpmn)
            edges = self.get_bpmn_flows(bpmn)

            if len(nodes) > 0 and len(raw_nodes) > 0:
                # calculate node matching similarity
                node_matching_sim, equivalence_mapping = self.calculate_node_matching_similarity(raw_nodes,
                                                                                                 nodes)
                print("node matching similarity: between", file_name1, "and", file_name2, ":",
                      round(node_matching_sim, 3))
                # calculate structure similarity
                structure_sim = self.calculate_structure_similarity(raw_edges, raw_nodes, edges, nodes,
                                                                    equivalence_mapping)
                print("structure similarity: between", file_name1, "and", file_name2, ":",
                      round(structure_sim, 3))
                return node_matching_sim, structure_sim
            else:
                return 0, 0
        except BaseException as e:
            print("error in calculate similarity: ", e)
            raise e

    def calculate_batch_similarity(self, bpmn_file_path1, bpmn_file_path2, output_dir = ""):
        """
        Compute the similarity of all BPMN graphs under two folders
        Two files to compare are placed in different folders,
        but they must have [[[the same file name]]]

        :param bpmn_file_path1:
        :param bpmn_file_path2:
        :return:
        """

        self.__raw_bpmn_file_path = self.check_file_name(bpmn_file_path1)
        self.__bpmn_file_path = self.check_file_name(bpmn_file_path2)
        raw_bpmn_file_list = self.get_bpmn_file_list(self.__raw_bpmn_file_path)
        for bpmn_file in raw_bpmn_file_list:
            try:
                # file name must be same!!
                raw_file_name = os.path.join(self.__raw_bpmn_file_path + bpmn_file)
                file_name = self.__bpmn_file_path + bpmn_file
                node_matching_sim, structure_sim = self.calculate_similarity(raw_file_name, file_name)

                self.result_list.append((bpmn_file, node_matching_sim, structure_sim))
            except BaseException as e:
                print(e, bpmn_file)

        df = pd.DataFrame(self.result_list)
        df.sort_values(by=1, inplace=True, ascending=False)

        print("avg node matching similarity: ", df.iloc[:, 1].mean())
        print("avg structure similarity: ", df.iloc[:, 2].mean())

        df.columns = ['file_name', 'node_sim', 'structure_sim']
        df.reset_index()
        if self.export_csv:
            df.to_csv(os.path.join(output_dir, "result_sim.csv"))

        if self.export_excel:
            df.to_excel(os.path.join(output_dir + "result_sim.excel"))


    def check_file_name(self, file_name):
        if file_name[-1] != '/':
            return file_name + '/'
        else:
            return file_name

    def calculate_node_matching_similarity(self, raw_nodes, nodes):
        """
        compare similarity of two nodes
        Similarity is measured by text editing distance (Levenshtein Distance) and node type
        :param raw_nodes:
        :param nodes:
        :return:
        """
        col = list(map(lambda x: x[0], nodes))

        edit_distance_df = pd.DataFrame(columns=col)
        for raw_node in raw_nodes:
            edit_distance_list = [0] * len(nodes)
            edit_distance_list_df = pd.DataFrame([edit_distance_list], columns=col, index=[raw_node[0]])
            edit_distance_df = edit_distance_df.append(edit_distance_list_df)
            for node in nodes:
                # Syntactic Similarity
                syn_sim = self.get_syn_sim(raw_node, node)
                # Type Similarity
                type_sim = self.get_type_sim(raw_node, node)
                node_sim = syn_sim * type_sim
                edit_distance_df.loc[raw_node[0], node[0]] = node_sim
        # find best mapping for each node
        equivalence_mapping = self.calculate_equivalence_mapping(sim_data_frame=edit_distance_df)
        node_matching_sim = self.calculate_node_matching(equivalence_mapping, len(raw_nodes), len(nodes))

        return node_matching_sim, equivalence_mapping

    def get_syn_sim(self, node1, node2):
        """
        根据传入的节点返回句法相似性
        :param node1:
        :param node2:
        :return:
        """
        node1 = node1[1]['node_name']
        node2 = node2[1]['node_name']
        distance_val = distance(node1, node2)
        if len(node1) == 0 and len(node2) == 0:
            return 1
        else:
            syn_sim = 1 - distance_val / max(len(node1), len(node2))
            return syn_sim

    def get_type_sim(self, node1, node2):
        """
        Calculate type similarity
        :param node1:
        :param node2:
        :return:
        """
        node_type1 = node1[1]['type']
        node_type2 = node2[1]['type']

        return 1 if node_type1 == node_type2 else 0

    def calculate_equivalence_mapping(self, sim_data_frame):
        """
        Computing the Best Equivalent Mapping Based on the Input Similarity Matrix
        :param sim_data_frame:
        :return: Best Equivalent Mapping List of Nodes
        """
        df_shape = sim_data_frame.shape
        cols = list(sim_data_frame.columns.values)
        equivalence_mapping = []
        while df_shape[0] > 0 and df_shape[1] > 0:
            for col in cols:
                mapping_tupple = self.find_best_mapping(col, sim_data_frame)
                df_shape = sim_data_frame.shape
                if mapping_tupple[2] > 0:
                    equivalence_mapping.append(mapping_tupple)
                if mapping_tupple != (0, 0, 0):
                    cols.remove(mapping_tupple[0])
        return equivalence_mapping

    def calculate_node_matching(self, equivalence_mapping, raw_node_num, node_num):
        """
        Computing the final similarity of nodes according to the formulas in the paper
        :param equivalence_mapping: Best Equivalent Mapping List of Nodes
        :param raw_node_num:
        :param node_num:
        :return:
        """
        sum_sim = sum(map(lambda x: x[2], equivalence_mapping))
        return 2 * sum_sim / (raw_node_num + node_num)

    def find_best_mapping(self, col, sim_data_frame):
        """
        Find the best equivalence mapping for incoming nodes
        :param col:
        :param sim_data_frame:
        :return:
        """
        column_data = sim_data_frame.loc[:, col]
        if len(column_data) > 0:
            max_index = column_data[column_data == column_data.max()].index.values[0]
            row_data = sim_data_frame.loc[max_index, :]
            max_column = row_data[row_data == row_data.max()].index.values[0]
            if max_column == col:
                # print('best mapping:', col, max_index)
                sim_data_frame.drop([col], axis=1, inplace=True)
                sim_data_frame.drop([max_index], axis=0, inplace=True)
                return (col, max_index, row_data.max())
            else:
                return self.find_best_mapping(max_column, sim_data_frame)
        return (0, 0, 0)

    def calculate_structure_similarity(self, raw_edges, raw_nodes, edges, nodes, equivalence_mapping):
        sn = self.calculate_sn(raw_nodes, nodes, equivalence_mapping)
        se = self.calculate_se(raw_edges, edges, equivalence_mapping)
        sim_sum = self.calculate_graph_edit_distance(equivalence_mapping)
        graph_edit_distance = len(sn) + len(se) + 2 * sim_sum
        print("graph edit distance：", graph_edit_distance)
        snv = len(sn) / (len(raw_nodes) + len(nodes))
        sev = len(se) / (len(raw_edges) + len(edges))
        sbv = 2 * sim_sum / (len(raw_nodes) + len(nodes) - len(sn))
        simged = 1 - (snv + sev + sbv) / 3
        print("graph edit similarity:", round(simged, 3))
        return simged

    def calculate_graph_edit_distance(self, equivalence_mapping):
        sim_sum = sum(map(lambda x: 1 - x[2], equivalence_mapping))
        return sim_sum

    def calculate_sn(self, raw_nodes, nodes, equivalence_mapping):
        mapped_nodes = set(map(lambda x: x[0], equivalence_mapping))
        nodes = set(map(lambda x: x[0], nodes))
        delete_nodes = list(nodes - mapped_nodes)

        mapped_nodes2 = set(map(lambda x: x[1], equivalence_mapping))
        nodes2 = set(map(lambda x: x[0], raw_nodes))
        insert_nodes = list(nodes2 - mapped_nodes2)
        sn = delete_nodes + insert_nodes
        return sn

    def calculate_se(self, raw_edges, edges, equivalence_mapping):
        equivalence_mapping_dict = {}
        for item in equivalence_mapping:
            equivalence_mapping_dict[item[0]] = item[1]

        raw_edges_set = set(map(lambda x: (x[0], x[1]), raw_edges))
        se_list = []
        for edge in edges:
            if edge[0] in equivalence_mapping_dict and edge[1] in equivalence_mapping_dict:
                new_edge_x = equivalence_mapping_dict[edge[0]]
                new_edge_y = equivalence_mapping_dict[edge[1]]
                if (new_edge_x, new_edge_y) not in raw_edges_set:
                    se_list.append((edge[0], edge[1]))
                else:
                    new_set = set()
                    new_set.add((new_edge_x, new_edge_y))
                    raw_edges_set = raw_edges_set - new_set
            else:
                se_list.append((edge[0], edge[1]))
        raw_edges_list = list(raw_edges_set)
        return se_list + raw_edges_list