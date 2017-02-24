# coding=utf-8
"""
Class used for representing tGateway of BPMN 2.0 graph
"""
from bpmn_python.graph.classes.flow_node_type import FlowNode


class Gateway(FlowNode):
    """
    Class used for representing tGateway of BPMN 2.0 graph
    """
    __gateway_directions_list = ["Unspecified", "Converging", "Diverging", "Mixed"]

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(Gateway, self).__init__()
        self.__gateway_direction = "Unspecified"


"""
<xsd:element name="activity" type="tActivity"/>
	<xsd:complexType name="tActivity" abstract="true">
		<xsd:complexContent>
			<xsd:extension base="tFlowNode">
				<xsd:sequence>
					<xsd:element ref="ioSpecification" minOccurs="0" maxOccurs="1"/>
					<xsd:element ref="property" minOccurs="0" maxOccurs="unbounded"/>
					<xsd:element ref="dataInputAssociation" minOccurs="0" maxOccurs="unbounded"/>
					<xsd:element ref="dataOutputAssociation" minOccurs="0" maxOccurs="unbounded"/>
					<xsd:element ref="resourceRole" minOccurs="0" maxOccurs="unbounded"/>
					<xsd:element ref="loopCharacteristics" minOccurs="0"/>
				</xsd:sequence>
				<xsd:attribute name="isForCompensation" type="xsd:boolean" default="false"/>
				<xsd:attribute name="startQuantity" type="xsd:integer" default="1"/>
				<xsd:attribute name="completionQuantity" type="xsd:integer" default="1"/>
				<xsd:attribute name="default" type="xsd:IDREF" use="optional"/>
			</xsd:extension>
		</xsd:complexContent>
	</xsd:complexType>
"""
