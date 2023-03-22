from netmiko_bridge.vendor_getter import VendorGetter
from netmiko_bridge_vendor import bdcom

__VERSION__ = '0.1.0'

vendor_getter = VendorGetter()
# you can add the mapper use the
vendor_getter.add_vendor(bdcom.__mapper__)
