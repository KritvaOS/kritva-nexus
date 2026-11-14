#!/usr/bin/env python3
"""Regression tests for the address-map checker (KOS-NEXUS-008).

The checker is structural only. These tests copy the real map files, tables and register into a temporary
tree, break one thing at a time and expect the checker to name it, so that a change to the checker cannot
silently weaken it. They do not test that any base, size or attribute is right.
"""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("check_address_maps", ROOT / "scripts" / "check_address_maps.py")
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

FILES = ["architecture/maps/application_map.yaml", "architecture/maps/secure_map.yaml",
         "architecture/maps/peripheral_windows.yaml", "architecture/maps/register_layouts.yaml",
         "architecture/maps/connectivity.yaml", "architecture/ADDRESS_MAP.md",
         "architecture/INTERCONNECT_SPECIFICATION.md", "requirements/REQUIREMENTS.md"]


class Tree:
    def __init__(self):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)
        for f in FILES:
            (self.root / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / f, self.root / f)

    def edit(self, rel, old, new, count=1):
        p = self.root / rel
        text = p.read_text(encoding="utf-8")
        assert text.count(old) >= 1, f"{old!r} not found in {rel}"
        p.write_text(text.replace(old, new, count), encoding="utf-8")

    def problems(self):
        errs, _ = C.run(self.root)
        return errs

    def close(self):
        self.dir.cleanup()


