#!/usr/bin/env python3
# -*- mode: Python; encoding: utf-8; indent-offset: 4; autowrap: nil -*-
# Shebang needed only for editors

from cmk.rulesets.v1.form_specs import Dictionary, DictElement, Float, String, Password, migrate_to_password
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic, Help, Title

def _formspec():
    return Dictionary(
        title=Title("Check SLZB-OS via web"),
        help_text=Help("Poll some additional infos from web api of the SLZB device"),
        elements={
#            ("uid", TextAscii(title=_("Username"), allow_empty=False)),
#            ("pwd", PasswordSpec(title=_("Password"), allow_empty=False, hidden=True)),
            "hostname": DictElement(
                required = True,
                parameter_form = String(
                    title = Title("Hostname or IP"), 
                    # prefill = DefaultValue("bla"),
                ),
            ),
        },
#        optional_keys=False,
    )


rule_spec_slzb_os = SpecialAgent(
    topic=Topic.GENERAL,
    name="agent_slzb_os",
    title=Title("SLZB-OS"),
    parameter_form=_formspec
)

