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
A PASS does not show that a base, size or attribute is right, that the width fits the C910 or any master,
or that anything is approved; that is review work (NX-REQ-029, NX-ARCH-GAP-003). Exit 0 if it passes, 1 if not.
Stdlib only.
"""
import argparse
import re
import sys
from pathlib import Path

MAPS = {"application": "architecture/maps/application_map.yaml", "secure": "architecture/maps/secure_map.yaml"}
HEADER_KEYS = ["space", "document", "version", "address_width_bits", "address_width_label",
               "address_width_records", "map_label", "map_records", "regions"]
REGION_KEYS = ["name", "base", "size", "class", "label", "records", "note"]
APP_REGION_KEYS = ["cacheable", "perm"]
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
    """Read the small YAML subset the map files use: top-level scalars, one `regions:` list of flat mappings."""
    top, regions, cur, in_regions = {}, [], None, False
    for n, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if indent == 0:
            in_regions = line == "regions:"
            if in_regions:
                top["regions"] = regions
                continue
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
            if not m:
                errs.append(f"{where}:{n}: cannot read line")
                continue
            val = m.group(2)
            if not val.startswith(("\"", "'")) and " #" in val:
                val = val.split(" #", 1)[0]
            top[m.group(1)] = scalar(val)
        elif in_regions:
            if line.startswith("- "):
                cur = {}
                regions.append(cur)
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
        if app:
            cells += ["Yes" if r["cacheable"] else "No", r["perm"]]
        cells += [r["label"], ids_text(r["records"])]
        rows.append(cells)
    return rows


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
    keys = REGION_KEYS + (APP_REGION_KEYS if space == "application" else [])
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
        if space == "application":
            if not isinstance(r["cacheable"], bool):
                errs.append(f"{w}: region {name}: cacheable must be true or false")
            if not re.fullmatch(r"[r-][w-][x-]", str(r["perm"])):
                errs.append(f"{w}: region {name}: perm must be three characters of r, w, x or -")
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
    if len(maps) == 2:
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
    print("check_address_maps ok: " + ", ".join(f"{k} {len(v['regions'])} regions" for k, v in maps.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
