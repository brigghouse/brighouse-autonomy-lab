"""mavaudit: defensive MAVLink configuration auditor for lab and authorised testing.

Brighouse Autonomy Security Lab. Passive by default; the only active check sends a
single read-only parameter request. Never use against systems you are not
authorised in writing to test.
"""

import os

# pymavlink's mavutil falls back to the MAVLink 1 dialect unless MAVLINK20 is set.
# The MAVLink 2 parser also accepts MAVLink 1 frames, so always enable it.
os.environ.setdefault("MAVLINK20", "1")

__version__ = "0.1.0"
