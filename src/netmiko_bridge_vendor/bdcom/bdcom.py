"""Subclass specific to Cisco bdcom."""
import time

from netmiko.cisco_base_connection import CiscoBaseConnection


class BDComBase(CiscoBaseConnection):
    """Subclass specific to BDCom."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("fast_cli", True)
        kwargs.setdefault("_legacy_mode", False)
        kwargs.setdefault("allow_auto_change", True)
        return super().__init__(*args, **kwargs)

    def session_preparation(self):
        """Prepare the session after the connection has been established."""

        self._test_channel_read(pattern=r"[>#]")
        self.set_base_prompt()
        """Ruijie OS requires enable mode to set terminal width"""
        self.enable()
        self.set_terminal_width(command="terminal width 256", pattern="terminal")
        self.disable_paging(command="terminal length 0")
        # Clear the read buffer
        time.sleep(0.3 * self.global_delay_factor)
        self.clear_buffer()

    def exit_enable_mode(self, exit_command="exit"):
        """Exits enable (privileged exec) mode."""
        return super().exit_enable_mode(exit_command=exit_command)

    def config_mode(self, config_command="config"):
        """Enter configuration mode."""
        return super().config_mode(config_command=config_command)

    def check_config_mode(self, check_string="_config#"):
        """Checks if the device is in configuration mode or not."""
        return super().check_config_mode(check_string)

    def exit_config_mode(self, exit_config="exit"):
        """Exit from configuration mode."""
        return super().exit_config_mode(exit_config=exit_config)

    def save_config(self, cmd="write", confirm=False, confirm_response=""):
        """Save config: write"""
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )


class BDComSSH(BDComBase):
    """Cisco IOS SSH driver."""

    pass


class BDComTelnet(BDComBase):
    """Cisco IOS Telnet driver."""

    def __init__(self, *args, **kwargs):
        default_enter = kwargs.get("default_enter")
        kwargs["default_enter"] = "\r" if default_enter is None else default_enter
        super().__init__(*args, **kwargs)
