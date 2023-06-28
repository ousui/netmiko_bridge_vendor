from netmiko_bridge_vendor.h3c.h3c import H3cSSH, H3cTelnet

__mapper__ = {
    "h3c": H3cSSH,
    "h3c_ssh": H3cSSH,
    "h3c_telnet": H3cTelnet
}
