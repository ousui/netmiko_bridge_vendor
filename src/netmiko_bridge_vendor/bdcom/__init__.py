from netmiko_bridge_vendor.bdcom.bdcom import BDComSSH, BDComTelnet

__mapper__ = {
    "bdcom": BDComSSH,
    "bdcom_ssh": BDComSSH,
    "bdcom_telnet": BDComTelnet
}
