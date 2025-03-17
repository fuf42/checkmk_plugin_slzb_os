#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# Shebang needed only for editors

from cmk.server_side_calls.v1 import noop_parser, SpecialAgentConfig, SpecialAgentCommand

def _agent_arguments(params, host_config):
#    import pprint
#    pprint.pprint(params)
    args = [ "--hostname", str(params['hostname']) ]
    yield SpecialAgentCommand(command_arguments=args)

special_agent_slzb_os = SpecialAgentConfig(
    name="slzb_os",
    parameter_parser=noop_parser,
    commands_function=_agent_arguments
)

