'''
Binary object store, defined in section 9.6.2 of the USB 3.0 specification

It holds multiple device capabilities
'''
import struct
from umap2.core.usb import DescriptorType
from umap2.core.usb_base import USBBaseActor
from umap2.fuzz.helpers import mutable


class USBBinaryObjectStore(USBBaseActor):

    def __init__(self, app, phy, capabilities):
        '''
        :param app: Umap2 application
        :param phy: Physical connection
        '''
        super(USBBinaryObjectStore, self).__init__(app, phy)
        self.capabilities = capabilities

    @mutable('bos_descriptor')
    def get_descriptor(self, usb_type='fullspeed', valid=False):
        device_capabilities_descriptors = b''
        for c in self.capabilities:
            device_capabilities_descriptors += c.get_descriptor(usb_type, valid)
        bLength = 5  # always 5
        bDescriptorType = DescriptorType.bos
        wTotalLength = len(device_capabilities_descriptors) + 5
        bNumCapabilities = len(self.capabilities)
        d = struct.pack(
            '<BBHB',
            bLength,
            bDescriptorType,
            wTotalLength & 0xffff,
            bNumCapabilities,
        )
        return d + device_capabilities_descriptors