class AddressMapChecker(unittest.TestCase):
    def setUp(self):
        self.t = Tree()
        self.addCleanup(self.t.close)

    def has(self, fragment):
        errs = self.t.problems()
        self.assertTrue(any(fragment in e for e in errs), f"expected {fragment!r} in {errs}")

    def test_repository_files_pass(self):
        self.assertEqual(self.t.problems(), [])

    def test_overlap_inside_a_space(self):
        self.t.edit("architecture/maps/application_map.yaml", "base: 0x0010000000", "base: 0x00000F0000")
        self.has("overlaps")

    def test_out_of_order(self):
        self.t.edit("architecture/maps/application_map.yaml", "base: 0x0040000000", "base: 0x0005000000")
        self.has("out of ascending order")

    def test_beyond_address_width(self):
        self.t.edit("architecture/maps/secure_map.yaml", "size: 0x00100000\n    class: crossing_alias",
                    "size: 0x100000000\n    class: crossing_alias")
        self.has("beyond the 32-bit address width")

    def test_misaligned_base(self):
        self.t.edit("architecture/maps/secure_map.yaml", "base: 0x20000000", "base: 0x20000800")
        self.has("not 4 KiB aligned")

    def test_duplicate_name(self):
        self.t.edit("architecture/maps/secure_map.yaml", "name: SHA", "name: AES")
        self.has("duplicate region name AES")

    def test_bad_label(self):
        self.t.edit("architecture/maps/application_map.yaml", "label: SELECTED\n    records: [NX-REQ-053, NX-REQ-102, NX-REQ-109]",
                    "label: DONE\n    records: [NX-REQ-053, NX-REQ-102, NX-REQ-109]")
        self.has("is not SELECTED, PROPOSED or OPEN")

    def test_bad_permission_string(self):
        self.t.edit("architecture/maps/application_map.yaml", "perm: rwx", "perm: rwz")
        self.has("perm must be")

    def test_missing_required_key(self):
        self.t.edit("architecture/maps/secure_map.yaml", "    class: security_rom\n", "")
        self.has("missing class")

    def test_alias_size_mismatch(self):
        self.t.edit("architecture/maps/secure_map.yaml", "size: 0x00100000", "size: 0x00080000")
        self.has("differs from")

    def test_alias_target_missing(self):
        self.t.edit("architecture/maps/secure_map.yaml", "target_region: System SRAM", "target_region: Nowhere")
        self.has("is not an application region")

    def test_alias_target_base_wrong(self):
        self.t.edit("architecture/maps/secure_map.yaml", "target_base: 0x0000000000", "target_base: 0x0000001000")
        self.has("target_base does not equal")

    def test_mailbox_region_missing(self):
        self.t.edit("architecture/maps/secure_map.yaml", "name: Mailbox (secure side)", "name: Mail slot")
        self.has("Mailbox (secure side) is missing")

    def test_unknown_requirement(self):
        self.t.edit("architecture/maps/application_map.yaml", "NX-REQ-102]", "NX-REQ-999]")
        self.has("NX-REQ-999 is not in the requirements register")

    def test_table_row_differs(self):
        self.t.edit("architecture/ADDRESS_MAP.md", "| 16 MiB | No | rw- |", "| 8 MiB | No | rw- |")
        self.has("differs from the file")

    def test_table_row_missing(self):
        text = (self.t.root / "architecture/ADDRESS_MAP.md").read_text(encoding="utf-8")
        row = next(l for l in text.splitlines() if l.startswith("| OSPI registers |"))
        self.t.edit("architecture/ADDRESS_MAP.md", row + "\n", "")
        self.has("table has")

    def test_window_outside_its_apb_window(self):
        self.t.edit("architecture/maps/peripheral_windows.yaml", "base: 0x0040010000", "base: 0x0050010000")
        self.has("is outside")

    def test_window_overlap(self):
        self.t.edit("architecture/maps/peripheral_windows.yaml", "base: 0x0040010000", "base: 0x0040008000")
        self.has("overlaps")

    def test_window_unknown_apb(self):
        self.t.edit("architecture/maps/peripheral_windows.yaml", "    apb: APB-0\n", "    apb: APB-9\n")
        self.has("is not an APB window")

    def test_window_outside_parent_region(self):
        self.t.edit("architecture/maps/application_map.yaml", "size: 0x0010000000\n    class: peripheral",
                    "size: 0x0000800000\n    class: peripheral")
        self.has("is outside")

    def test_required_window_missing(self):
        self.t.edit("architecture/maps/peripheral_windows.yaml", "name: DMA controller", "name: DMA engine")
        self.has("window DMA controller is missing")

    def test_window_unknown_requirement(self):
        self.t.edit("architecture/maps/peripheral_windows.yaml", "NX-REQ-019,", "NX-REQ-998,")
        self.has("NX-REQ-998 is not in the requirements register")

    def test_window_table_row_differs(self):
        self.t.edit("architecture/ADDRESS_MAP.md", "| PWM controller | APB-0 | 0x00_4000_0000 | 0x00_4000_FFFF | 64 KiB |",
                    "| PWM controller | APB-0 | 0x00_4000_0000 | 0x00_4000_7FFF | 32 KiB |")
        self.has("peripheral row")

    def test_window_table_row_missing(self):
        text = (self.t.root / "architecture/ADDRESS_MAP.md").read_text(encoding="utf-8")
        row = next(l for l in text.splitlines() if l.startswith("| Storage DMA | APB-1 |"))
        self.t.edit("architecture/ADDRESS_MAP.md", row + "\n", "")
        self.has("peripheral table has")

    def test_peripheral_file_missing(self):
        (self.t.root / "architecture/maps/peripheral_windows.yaml").unlink()
        self.has("peripheral_windows.yaml not found")

    def test_missing_file(self):
        (self.t.root / "architecture/maps/secure_map.yaml").unlink()
        self.has("secure_map.yaml not found")

    def test_secure_region_without_perm(self):
        self.t.edit("architecture/maps/secure_map.yaml", "    perm: r-x\n", "", 1)
        self.has("missing perm")

    def test_secure_rom_writable(self):
        self.t.edit("architecture/maps/secure_map.yaml", "perm: r-x", "perm: rwx", 1)
        self.has("must not be writable")

    def test_boot_window_executable(self):
        self.t.edit("architecture/maps/secure_map.yaml", "    class: crossing_alias\n    cacheable: false\n    perm: rw-",
                    "    class: crossing_alias\n    cacheable: false\n    perm: rwx")
        self.has("must not be executable")

    def test_secure_table_attribute_drift(self):
        self.t.edit("architecture/ADDRESS_MAP.md", "| Security ROM | 0x0000_0000 | 0x0000_FFFF | 64 KiB | No | r-x |",
                    "| Security ROM | 0x0000_0000 | 0x0000_FFFF | 64 KiB | Yes | r-x |")
        self.has("secure row 'Security ROM' differs")

    def test_secure_attributes_label_missing(self):
        self.t.edit("architecture/maps/secure_map.yaml", "attributes_label: SELECTED\n", "")
        self.has("missing key attributes_label")

    def test_layout_misaligned_offset(self):
        self.t.edit("architecture/maps/register_layouts.yaml", "offset: 0x0104", "offset: 0x0105", 1)
        self.has("4-byte aligned")

    def test_layout_duplicate_offset(self):
        self.t.edit("architecture/maps/register_layouts.yaml", "offset: 0x0108\n    access: RW\n    note: Baud-rate divisor",
                    "offset: 0x0104\n    access: RW\n    note: Baud-rate divisor")
        self.has("duplicate offset")

    def test_layout_bad_access(self):
        self.t.edit("architecture/maps/register_layouts.yaml", "access: W1C", "access: RWC", 1)
        self.has("is not one of")

    def test_layout_below_header(self):
        self.t.edit("architecture/maps/register_layouts.yaml", "offset: 0x0100", "offset: 0x0000", 1)
        self.has("is below")

    def test_layout_unknown_layout_for_block(self):
        self.t.edit("architecture/maps/register_layouts.yaml", "    layout: pwm\n    label: PROPOSED", "    layout: nothing\n    label: PROPOSED")
        self.has("is not defined")

    def test_block_missing_for_window(self):
        self.t.edit("architecture/maps/register_layouts.yaml", "  - name: GPIO controller\n    space: application\n    layout: gpio\n    label: PROPOSED\n    records: [NX-REQ-118]\n", "")
        self.has("has no block entry")

    def test_layout_none_needs_open(self):
        self.t.edit("architecture/maps/register_layouts.yaml", "    layout: none\n    label: OPEN", "    layout: none\n    label: PROPOSED")
        self.has("layout none needs the label OPEN")

    def test_layout_table_drift(self):
        self.t.edit("architecture/ADDRESS_MAP.md", "| BAUD_DIV | 0x0108 | RW |", "| BAUD_DIV | 0x0108 | RO |")
        self.has("layout uart row 'BAUD_DIV' differs")

    def test_layout_window_too_small(self):
        self.t.edit("architecture/maps/register_layouts.yaml", "offset: 0x200004", "offset: 0x20000004", 1)
        self.has("does not fit the smallest window")

    def test_layout_unknown_record(self):
        self.t.edit("architecture/maps/register_layouts.yaml", "layout_records: [NX-REQ-117, NX-REQ-118]", "layout_records: [NX-REQ-117, NX-REQ-998]")
        self.has("NX-REQ-998 is not in the requirements register")

    def test_connectivity_unknown_region(self):
        self.t.edit("architecture/maps/connectivity.yaml", "region: DDR4\n    access: rw", "region: Nowhere\n    access: rw")
        self.has("region is not a non-reserved region")

    def test_connectivity_access_beyond_permission(self):
        self.t.edit("architecture/maps/connectivity.yaml", "region: OSPI NOR window\n    access: r\n", "region: OSPI NOR window\n    access: rw\n")
        self.has("is not allowed by the region permissions")

    def test_connectivity_master_on_unknown_fabric(self):
        self.t.edit("architecture/maps/connectivity.yaml", "name: ISP\n    fabric: AXI-1", "name: ISP\n    fabric: AXI-9")
        self.has("fabric 'AXI-9' is not defined")

    def test_connectivity_region_without_attachment(self):
        self.t.edit("architecture/maps/connectivity.yaml", "  - region: System SRAM\n    attached_to: open\n    label: PROPOSED\n    records: [NX-REQ-120]\n", "")
        self.has("region System SRAM has no attachment")

    def test_connectivity_ddr4_not_on_crossbar(self):
        self.t.edit("architecture/maps/connectivity.yaml", "attached_to: crossbar", "attached_to: AXI-0")
        self.has("DDR4, and only DDR4, is attached to the crossbar")

    def test_connectivity_master_without_link(self):
        self.t.edit("architecture/maps/connectivity.yaml", "master: Boot window bridge", "master: Nobody")
        self.has("master Boot window bridge has no link")

    def test_connectivity_link_to_reserved_region(self):
        self.t.edit("architecture/maps/connectivity.yaml", "region: DDR4\n    access: rw", "region: Reserved\n    access: rw")
        self.has("region is not a non-reserved region")

    def test_connectivity_link_on_wrong_fabric(self):
        self.t.edit("architecture/maps/connectivity.yaml", "region: Camera frame pool\n    attached_to: AXI-1", "region: Camera frame pool\n    attached_to: AXI-2")
        self.has("the region is attached to AXI-2 and the master is on AXI-1")

    def test_connectivity_apb_link_from_wrong_fabric(self):
        self.t.edit("architecture/maps/connectivity.yaml", "master: ISP\n    region: Camera frame pool\n    access: r", "master: ISP\n    region: Peripheral register space\n    access: rw")
        self.has("only masters on AXI-0 or AXI-3 reach the peripheral register space")

    def test_connectivity_matrix_table_drift(self):
        self.t.edit("architecture/INTERCONNECT_SPECIFICATION.md", "| C910 cluster | AXI-0 | rw | - |", "| C910 cluster | AXI-0 | r | - |")
        self.has("row 'C910 cluster' differs from the file")

    def test_connectivity_fabric_table_drift(self):
        self.t.edit("architecture/INTERCONNECT_SPECIFICATION.md", "| AXI-3 | 64 |", "| AXI-3 | 128 |")
        self.has("differs from the file")

    def test_connectivity_unknown_record(self):
        self.t.edit("architecture/maps/connectivity.yaml", "connectivity_records: [NX-REQ-120]", "connectivity_records: [NX-REQ-998]")
        self.has("NX-REQ-998 is not in the requirements register")


