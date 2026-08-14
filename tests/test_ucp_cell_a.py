#!/usr/bin/env python
"""Automatic regression test for the cell_a unit-cell-property self-reference fix.

BUG (fixed in mudlab/phases/models/unit_cell_prop.py):
    A component's cell_a derives from its OWN cell_b (cell_a = 0.57735 * cell_b,
    i.e. a = b / sqrt(3)). On import the object pool can re-uuid a component whose
    uuid collides with one already in the project (ObjectPool.add_object, comment:
    "will break refs"). That orphaned the cell_a<-cell_b SELF-reference, and
    UnitCellProperty.resolve_json_references then NULLED the derivation, leaving
    cell_a = 0 -> volume ~= 0 -> the phase produced a zero diffraction pattern.

FIX: resolve_json_references recovers the derivation from the UCP's own component
    when the stored prop uuid is orphaned but the referenced attribute (cell_b)
    exists on that component.

Run with the app's own python (from the repo root):
    data\\bin\\python.exe tests\\test_ucp_cell_a.py
"""
import os
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: F401  (importing the models needs GTK present)

import mudlab
from mudlab.phases.models.component import Component

CMP = os.path.join(
    os.path.dirname(mudlab.__file__), "data", "default components",
    "Di-Smectite", "Di-Smectite - Ca 2GLY.cmp")


def main():
    if not os.path.isfile(CMP):
        print("SKIP: default component not found:\n  %s" % CMP)
        return 2

    # Load the component; resolve ONLY its unit-cell properties (the whole
    # component.resolve_json_references also resolves atoms, which assert a phase
    # parent - not needed to exercise the UCP self-reference logic under test).
    comp = list(Component.load_components(CMP, parent=None))[0]
    ucp_a = type(comp).ucp_a._get(comp)

    # 1) Clean resolve: the derived cell_a resolves (~0.5206 = 0.57735 * cell_b).
    ucp_a.resolve_json_references()
    ucp_a.update_value()
    ok1 = comp.cell_a > 0.4
    print("1) clean resolve     cell_a=%.5f -> %s"
          % (comp.cell_a, "OK" if ok1 else "FAIL"))

    # 2) Orphaned self-reference (simulates the import re-uuid): the stored prop
    #    uuid is no longer in the object pool. WITH the fix, resolve recovers
    #    cell_a from the component's own cell_b; WITHOUT it, cell_a -> 0.
    ucp_a._temp_prop = ["ffffffffffffffffffffffffffffffff", "cell_b"]  # bogus uuid
    ucp_a.prop = None
    ucp_a.resolve_json_references()
    ucp_a.update_value()
    ok2 = comp.cell_a > 0.4
    print("2) orphaned self-ref cell_a=%.5f -> %s   (the fix)"
          % (comp.cell_a, "OK" if ok2 else "FAIL"))

    if ok1 and ok2:
        print("\nPASS: cell_a survives an orphaned self-reference.")
        return 0
    print("\nFAIL: cell_a lost its cell_b derivation - the "
          "resolve_json_references fix is missing or broken.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
