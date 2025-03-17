# CheckMK Plugin slzb-os

Very basic CheckMK special agent for SMLight slzb-os devices (e.g. SLZB-06M).
The special_agent is polling `http:/<hostname or ip/ha_status` and `http:/<hostname or ip/ha_sensors`. No authentication at the moment.

Minumum CheckMK version is 2.3
