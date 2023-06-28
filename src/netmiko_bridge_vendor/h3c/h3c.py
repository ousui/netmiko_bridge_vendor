import re
import logging

# Logging configuration
log = logging.getLogger(__name__)  # noqa
log.addHandler(logging.NullHandler())  # noqa

from netmiko import NetmikoTimeoutException
from netmiko.hp.hp_comware import HPComwareBase, HPComwareSSH, HPComwareTelnet


class H3cBase(HPComwareBase):
    """
    support super mode
    """

    def __init__(self, *args, **kwargs):
        self.super_mode = False
        return super().__init__(**kwargs)

    def enable(self,
               cmd="super",
               pattern="assword",
               enable_pattern=None,
               re_flags=re.IGNORECASE,
               ):
        """enable mode on Comware is system-view."""

        """Enter enable mode.

        :param cmd: Device command to enter enable mode
        :type cmd: str

        :param pattern: pattern to search for indicating device is waiting for password
        :type pattern: str

        :param enable_pattern: pattern indicating you have entered enable mode
        :type pattern: str

        :param re_flags: Regular expression flags used in conjunction with pattern
        :type re_flags: int
        """

        output = ""
        msg = (
            "Failed to enter super mode. Please ensure you super password is correct."
        )

        if self.check_enable_mode():
            return output

        # Send "enable" mode command
        self.write_channel(self.normalize_cmd(cmd))
        try:
            # Read the command echo
            end_data = ""
            if self.global_cmd_verify is not False:
                output += self.read_until_pattern(pattern=re.escape(cmd.strip()))
                end_data = output.split(cmd.strip())[-1]

            # Search for trailing prompt or password pattern
            if pattern not in output and self.base_prompt not in end_data:
                output += self.read_until_prompt_or_pattern(
                    pattern=pattern, re_flags=re_flags
                )
            # Send the "secret" in response to password pattern
            if re.search(pattern, output):
                self.write_channel(self.normalize_cmd(self.secret))
                end_data = self.read_until_prompt_or_pattern(
                    pattern=pattern, re_flags=re_flags
                )
                output += end_data

            log.debug(f"get super result: {end_data}")

            if re.search("Error", end_data, re_flags) and re.search("locked", end_data, re_flags):
                raise ValueError(
                    "Failed to enter super mode. Maybe locked "
                    "the 'secret' argument to ConnectHandler."
                )

            # always have pattern charset
            if re.search("Error", end_data, re_flags) and re.search(pattern, end_data, re_flags):
                raise ValueError(msg)

            self.super_mode = True

        except NetmikoTimeoutException:
            raise ValueError(msg)
        return output

    def exit_enable_mode(self, exit_command="return"):
        """enable mode on Comware is system-view."""
        return ""

    def check_enable_mode(self):
        """ use the super_mod flag """
        return self.super_mode


class H3cSSH(HPComwareSSH, H3cBase):
    pass


class H3cTelnet(HPComwareTelnet, H3cBase):
    pass
