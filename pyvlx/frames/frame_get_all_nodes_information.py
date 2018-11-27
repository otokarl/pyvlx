"""Module for get all node information from gateway."""
from enum import Enum

from pyvlx.const import Command, NodeTypeWithSubtype, NodeVariation
from pyvlx.position import Position
from pyvlx.string_helper import bytes_to_string, string_to_bytes

from .frame import FrameBase


class FrameGetAllNodesInformationRequest(FrameBase):
    """Frame for get node information request."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_ALL_NODES_INFORMATION_REQ)


class AllNodesInformationStatus(Enum):
    """Enum for node information status."""

    OK = 0  # pylint: disable=invalid-name
    Error_System_Table_Empty = 1


class FrameGetAllNodesInformationConfirmation(FrameBase):
    """Frame for confirmation for node information request."""

    PAYLOAD_LEN = 2

    def __init__(self, status=AllNodesInformationStatus.OK, number_of_nodes=0):
        """Init Frame."""
        super().__init__(Command.GW_GET_ALL_NODES_INFORMATION_CFM)
        self.status = status
        self.number_of_nodes = number_of_nodes

    def get_payload(self):
        """Return Payload."""
        return bytes([self.status.value, self.number_of_nodes])

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.status = AllNodesInformationStatus(payload[0])
        self.number_of_nodes = payload[1]

    def __str__(self):
        """Return human readable string."""
        return '<FrameGetAllNodesInformationConfirmation status=\'{}\' number_of_nodes={}/>'.format(self.status, self.number_of_nodes)


class FrameGetAllNodesInformationNotification(FrameBase):
    """Frame for notification of all nodes information request."""

    PAYLOAD_LEN = 124

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_ALL_NODES_INFORMATION_NTF)
        self.node_id = 0
        self.order = 0
        self.placement = 0
        self.name = ""
        self.velocity = 0
        self.node_type = NodeTypeWithSubtype.NO_TYPE
        self.product_group = 0
        self.product_type = 0
        self.node_variation = NodeVariation.NOT_SET
        self.power_mode = 0
        self.build_number = 0
        self._serial_number = bytes(8)
        self.state = 0
        self.current_position = Position()
        self.target = Position()
        self.current_position_fp1 = Position()
        self.current_position_fp2 = Position()
        self.current_position_fp3 = Position()
        self.current_position_fp4 = Position()
        self.remaining_time = 0
        self.timestamp = bytes(4)
        self.nbr_of_alias = 0
        self.alias_array = bytes(20)  # @VELUX: Looks like your documentation is wrong here. Alias array has 20 bytes.

    @property
    def serial_number(self):
        """Property for serial number in a human readable way."""
        return ":".join("{:02x}".format(c) for c in self._serial_number)

    def get_payload(self):
        """Return Payload."""
        payload = bytes()
        payload += bytes([self.node_id])
        payload += bytes([self.order >> 8 & 255, self.order & 255])
        payload += bytes([self.placement])
        payload += bytes(string_to_bytes(self.name, 64))
        payload += bytes([self.velocity])
        payload += bytes([self.node_type.value >> 8 & 255, self.node_type.value & 255])
        payload += bytes([self.product_group])
        payload += bytes([self.product_type])
        payload += bytes([self.node_variation.value])
        payload += bytes([self.power_mode])
        payload += bytes([self.build_number])
        payload += bytes(self._serial_number)
        payload += bytes([self.state])
        payload += bytes(self.current_position.raw)
        payload += bytes(self.target.raw)
        payload += bytes(self.current_position_fp1.raw)
        payload += bytes(self.current_position_fp2.raw)
        payload += bytes(self.current_position_fp3.raw)
        payload += bytes(self.current_position_fp4.raw)
        payload += bytes([self.remaining_time >> 8 & 255, self.remaining_time & 255])
        payload += bytes(self.timestamp)
        payload += bytes([self.nbr_of_alias])
        payload += self.alias_array
        return payload

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.node_id = payload[0]
        self.order = payload[1] * 256 + payload[2]
        self.placement = payload[3]
        self.name = bytes_to_string(payload[4:68])
        self.velocity = payload[68]
        self.node_type = NodeTypeWithSubtype(payload[69] * 256 + payload[70])
        self.product_group = payload[71]
        self.product_type = payload[72]
        self.node_variation = NodeVariation(payload[73])
        self.power_mode = payload[74]
        self.build_number = payload[75]
        self._serial_number = payload[76:84]
        self.state = payload[84]
        self.current_position = Position(payload[85:87])
        self.target = Position(payload[87:89])
        self.current_position_fp1 = Position(payload[89:91])
        self.current_position_fp2 = Position(payload[91:93])
        self.current_position_fp3 = Position(payload[93:95])
        self.current_position_fp4 = Position(payload[95:97])
        self.remaining_time = payload[97] * 256 + payload[98]
        self.timestamp = payload[99:103]
        self.nbr_of_alias = payload[103]
        self.alias_array = payload[104:125]

    def __str__(self):
        """Return human readable string."""
        return '<FrameGetAllNodesInformationNotification node_id={} oder={} ' \
            'placement={} name=\'{}\' velocity={} node_type=\'{}\' product_group={} ' \
            'product_type={} node_variation={} power_mode={} build_number={} ' \
            'serial_number=\'{}\' state={} current_position=\'{}\' ' \
            'target=\'{}\' current_position_fp1=\'{}\' current_position_fp2=\'{}\' ' \
            'current_position_fp3=\'{}\' current_position_fp4=\'{}\' ' \
            'remaining_time={} timestamp={} nbr_of_alias={} alias_array=\'{}\'/>'.format(
                self.node_id,
                self.order,
                self.placement,
                self.name,
                self.velocity,
                self.node_type,
                self.product_group,
                self.product_type,
                self.node_variation,
                self.power_mode,
                self.build_number,
                self.serial_number,
                self.state,
                self.current_position,
                self.target,
                self.current_position_fp1,
                self.current_position_fp2,
                self.current_position_fp3,
                self.current_position_fp4,
                self.remaining_time,
                self.timestamp,
                self.nbr_of_alias,
                (":".join("{:02x}".format(c) for c in self.alias_array)))


class FrameGetAllNodesInformationFinishedNotification(FrameBase):
    """Frame for notification of all nodes information finished notification."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_ALL_NODES_INFORMATION_FINISHED_NTF)