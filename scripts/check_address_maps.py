#!/usr/bin/env python3
"""Check the Kritva Nexus address-map files (KOS-NEXUS-008).

  check_address_maps.py [--root DIR]

Reads architecture/maps/application_map.yaml and architecture/maps/secure_map.yaml (the machine-readable
sources), architecture/ADDRESS_MAP.md (the tables derived from them) and requirements/REQUIREMENTS.md.

Implemented checks, and nothing more:
  1. Each map file parses (a small YAML subset is read by this script, so no package is needed) and has the
     required header keys; the file name matches its `space`; the address width is a positive integer.
  2. Every region has the required keys, an integer base and size, a label of SELECTED, PROPOSED or OPEN,
     a records list of identifiers, and (application map) a cacheable flag and an rwx permission string.
  3. Region names are unique; each base is 4 KiB aligned; each region ends inside the address width; regions
     are listed in ascending order and none overlaps another inside the same space. Overlap between the two
     spaces is not a conflict and is not checked.
  4. Crossing aliases of the secure map name an existing region of the application map, start at its base and
     have its size; the secure map has the mailbox region; the application map has the System SRAM region and
     the peripheral register space.
  5. Every NX-REQ identifier named in a map file exists in the requirements register.
  6. The two tables of ADDRESS_MAP.md agree with the files, row by row: name, first and last address, size,
     cacheability, permissions, label and requirement numbers.
  7. architecture/maps/peripheral_windows.yaml (the division of the peripheral register space): the parent
     region exists in the application map; each APB window and each peripheral window has its keys, a 4 KiB
     aligned base and size, a label and records, a unique name, lies inside its parent (the APB window inside
     the parent region, the peripheral window inside the APB window it names), is listed in ascending order
     and overlaps no other; the DMA controller, OSPI NOR controller and application-side mailbox windows
     exist; the NX-REQ identifiers exist; and the table of section 2.1 of ADDRESS_MAP.md agrees row by row.
  8. Both maps carry cacheable and perm for every region (the secure attributes are PROPOSED, NX-REQ-119); in the
     secure map a security_rom or nor_secure region has no write permission and a crossing_alias region has no
     execute permission; the secure header has attributes_label and attributes_records.
  9. architecture/maps/register_layouts.yaml (NX-REQ-117, NX-REQ-118): the common registers and the registers of
     each layout have 4-byte aligned, unique, ascending offsets, an access type of RO, RW, WO, W1C or W1S and a
     note; a layout with a header keeps its registers at or above the header size and every layout fits inside
     the smallest window of the blocks that use it; every peripheral window and every security peripheral
     region has one block entry with an existing layout (or layout none with the label OPEN); the identifiers
     exist; and the register tables of section 2.2 of ADDRESS_MAP.md agree row by row.
  10. architecture/maps/connectivity.yaml (NX-REQ-120): fabrics, masters, region attachments and links have their
     keys, labels and identifiers; each master sits on an existing fabric; each link names an existing master and a
     region of the application map (never Reserved), appears once and asks for read and write access that the
     region permissions allow; every region other than Reserved has one attachment (a fabric, crossbar, apb or open);
     DDR4 is attached to the crossbar and only DDR4 is; the peripheral register space is attached to apb and is
     linked only from masters on AXI-0 or AXI-3; a link to a region attached to a fabric comes only from a master on
     that fabric; every master has a link; the identifiers exist; and the four tables of section 7 of
     INTERCONNECT_SPECIFICATION.md agree row by row.
A PASS does not show that a base, size or attribute is right, that the width fits the C910 or any master,
or that anything is approved; that is review work (NX-REQ-029, NX-ARCH-GAP-003). Exit 0 if it passes, 1 if not.
Stdlib only.
"""
import argparse
import re
import sys
from pathlib import Path

MAPS = {"application": "architecture/maps/application_map.yaml", "secure": "architecture/maps/secure_map.yaml"}
PERIPH = "architecture/maps/peripheral_windows.yaml"
LAYOUTS = "architecture/maps/register_layouts.yaml"
CONN = "architecture/maps/connectivity.yaml"
SPEC = "architecture/INTERCONNECT_SPECIFICATION.md"
CONN_KEYS = ["space", "document", "version", "connectivity_label", "connectivity_records", "fabrics", "masters",
             "attachments", "links"]
APB_FABRICS = {"AXI-0", "AXI-3"}
LAYOUT_KEYS = ["space", "document", "version", "layout_label", "layout_records", "register_width_bits", "header_size",
               "common_registers", "layouts", "registers", "blocks"]