class Parser(unittest.TestCase):
    def test_subset(self):
        errs = []
        m = C.parse("# c\nspace: x\nwidth: 40   # note\nlist: [A, B]\nregions:\n  - name: N\n    base: 0x10\n"
                    "    perm: \"---\"\n    cacheable: true\n    note: text with: colon\n", errs, "t")
        self.assertEqual(errs, [])
        self.assertEqual(m["width"], 40)
        self.assertEqual(m["list"], ["A", "B"])
        r = m["regions"][0]
        self.assertEqual((r["name"], r["base"], r["perm"], r["cacheable"], r["note"]),
                         ("N", 16, "---", True, "text with: colon"))

    def test_two_lists(self):
        errs = []
        m = C.parse("space: x\napb_windows:\n  - name: A\n    base: 0x10\nwindows:\n  - name: W\n    apb: A\n"
                    "  - name: V\n    apb: A\n", errs, "t")
        self.assertEqual(errs, [])
        self.assertEqual([r["name"] for r in m["apb_windows"]], ["A"])
        self.assertEqual([r["name"] for r in m["windows"]], ["W", "V"])

    def test_unreadable_line_is_reported(self):
        errs = []
        C.parse("space x\n", errs, "t")
        self.assertTrue(errs)

    def test_hex_grouping(self):
        self.assertEqual(C.hexs(0x1000000000, 40), "0x10_0000_0000")
        self.assertEqual(C.hexs(0x20080000, 32), "0x2008_0000")

    def test_size_text(self):
        self.assertEqual(C.size_text(1 << 30), "1 GiB")
        self.assertEqual(C.size_text(0xC000000), "192 MiB")
        self.assertEqual(C.size_text(0x10000), "64 KiB")


if __name__ == "__main__":
    unittest.main()
