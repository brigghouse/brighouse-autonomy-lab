"""Executable model of MAVLink 2 message-signing acceptance semantics.

The model is deliberately small: it captures the decisions a receiver makes when a frame
arrives (keyed? signed? verifies? fresh? allow-listed? trusted link?) and the decisions it
makes on SETUP_SIGNING. Implementations differ in a handful of parameters (`Policy`).
Bounded exploration over an abstract adversary (observe, inject unsigned, replay, cannot
forge) checks security properties per policy and yields conformance tests that
`scripts/conformance.py` runs against real SITL builds.
"""