REG_KEYS = ["name", "offset", "access", "note"]
ACCESS = {"RO", "RW", "WO", "W1C", "W1S"}
PERIPH_KEYS = ["space", "document", "version", "parent_region", "map_label", "map_records", "apb_windows", "windows"]
APB_KEYS = ["name", "base", "size", "label", "records", "note"]
WINDOW_KEYS = ["name", "apb", "base", "size", "class", "label", "records", "note"]
REQUIRED_WINDOWS = ["DMA controller", "OSPI NOR controller", "Mailbox (application side)"]
HEADER_KEYS = ["space", "document", "version", "address_width_bits", "address_width_label",
               "address_width_records", "map_label", "map_records", "regions"]
REGION_KEYS = ["name", "base", "size", "class", "label", "records", "note"]
APP_REGION_KEYS = ["cacheable", "perm"]
SECURE_HEADER_KEYS = ["attributes_label", "attributes_records"]
LABELS = {"SELECTED", "PROPOSED", "OPEN"}
ALIGN = 0x1000
RECORD_RE = re.compile(r"^NX-(REQ|DEC|ARCH-GAP|ARCH-OI|INT)-\d{3}$")


def scalar(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [x.strip() for x in inner.split(",")] if inner else []
    if v in ("true", "false"):
        return v == "true"
    if re.fullmatch(r"0[xX][0-9A-Fa-f]+", v):
        return int(v, 16)
    if re.fullmatch(r"\d+", v):
        return int(v)
    return v


def parse(text, errs, where):
    """Read the small YAML subset the map files use: top-level scalars and lists of flat mappings."""
    top, cur, cur_list = {}, None, None
    for n, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if indent == 0:
            cur_list = None
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
            if not m:
                errs.append(f"{where}:{n}: cannot read line")
                continue
            val = m.group(2)
            if not val.startswith(("\"", "'")) and " #" in val:
                val = val.split(" #", 1)[0]
            if val.strip() == "":
                cur_list = []
                top[m.group(1)] = cur_list
                continue
            top[m.group(1)] = scalar(val)
        elif cur_list is not None:
            if line.startswith("- "):
                cur = {}
                cur_list.append(cur)
                line = line[2:].strip()
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
            if not m or cur is None:
                errs.append(f"{where}:{n}: cannot read region line")
                continue
            cur[m.group(1)] = scalar(m.group(2))
        else:
            errs.append(f"{where}:{n}: unexpected indented line")
    return top


def hexs(v, bits):
    s = f"{v:0{(bits + 3) // 4}X}"
    groups, i = [], len(s)
    while i > 0:
        groups.append(s[max(0, i - 4):i])
        i -= 4
    return "0x" + "_".join(reversed(groups))


def size_text(v):
    for unit, d in (("GiB", 1 << 30), ("MiB", 1 << 20), ("KiB", 1 << 10)):
        if v >= d and v % d == 0:
            return f"{v // d} {unit}"
    return f"{v} B"


def ids_text(records):
    return ", ".join(r.replace("NX-REQ-", "") for r in records)


def expected_rows(m, app):
    bits = m["address_width_bits"]
    rows = []
    for r in m["regions"]:
        end = r["base"] + r["size"] - 1
        cells = [r["name"], hexs(r["base"], bits), hexs(end, bits), size_text(r["size"])]
        cells += ["Yes" if r["cacheable"] else "No", r["perm"]]
        cells += [r["label"], ids_text(r["records"])]
        rows.append(cells)
    return rows


def periph_rows(pw):
    rows = []
    for r in pw["apb_windows"]:
        end = r["base"] + r["size"] - 1
        rows.append([r["name"] + " (bridge window)", "-", hexs(r["base"], 40), hexs(end, 40), size_text(r["size"]),
                     r["label"], ids_text(r["records"])])
    for r in pw["windows"]:
        end = r["base"] + r["size"] - 1
        rows.append([r["name"], r["apb"], hexs(r["base"], 40), hexs(end, 40), size_text(r["size"]), r["label"],
                     ids_text(r["records"])])
    return rows


def hex_off(v):
    return f"0x{v:04X}"


def reg_row(r):
    return [r["name"], hex_off(r["offset"]), r["access"], r["note"]]


def check_regs(items, keys, label, errs, w, lo, hi, layout_header=False):
    """Offset rules shared by common registers and layout registers; returns nothing."""
    seen_n, seen_o, prev = set(), set(), -1
    for r in items:
        name = r.get("name", "?")
        miss = [k for k in keys if k not in r]
        if miss:
            errs.append(f"{w}: {label} {name}: missing {', '.join(miss)}")
            continue
        o = r["offset"]
        if not isinstance(o, int) or o % 4:
            errs.append(f"{w}: {label} {name}: offset must be a 4-byte aligned integer")
            continue
        if name in seen_n:
            errs.append(f"{w}: {label} {name}: duplicate register name")
        if o in seen_o:
            errs.append(f"{w}: {label} {name}: duplicate offset {hex(o)}")
        if o < prev:
            errs.append(f"{w}: {label} {name}: offsets are not ascending")
        seen_n.add(name), seen_o.add(o)
        prev = max(prev, o)
        if r["access"] not in ACCESS:
            errs.append(f"{w}: {label} {name}: access {r['access']!r} is not one of {sorted(ACCESS)}")
        if lo is not None and o < lo:
            errs.append(f"{w}: {label} {name}: offset {hex(o)} is below {hex(lo)}")
        if hi is not None and o + 4 > hi:
            errs.append(f"{w}: {label} {name}: offset {hex(o)} does not fit the smallest window ({size_text(hi)})")


def check_layouts(maps, rl, errs):
    w = "register layouts"
    for k in LAYOUT_KEYS:
        if k not in rl:
            errs.append(f"{w}: missing key {k}")
    if rl.get("space") != "register_layouts":
        errs.append(f"{w}: space is {rl.get('space')!r}, expected 'register_layouts'")
    if rl.get("layout_label") not in LABELS:
        errs.append(f"{w}: layout_label must be one of {sorted(LABELS)}")
    if rl.get("register_width_bits") != 32:
        errs.append(f"{w}: register_width_bits must be 32")
    hs = rl.get("header_size")
    if not isinstance(hs, int) or hs <= 0 or hs % 4:
        errs.append(f"{w}: header_size must be a positive multiple of 4")
        return False
    sizes = {("application", x["name"]): x["size"] for x in maps["peripheral"]["windows"]}
    sizes.update({("secure", x["name"]): x["size"] for x in maps["secure"]["regions"]
                  if x.get("class") == "security_peripheral"})
    check_regs(rl.get("common_registers") or [], REG_KEYS, "common register", errs, w, 0, hs)
    layouts, names = {}, set()
    for l_ in rl.get("layouts") or []:
        n = l_.get("name", "?")
        miss = [k for k in ("name", "header", "label", "records", "note") if k not in l_]
        if miss:
            errs.append(f"{w}: layout {n}: missing {', '.join(miss)}")
            continue
        if n in names:
            errs.append(f"{w}: duplicate layout {n}")
        names.add(n)
        if not isinstance(l_["header"], bool):
            errs.append(f"{w}: layout {n}: header must be true or false")
        if l_["label"] not in LABELS:
            errs.append(f"{w}: layout {n}: label {l_['label']!r} is not SELECTED, PROPOSED or OPEN")
        layouts[n] = l_
    blocks, bnames = rl.get("blocks") or [], set()
    users = {}
    for b in blocks:
        n = b.get("name", "?")
        miss = [k for k in ("name", "space", "layout", "label", "records") if k not in b]
        if miss:
            errs.append(f"{w}: block {n}: missing {', '.join(miss)}")
            continue
        key = (b["space"], n)
        if key in bnames:
            errs.append(f"{w}: duplicate block {n}")
        bnames.add(key)
        if key not in sizes:
            errs.append(f"{w}: block {n}: no {b['space']} peripheral window or security peripheral region of that name")
        if b["label"] not in LABELS:
            errs.append(f"{w}: block {n}: label {b['label']!r} is not SELECTED, PROPOSED or OPEN")
        recs = b["records"]
        if not isinstance(recs, list) or not recs or not all(RECORD_RE.match(str(x)) for x in recs):
            errs.append(f"{w}: block {n}: records must be a non-empty list of NX identifiers")
        if b["layout"] == "none":
            if b["label"] != "OPEN":
                errs.append(f"{w}: block {n}: layout none needs the label OPEN")
        elif b["layout"] not in layouts:
            errs.append(f"{w}: block {n}: layout {b['layout']!r} is not defined")
        else:
            users.setdefault(b["layout"], []).append(key)
    for key in sizes:
        if key not in bnames:
            errs.append(f"{w}: {key[0]} window {key[1]} has no block entry")
    regs = rl.get("registers") or []
    for n, l_ in layouts.items():
        mine = [r for r in regs if r.get("layout") == n]
        if not mine:
            errs.append(f"{w}: layout {n} has no registers")
        small = min((sizes[k] for k in users.get(n, []) if k in sizes), default=None)
        check_regs(mine, REG_KEYS, f"layout {n} register", errs, w, hs if l_.get("header") is True else None, small)
    for r in regs:
        if r.get("layout") not in layouts:
            errs.append(f"{w}: register {r.get('name')}: layout {r.get('layout')!r} is not defined")
    for n in layouts:
        if n not in users:
            errs.append(f"{w}: layout {n} is used by no block")
    return True


def conn_tables(cn, app):
    regs = [r["name"] for r in app["regions"] if r["class"] != "reserved"]
    link = {(l["master"], l["region"]): l["access"] for l in cn["links"]}
    fab = [[f["name"], str(f["width_bits"]), f["role"], f["label"], ids_text(f["records"])] for f in cn["fabrics"]]
    mas = [[m["name"], m["fabric"], m["label"], ids_text(m["records"])] for m in cn["masters"]]
    att = [[a["region"], a["attached_to"], a["label"], ids_text(a["records"])] for a in cn["attachments"]]
    mat = [[m["name"], m["fabric"]] + [link.get((m["name"], r), "-") for r in regs] for m in cn["masters"]]
    return regs, fab, mas, att, mat


def check_connectivity(app, cn, errs):
    w = "connectivity"
    for k in CONN_KEYS:
        if k not in cn:
            errs.append(f"{w}: missing key {k}")
    if cn.get("space") != "connectivity":
        errs.append(f"{w}: space is {cn.get('space')!r}, expected 'connectivity'")
    if cn.get("connectivity_label") not in LABELS:
        errs.append(f"{w}: connectivity_label must be one of {sorted(LABELS)}")
    perms = {r["name"]: r for r in app["regions"]}
    fabrics, masters, attach = {}, {}, {}

    def common(item, what, name, keys):
        miss = [k for k in keys if k not in item]
        if miss:
            errs.append(f"{w}: {what} {name}: missing {', '.join(miss)}")
            return False
        if item["label"] not in LABELS:
            errs.append(f"{w}: {what} {name}: label {item['label']!r} is not SELECTED, PROPOSED or OPEN")
        recs = item["records"]
        if not isinstance(recs, list) or not recs or not all(RECORD_RE.match(str(x)) for x in recs):
            errs.append(f"{w}: {what} {name}: records must be a non-empty list of NX identifiers")
        return True

    for f in cn.get("fabrics") or []:
        n = f.get("name", "?")
        if common(f, "fabric", n, ["name", "width_bits", "role", "label", "records"]):
            if n in fabrics:
                errs.append(f"{w}: duplicate fabric {n}")
            if not isinstance(f["width_bits"], int) or f["width_bits"] <= 0 or f["width_bits"] & (f["width_bits"] - 1):
                errs.append(f"{w}: fabric {n}: width_bits must be a power of two")
            fabrics[n] = f
    for m in cn.get("masters") or []:
        n = m.get("name", "?")
        if common(m, "master", n, ["name", "fabric", "label", "records"]):
            if n in masters:
                errs.append(f"{w}: duplicate master {n}")
            if m["fabric"] not in fabrics:
                errs.append(f"{w}: master {n}: fabric {m['fabric']!r} is not defined")
            masters[n] = m
    for a in cn.get("attachments") or []:
        n = a.get("region", "?")
        if common(a, "attachment", n, ["region", "attached_to", "label", "records"]):
            if n in attach:
                errs.append(f"{w}: duplicate attachment for {n}")
            if n not in perms or perms[n]["class"] == "reserved":
                errs.append(f"{w}: attachment {n}: not a non-reserved region of the application map")
            if a["attached_to"] not in set(fabrics) | {"crossbar", "apb", "open"}:
                errs.append(f"{w}: attachment {n}: attached_to {a['attached_to']!r} is not a fabric, crossbar, apb or open")
            if (a["attached_to"] == "crossbar") != (n == "DDR4"):
                errs.append(f"{w}: attachment {n}: DDR4, and only DDR4, is attached to the crossbar")
            if (a["attached_to"] == "apb") != (n == "Peripheral register space"):
                errs.append(f"{w}: attachment {n}: the peripheral register space, and only it, is attached to apb")
            attach[n] = a
    for r in app["regions"]:
        if r["class"] != "reserved" and r["name"] not in attach:
            errs.append(f"{w}: region {r['name']} has no attachment")
    seen, used = set(), set()
    for l in cn.get("links") or []:
        n = f"{l.get('master', '?')} to {l.get('region', '?')}"
        if not common(l, "link", n, ["master", "region", "access", "label", "records"]):
            continue
        if n in seen:
            errs.append(f"{w}: duplicate link {n}")
        seen.add(n)
        mm = masters.get(l["master"])
        if mm is None:
            errs.append(f"{w}: link {n}: master is not defined")
            continue
        used.add(l["master"])
        rg = perms.get(l["region"])
        if rg is None or rg["class"] == "reserved":
            errs.append(f"{w}: link {n}: region is not a non-reserved region of the application map")
            continue
        if l["access"] not in ("r", "w", "rw"):
            errs.append(f"{w}: link {n}: access must be r, w or rw")
        else:
            for ch, idx in (("r", 0), ("w", 1)):
                if ch in l["access"] and rg["perm"][idx] != ch:
                    errs.append(f"{w}: link {n}: access {l['access']} is not allowed by the region permissions {rg['perm']}")
        att = attach.get(l["region"], {}).get("attached_to")
        if att in fabrics and att != mm["fabric"]:
            errs.append(f"{w}: link {n}: the region is attached to {att} and the master is on {mm['fabric']}")
        if att == "apb" and mm["fabric"] not in APB_FABRICS:
            errs.append(f"{w}: link {n}: only masters on AXI-0 or AXI-3 reach the peripheral register space")
    for n in masters:
        if n not in used:
            errs.append(f"{w}: master {n} has no link")
    return True


def layout_block_rows(rl):
    return [[b["name"], b["space"], b["layout"], b["label"], ids_text(b["records"])] for b in rl["blocks"]]


def table_after(lines, heading_prefix):
    """First Markdown table after the heading that starts with heading_prefix; rows as lists of cells."""
    start = next((i for i, l in enumerate(lines) if l.startswith(heading_prefix)), None)
    if start is None:
        return None
    rows, seen = [], False
    for l in lines[start + 1:]:
        if l.startswith("## "):
            break
        if l.startswith("|"):
            seen = True
            rows.append([c.strip() for c in l.strip().strip("|").split("|")])
        elif seen:
            break
    return rows[2:] if len(rows) >= 2 else None


def check_map(space, m, errs):
    w = f"{space} map"
    for k in HEADER_KEYS:
        if k not in m:
            errs.append(f"{w}: missing key {k}")
    if m.get("space") != space:
        errs.append(f"{w}: space is {m.get('space')!r}, expected {space!r}")
    bits = m.get("address_width_bits")
    if not isinstance(bits, int) or bits <= 0:
        errs.append(f"{w}: address_width_bits must be a positive integer")
        return False
    for k in ("address_width_label", "map_label"):
        if m.get(k) not in LABELS:
            errs.append(f"{w}: {k} must be one of {sorted(LABELS)}")
    regions = m.get("regions") or []
    if not regions:
        errs.append(f"{w}: no regions")
        return False
    ok, names, prev_base, prev_end, prev_name = True, set(), -1, -1, None
    keys = REGION_KEYS + APP_REGION_KEYS
    if space == "secure":
        for k in SECURE_HEADER_KEYS:
            if k not in m:
                errs.append(f"{w}: missing key {k}")
        if m.get("attributes_label") not in LABELS:
            errs.append(f"{w}: attributes_label must be one of {sorted(LABELS)}")
    for r in regions:
        name = r.get("name", "?")
        miss = [k for k in keys if k not in r]
        if miss:
            errs.append(f"{w}: region {name}: missing {', '.join(miss)}")
            ok = False
            continue
        if name in names:
            errs.append(f"{w}: duplicate region name {name}")
        names.add(name)
        base, size = r["base"], r["size"]
        if not isinstance(base, int) or not isinstance(size, int) or size <= 0:
            errs.append(f"{w}: region {name}: base and size must be integers and size positive")
            ok = False
            continue
        if base % ALIGN:
            errs.append(f"{w}: region {name}: base {hex(base)} is not 4 KiB aligned")
        if size % ALIGN:
            errs.append(f"{w}: region {name}: size {hex(size)} is not a multiple of 4 KiB")
        end = base + size - 1
        if end >= 1 << bits:
            errs.append(f"{w}: region {name}: ends at {hex(end)}, beyond the {bits}-bit address width")
        if base < prev_base:
            errs.append(f"{w}: region {name} is listed out of ascending order after {prev_name}")
        elif base <= prev_end:
            errs.append(f"{w}: region {name} overlaps {prev_name}")
        prev_base, prev_end, prev_name = base, max(prev_end, end), name
        if r["label"] not in LABELS:
            errs.append(f"{w}: region {name}: label {r['label']!r} is not SELECTED, PROPOSED or OPEN")
        recs = r["records"]
        if not isinstance(recs, list) or not recs or not all(RECORD_RE.match(str(x)) for x in recs):
            errs.append(f"{w}: region {name}: records must be a non-empty list of NX identifiers")
        if not isinstance(r["cacheable"], bool):
            errs.append(f"{w}: region {name}: cacheable must be true or false")
        if not re.fullmatch(r"[r-][w-][x-]", str(r["perm"])):
            errs.append(f"{w}: region {name}: perm must be three characters of r, w, x or -")
        elif space == "secure":
            if r["class"] in ("security_rom", "nor_secure") and r["perm"][1] == "w":
                errs.append(f"{w}: region {name}: a {r['class']} region must not be writable")
            if r["class"] == "crossing_alias" and r["perm"][2] == "x":
                errs.append(f"{w}: region {name}: a crossing_alias region must not be executable")
    return ok


def check_crossings(app, sec, errs):
    by_name = {r.get("name"): r for r in app.get("regions", [])}
    for need in ("System SRAM", "Peripheral register space"):
        if need not in by_name:
            errs.append(f"application map: region {need} is missing")
    sec_names = {r.get("name") for r in sec.get("regions", [])}
    if "Mailbox (secure side)" not in sec_names:
        errs.append("secure map: region Mailbox (secure side) is missing")
    aliases = [r for r in sec.get("regions", []) if r.get("class") == "crossing_alias"]
    if not aliases:
        errs.append("secure map: no crossing_alias region (the boot window) is present")
    for r in aliases:
        name = r.get("name", "?")
        if r.get("target_space") != "application":
            errs.append(f"secure map: alias {name}: target_space must be application")
        tgt = by_name.get(r.get("target_region"))
        if tgt is None:
            errs.append(f"secure map: alias {name}: target_region {r.get('target_region')!r} is not an application region")
            continue
        if r.get("target_base") != tgt.get("base"):
            errs.append(f"secure map: alias {name}: target_base does not equal the base of {tgt['name']}")
        if r.get("size") != tgt.get("size"):
            errs.append(f"secure map: alias {name}: size {size_text(r.get('size', 0))} differs from "
                        f"{tgt['name']} ({size_text(tgt.get('size', 0))})")


def check_periph(app, pw, errs):
    w = "peripheral windows"
    for k in PERIPH_KEYS:
        if k not in pw:
            errs.append(f"{w}: missing key {k}")
    if pw.get("space") != "application_peripheral":
        errs.append(f"{w}: space is {pw.get('space')!r}, expected 'application_peripheral'")
    if pw.get("map_label") not in LABELS:
        errs.append(f"{w}: map_label must be one of {sorted(LABELS)}")
    parent = next((r for r in app.get("regions", []) if r.get("name") == pw.get("parent_region")), None)
    if parent is None:
        errs.append(f"{w}: parent_region {pw.get('parent_region')!r} is not a region of the application map")
        return False
    p_lo, p_hi = parent["base"], parent["base"] + parent["size"] - 1
    apbs, ok = {}, True

    def scan(items, keys, label, lo_hi=None):
        nonlocal ok
        names, prev_base, prev_end, prev_name = set(), -1, -1, None
        for r in items:
            name = r.get("name", "?")
            miss = [k for k in keys if k not in r]
            if miss:
                errs.append(f"{w}: {label} {name}: missing {', '.join(miss)}")
                ok = False
                continue
            if name in names:
                errs.append(f"{w}: duplicate {label} name {name}")
            names.add(name)
            base, size = r["base"], r["size"]
            if not isinstance(base, int) or not isinstance(size, int) or size <= 0:
                errs.append(f"{w}: {label} {name}: base and size must be integers and size positive")
                ok = False
                continue
            if base % ALIGN or size % ALIGN:
                errs.append(f"{w}: {label} {name}: base and size must be multiples of 4 KiB")
            end = base + size - 1
            lo, hi = lo_hi(r) if lo_hi else (p_lo, p_hi)
            if lo is None:
                errs.append(f"{w}: {label} {name}: apb {r.get('apb')!r} is not an APB window")
            elif base < lo or end > hi:
                errs.append(f"{w}: {label} {name}: {hex(base)} to {hex(end)} is outside {hex(lo)} to {hex(hi)}")
            if base < prev_base:
                errs.append(f"{w}: {label} {name} is listed out of ascending order after {prev_name}")
            elif base <= prev_end:
                errs.append(f"{w}: {label} {name} overlaps {prev_name}")
            prev_base, prev_end, prev_name = base, max(prev_end, end), name
            if r["label"] not in LABELS:
                errs.append(f"{w}: {label} {name}: label {r['label']!r} is not SELECTED, PROPOSED or OPEN")
            recs = r["records"]
            if not isinstance(recs, list) or not recs or not all(RECORD_RE.match(str(x)) for x in recs):
                errs.append(f"{w}: {label} {name}: records must be a non-empty list of NX identifiers")

    scan(pw.get("apb_windows") or [], APB_KEYS, "APB window")
    for r in pw.get("apb_windows") or []:
        if isinstance(r.get("base"), int) and isinstance(r.get("size"), int):
            apbs[r.get("name")] = (r["base"], r["base"] + r["size"] - 1)

    def window_range(r):
        a = apbs.get(r.get("apb"))
        return a if a else (None, None)

    wins = pw.get("windows") or []
    if not wins:
        errs.append(f"{w}: no windows")
        return False
    scan(wins, WINDOW_KEYS, "window", window_range)
    have = {r.get("name") for r in wins}
    for need in REQUIRED_WINDOWS:
        if need not in have:
            errs.append(f"{w}: window {need} is missing")
    return ok


def check_records(maps, root, errs):
    req = root / "requirements" / "REQUIREMENTS.md"
    if not req.exists():
        errs.append("requirements/REQUIREMENTS.md not found")
        return
    known = set(re.findall(r"^\| (NX-REQ-\d{3}) \|", req.read_text(encoding="utf-8"), re.M))
    for space, m in maps.items():
        used = set(m.get("map_records", [])) | set(m.get("address_width_records", []))
        for r in m.get("regions", []):
            used |= set(r.get("records", []))
        if space == "secure":
            used |= set(m.get("attributes_records", []))
        if space == "connectivity":
            used |= set(m.get("connectivity_records", []))
            for r in m.get("fabrics", []) + m.get("masters", []) + m.get("attachments", []) + m.get("links", []):
                used |= set(r.get("records", []))
        if space == "layouts":
            used |= set(m.get("layout_records", []))
            for r in m.get("layouts", []) + m.get("blocks", []):
                used |= set(r.get("records", []))
        if space == "peripheral":
            used |= set(m.get("map_records", []))
            for r in m.get("apb_windows", []) + m.get("windows", []):
                used |= set(r.get("records", []))
        for rid in sorted(x for x in used if str(x).startswith("NX-REQ-")):
            if rid not in known:
                errs.append(f"{space} map: {rid} is not in the requirements register")


def check_tables(maps, root, errs):
    doc = root / "architecture" / "ADDRESS_MAP.md"
    if not doc.exists():
        errs.append("architecture/ADDRESS_MAP.md not found")
        return
    lines = doc.read_text(encoding="utf-8").splitlines()
    for space, heading, app in (("application", "## 2. Application address map", True),
                                ("secure", "## 3. Secure address map", False)):
        got = table_after(lines, heading)
        if got is None:
            errs.append(f"ADDRESS_MAP.md: no table under '{heading}'")
            continue
        want = expected_rows(maps[space], app)
        if len(got) != len(want):
            errs.append(f"ADDRESS_MAP.md: {space} table has {len(got)} rows, the file has {len(want)} regions")
        for g, w in zip(got, want):
            if g != w:
                errs.append(f"ADDRESS_MAP.md: {space} row {w[0]!r} differs from the file: table {g} / file {w}")
    rl = maps.get("layouts")
    if rl:
        got = table_after(lines, "## 2.2 Register layouts")
        want = layout_block_rows(rl)
        if got is None:
            errs.append("ADDRESS_MAP.md: no table under '## 2.2 Register layouts'")
        else:
            if len(got) != len(want):
                errs.append(f"ADDRESS_MAP.md: block table has {len(got)} rows, the file has {len(want)} blocks")
            for g, w_ in zip(got, want):
                if g != w_:
                    errs.append(f"ADDRESS_MAP.md: block row {w_[0]!r} differs from the file: table {g} / file {w_}")
        sets = [("common header", [reg_row(r) for r in rl["common_registers"]])]
        for l_ in rl["layouts"]:
            sets.append((l_["name"], [reg_row(r) for r in rl["registers"] if r["layout"] == l_["name"]]))
        for name, want in sets:
            head = f"### Layout {name} ("
            got = table_after(lines[lines.index(next(x for x in lines if x.startswith("## 2.2 Register layouts"))):], head)
            if got is None:
                errs.append(f"ADDRESS_MAP.md: no table under '{head}'")
                continue
            if len(got) != len(want):
                errs.append(f"ADDRESS_MAP.md: layout {name} table has {len(got)} rows, the file has {len(want)} registers")
            for g, w_ in zip(got, want):
                if g != w_:
                    errs.append(f"ADDRESS_MAP.md: layout {name} row {w_[0]!r} differs from the file: table {g} / file {w_}")
    cn = maps.get("connectivity")
    spec = root / SPEC
    if cn:
        if not spec.exists():
            errs.append(f"{SPEC} not found")
        else:
            sl = spec.read_text(encoding="utf-8").splitlines()
            regs, fab, mas, att, mat = conn_tables(cn, maps["application"])
            for head, want in (("### 7.1 Fabrics", fab), ("### 7.2 Masters", mas), ("### 7.3 Region attachments", att),
                               ("### 7.4 Connectivity matrix", mat)):
                got = table_after(sl, head)
                if got is None:
                    errs.append(f"{SPEC}: no table under '{head}'")
                    continue
                if len(got) != len(want):
                    errs.append(f"{SPEC}: table '{head}' has {len(got)} rows, the file has {len(want)}")
                for g, w_ in zip(got, want):
                    if g != w_:
                        errs.append(f"{SPEC}: '{head}' row {w_[0]!r} differs from the file: table {g} / file {w_}")
    pw = maps.get("peripheral")
    if pw:
        heading = "## 2.1 Peripheral register windows"
        got = table_after(lines, heading)
        if got is None:
            errs.append(f"ADDRESS_MAP.md: no table under '{heading}'")
            return
        want = periph_rows(pw)
        if len(got) != len(want):
            errs.append(f"ADDRESS_MAP.md: peripheral table has {len(got)} rows, the file has {len(want)} windows")
        for g, w in zip(got, want):
            if g != w:
                errs.append(f"ADDRESS_MAP.md: peripheral row {w[0]!r} differs from the file: table {g} / file {w}")


def run(root):
    errs, maps = [], {}
    for space, rel in MAPS.items():
        p = root / rel
        if not p.exists():
            errs.append(f"{rel} not found")
            continue
        m = parse(p.read_text(encoding="utf-8"), errs, rel)
        if check_map(space, m, errs):
            maps[space] = m
        if Path(rel).stem != f"{m.get('space')}_map":
            errs.append(f"{rel}: file name does not match space {m.get('space')!r}")
    pp = root / PERIPH
    if not pp.exists():
        errs.append(f"{PERIPH} not found")
    else:
        pw = parse(pp.read_text(encoding="utf-8"), errs, PERIPH)
        if "application" in maps and check_periph(maps["application"], pw, errs):
            maps["peripheral"] = pw
    lp = root / LAYOUTS
    if not lp.exists():
        errs.append(f"{LAYOUTS} not found")
    elif {"application", "secure", "peripheral"} <= set(maps):
        rl = parse(lp.read_text(encoding="utf-8"), errs, LAYOUTS)
        if check_layouts(maps, rl, errs):
            maps["layouts"] = rl
    cp = root / CONN
    if not cp.exists():
        errs.append(f"{CONN} not found")
    elif "application" in maps:
        cn = parse(cp.read_text(encoding="utf-8"), errs, CONN)
        if check_connectivity(maps["application"], cn, errs):
            maps["connectivity"] = cn
    if "application" in maps and "secure" in maps:
        check_crossings(maps["application"], maps["secure"], errs)
        check_records(maps, root, errs)
        check_tables(maps, root, errs)
    return errs, maps


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    errs, maps = run(Path(ap.parse_args().root))
    for e in errs:
        print("FAIL:", e)
    if errs:
        print(f"check_address_maps: {len(errs)} problem(s)")
        return 1
    kind = {"peripheral": ("windows", "windows"), "layouts": ("blocks", "blocks"), "connectivity": ("links", "links")}
    print("check_address_maps ok: " + ", ".join(
        f"{k} {len(v[kind[k][0]]) if k in kind else len(v['regions'])} {kind[k][1] if k in kind else 'regions'}"
        for k, v in maps.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
