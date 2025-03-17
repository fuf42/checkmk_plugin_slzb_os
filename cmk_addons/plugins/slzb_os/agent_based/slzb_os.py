#!/usr/bin/env python3

from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, Result, State, Metric, check_levels, render
from cmk.plugins.lib import uptime

import itertools
import json
import time

from pprint import pprint

def parse_slzb_os(string_table):
    #pprint(string_table)
    parsed = {}

    for line in string_table:
        parsed[line[0]] = line[1]

    #pprint(parsed)
    return parsed


def discover_slzb_os(section):

    # pprint(section)

    yield Service(item = "info")
    yield Service(item = "RAM")
    yield Service(item = "Zigbee-Chip-Temperatur")
    yield Service(item = "Core-Chip-Temperatur")


def check_slzb_os(item, section):
    
    #pprint(item)
    #pprint(section)

    if item == "Uptime":
        uptime_secs = int(section['uptime'])
        #pprint(uptime_secs)
        up_date = render.datetime(time.time() - uptime_secs)
        #pprint(up_date)

        return uptime.Section(
            uptime_secs,
            "Up since %s" % up_date
        )

    if item == "Core-Chip-Temperatur":
        esp32_temp = float(section['esp32_temp'])
        yield from check_levels(
            esp32_temp,
            #levels_upper=params.get('temperature', None),
            label='Core-Chip-Temperatur',
            metric_name='esp32_temp',
            render_func=lambda v: "%.1f°C" % v
        )

    if item == "Zigbee-Chip-Temperatur":
        zb_temp = float(section['zb_temp'])
        yield from check_levels(
            zb_temp,
            # section['temperature'],
            #levels_upper=params.get('temperature', None),
            label='Zigbee-Chip-Temperatur',
            metric_name='zb_temp',
            render_func=lambda v: "%.1f°C" % v
        )
 
    if item == "RAM":
        ram_total = float(section['ram_total'])
        ram_usage = float(section['ram_usage'])
        yield Metric(name="ram_usage", value=ram_usage, boundaries=(0, ram_total))

        ram_used_perc = 100.0 * ram_usage / ram_total
        yield from check_levels(
            ram_used_perc,
            levels_upper = ("fixed", (80.0, 90.0)),
            metric_name = "ram_used_perc",
            label = "RAM used",
            boundaries = (0.0, 100.0),
            # notice_only = True,
            render_func=lambda v: "%.0f%% (%.0f kB of %.0f kB)" % (v, ram_usage, ram_total)
        )

    if item == "info":
      yield Result(
        state = State.OK, 
        summary = "Model: %s, Firmware: %s, branch: %s, Zigbee hardware: %s, Zigbee Version: %s" % (
            section['model'],
            section['sw_version'], 
            section['fw_channel'],
            section['zb_hw'],
            section['zb_version']
        )
      )


agent_section_slzb_os = AgentSection(
    name = "slzb_os",
    parse_function = parse_slzb_os,
)

check_plugin_slzb_os = CheckPlugin(
    name = "slzb_os",
    service_name = "SLZB %s",
    discovery_function = discover_slzb_os,
    check_function = check_slzb_os,
)

