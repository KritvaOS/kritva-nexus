# Kritva Nexus Interconnect Specification

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-ARCH-002 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Specification |
| Status | DRAFT (first part: the route for NX-ARCH-GAP-001 is selected by the owner; proposal for NX-ARCH-GAP-004; not reviewed or approved) |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.1.0-draft |
| Last Updated | 2026-11-09 |
| Authority | INPUT (not AUTHORITATIVE until the owner approves it) |
| Related Tasks / Milestones | KOS-NEXUS-007; NX-M1 |
| Related Documents | [System architecture](SYSTEM_ARCHITECTURE.md); [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md); [A0 integration draft](A0_INTEGRATION_DRAFT.md) |

## Purpose

This document specifies the application AXI and memory-access architecture of the Nexus SoC. Its first part works on the two open items that belong to KOS-NEXUS-007: the C910 access path to the APB peripherals (NX-ARCH-GAP-001, AC-014) and the DDR4 controller ingress topology and port count (NX-ARCH-GAP-004, AC-016). For each it states the required behaviour, the options, a recommendation and the decisions the owner is asked to make. It is written for the owner and for the engineers who will write the memory and address-map documents (KOS-NEXUS-008) and the interconnect RTL.

## 1. Status of this part

With one exception, everything here is a PROPOSAL (label PROPOSED). The exception is the route in section 3: on 2026-11-09 the owner chose Option A for NX-ARCH-GAP-001, recorded as NX-DEC-021 and NX-REQ-067 (SELECTED). That choice does not close the gap: the behaviour of the path in 3.1 stays PROPOSED or OPEN, so NX-REQ-027 stays OPEN. NX-ARCH-GAP-004 and NX-REQ-030 stay OPEN until the owner states a decision. After a decision, the owner's wording is recorded as an NX-DEC record, the requirement is updated with a changelog entry, and this document is corrected. A recommendation from an agent or another AI tool does not make a choice SELECTED. Figures are theoretical interface arithmetic or assumptions, not measured results; no timing, bandwidth or latency result exists.

Later parts of KOS-NEXUS-007 add the secure fabric, the APB bridge details, QoS and protection at the memory-access layer and the connectivity matrix.

## 2. Inputs and assumptions

| ID | Item | Source | Label |
|---|---|---|---|
| IN-1 | Four application AXI fabrics, AXI-0 (128-bit), AXI-1 (256-bit), AXI-2 (128-bit) and AXI-3 (64-bit), at 400 to 600 MHz. Only the count is SELECTED. | NX-REQ-015, NX-DEC-014; NX-REQ-050 | SELECTED count; PROPOSED widths |
| IN-2 | Two AXI-to-APB interconnects (APB-0 and APB-1), 32-bit APB, 200 to 250 MHz target. Only the count is SELECTED. | NX-REQ-016, NX-DEC-015; NX-REQ-052 | SELECTED count; PROPOSED parameters |
| IN-3 | The C910 attaches to AXI-0 with a 128-bit AXI4 interface and 8 outstanding reads and writes; the C910 configuration is not confirmed. | NX-REQ-051, NX-REQ-056; NX-ARCH-OI-001 | PROPOSED |
| IN-4 | A Memory Access Crossbar (MAX) with four fabric ingress ports provides arbitration, QoS, address decode and protection toward memory. | NX-REQ-049 | PROPOSED |
| IN-5 | DDR4 is the primary system memory, targeting DDR4-3200 (3200 MT/s per pin). Data width and capacity are not selected. | NX-REQ-002, NX-DEC-001; NX-REQ-064; NX-ARCH-OI-005 | SELECTED role; PROPOSED target; OPEN width |
| IN-6 | The normal camera, ISP and NPU path does not use DDR4 for intermediates. | NX-REQ-047 | PROPOSED |
| IN-7 | Peripheral register windows are proposed near 0x40000000 (APB-0 peripherals) and 0x41000000 (APB-1 control). The application address map is held by KOS-NEXUS-008. | NX-REQ-052, NX-REQ-053 | PROPOSED |

## 3. C910 to APB path (NX-ARCH-GAP-001, AC-014)

### 3.1 Required behaviour

The path from a C910 load or store to an APB register, and back, carries register traffic only; DMA data does not use it. The specification of the path must define each item below. The items are requirements on the specification, not yet decisions.

| Area | What must be defined |
|---|---|
| Route and conversion | The route, where each conversion happens (width, clock, protocol), the protocol version on each side of every bridge, and whether width conversion and clock-domain crossing are in one bridge or separate blocks |
| Decode and attributes | The address decode that selects APB-0, APB-1 or neither; the access attributes (device, non-cacheable, ordered, non-speculative) |
| Ordering | Ordering across AXI IDs and across APB targets; whether the bridge serialises device accesses or lets independent targets progress |
| Bursts | Supported burst types and lengths, burst splitting, alignment, byte strobes and the behaviour for an unsupported transaction |
| Outstanding traffic | Buffering limits, backpressure, ID handling and how a response is matched to its original AXI transaction after width conversion |
| Responses | Handling of DECERR, SLVERR, downstream errors and malformed or unsupported transactions |
| Timeout | Timeout scope, the response, recovery, and whether a timed-out APB transaction can still complete later; the numerical value stays OPEN |
| APB errors | PSLVERR propagation and the behaviour for a target that never asserts PREADY |
| Access control | The trusted address-window decode, the allowed AxPROT attributes, default-deny for any access not explicitly allowed, and that protection is checked before an APB access is issued |
| Reset | The behaviour of in-flight transactions during bridge or peripheral reset and during clock-domain reset release |
| Placement | Where the bridges sit |

### 3.2 Options

| Option | Route | Advantages | Drawbacks |
|---|---|---|---|
| A | C910, AXI-0, an AXI fabric bridge from AXI-0 to AXI-3 (128-bit to 64-bit width conversion and a clock crossing), AXI-3 decode, then the APB-0 and APB-1 bridges as slaves of AXI-3 | Uses AXI-3 for its proposed control role; keeps register traffic out of the AXI-0 data fabric; one decode point for all peripherals | Two hops and a width and clock conversion add latency (not quantified); AXI-3 also carries peripheral and I2S DMA, so register access can contend with it unless QoS separates them |
| B | C910, AXI-0, the APB-0 and APB-1 bridges as direct slaves of AXI-0 | Shortest route for the CPU; no conversion bridge | Peripheral registers sit on the CPU and memory fabric; the bridges' clock and width conversion load AXI-0; other masters needing register access would need a path to AXI-0 |
| C | A separate peripheral or uncached port of the C910 cluster to the bridges | Isolates register traffic from the memory port | Depends on the selected C910 configuration offering such a port; UNVERIFIED and tied to NX-ARCH-OI-001 |

### 3.3 Selected route and proposed behaviour

The owner chose Option A (SELECTED, NX-DEC-021, NX-REQ-067), subject to the C910 configuration check. The behaviour below is the recommendation made with the option and is PROPOSED until the owner confirms it; it is not selected by the choice of the route.

Option A. Register accesses are routed from AXI-0 to AXI-3 by the AXI-0 decode and an AXI fabric bridge (a bridge between the named fabrics, not an AXI4 to AXI3 protocol conversion; the protocol version on each side is assumed AXI4 and is OPEN for AXI-3 and the APB bridges); AXI-3 decodes the APB-0 and APB-1 windows. The accesses are device-type and strongly ordered, with one outstanding transaction per APB target unless a later analysis shows otherwise. An access to an unmapped address returns DECERR; a denied access returns SLVERR; an APB PSLVERR is returned as SLVERR; each reaches the C910 as a bus error. A bridge timeout for a hung slave returns SLVERR; the timeout value is OPEN. The bridge enforces a trusted address-window policy with default-deny: an access is issued to APB only if its window and its AxPROT attributes are explicitly allowed, and the check is made before the APB access is issued. AxPROT alone is not the security boundary. The application domain cannot change the policy for secure resources, which are never reachable on this path (NX-REQ-034). Whether Option C is available is confirmed after the C910 configuration check, and the recommendation is revisited if it is.

### 3.4 Decisions still requested from the owner

Decided: the route is Option A (NX-DEC-021). Still requested, and until they are stated NX-REQ-027 stays OPEN:

1. Confirm the error-response mapping in 3.3, or state another.
2. State the timeout policy or leave it OPEN with an owner.
3. Confirm that an access from a master other than the C910 to the APB windows is out of scope for this path, or state which masters need it.
4. State whether width conversion and the clock crossing are one bridge or separate blocks, and the protocol version of AXI-3 and the APB bridges, or leave both OPEN with an owner.

## 4. DDR4 controller ingress (NX-ARCH-GAP-004, AC-016)

### 4.1 Demand known so far

The A0 draft documents these DDR4 consumers. All figures are the draft's workload arithmetic and do not include burst, arbitration or refresh overhead.

| Consumer | Documented traffic | Source |
|---|---|---|
| Display, three full-screen layers, XRGB8888 | 663.552 MB/s read | A0 draft 5.4 |
| Ethernet, two MACs at 1 Gbps full duplex | 500 MB/s as an upper bound (2 MACs x 2 directions x 125 MB/s); only directions that DMA to or from DDR4 count, descriptor traffic is not included | Derived here from NX-REQ-040 (1000 Mbps per MAC); not an A0 figure |
| Camera RGB888 output, only if sent to DDR4 (optional use) | 49.152 MB/s write | A0 draft 3.8 |
| C910 cluster | Not documented | OPEN |
| NPU models, weights and large activations | Not documented | OPEN, NX-ARCH-OI-010 |
| DMA buffers, recording, other system memory | Not documented | OPEN; recording and optional intermediates are NX-ARCH-OI-011 |

The documented consumers add up to about 1.213 GB/s. The CPU and NPU, which are expected to dominate DDR4 traffic, have no documented bandwidth. AC-016 therefore cannot be completed from documented requirements: the derivation below is a method with its inputs shown, and the CPU and NPU demand is an owner or engineering input.

### 4.2 Capacity

DDR4-3200 gives 6.4 GB/s of theoretical peak per 16 bits of data width. An AXI port gives its width times its clock in each direction.

| DDR4 data width | Theoretical peak | Minimum ingress ports for one direction to carry the whole peak |
|---|---|---|
| x16 | 6.4 GB/s | 1 at 128-bit and 500 MHz (8 GB/s) |
| x32 | 12.8 GB/s | 2 at 128-bit and 500 MHz; 1 at 256-bit and 500 MHz (16 GB/s) |
| x64 | 25.6 GB/s | 4 at 128-bit and 500 MHz; 2 at 256-bit and 500 MHz |

The rule is: ports = ceil(DDR4 peak bandwidth / per-direction bandwidth of one port), taking the worst case of one direction carrying the whole stream. The table values are interface peaks, not sustainable payload bandwidth. Sustained bandwidth is lower because of DDR4 efficiency, refresh, row and bank behaviour, read and write turnaround, burst length, arbitration, AXI overhead and the controller's real clocking, and none of these is assumed here. The table also assumes the port bandwidth is per direction and that the controller can sustain simultaneous read and write traffic at those rates; both are unconfirmed. The known demand of about 1.213 GB/s is below the peak of every width in the table; whether the CPU and NPU demand fits is not known.

### 4.3 Options

| Option | Topology | Advantages | Drawbacks |
|---|---|---|---|
| A | The MAX takes the four fabric ingress ports and presents one port to the DDR4 controller | Simplest; one arbitration point; matches the proposed MAX | One port is limited to its per-direction bandwidth, which is enough only for narrow DDR4 widths or a 256-bit port |
| B | The MAX presents two ports to the controller, split by address interleave or by traffic class | Covers x32 with 128-bit ports and part of x64; keeps the MAX | Interleave or class split and controller support for multiple ports need specification; extra area and complexity |
| C | The fabrics connect directly to a multi-port DDR4 controller with no separate MAX | Fewest hops | Conflicts with the proposed MAX (NX-REQ-049) if the MAX is meant to be the sole aggregation point; arbitration, QoS and protection move into the controller IP, which is not selected. A controller with one AXI ingress and internal arbitration is a different topology from a genuinely multi-port controller, and the intended topology must be stated before the options are compared |

### 4.4 Recommendation (PROPOSED)

Keep the MAX (Option A or B) and fix the controller port count from the rule in 4.2 once the DDR4 data width and the CPU and NPU demand are stated. Until those two inputs exist, no port count is recommended; the document does not pick a number the inputs cannot support. If the owner states a width and a demand, the table gives the count. If the width is x32 or less, Option A with a 256-bit port is sufficient on theoretical grounds. If it is x64, Option B with two 256-bit ports or four 128-bit ports is the minimum.

### 4.5 Decisions requested from the owner

1. State the intended DDR4 data width, or record that it stays OPEN with an owner (NX-ARCH-OI-005).
2. State the planned CPU and NPU DDR4 bandwidth demand, or ask for an estimate from the NPU and CPU work; until then NX-REQ-030 stays OPEN.
3. Choose Option A, B or C, or defer the choice until 1 and 2 are known.
4. State whether the sustained-efficiency assumption is a fixed value or an analysis output.

## 5. Effect on the gaps

| Gap | Requirement | State after this part |
|---|---|---|
| NX-ARCH-GAP-001 | NX-REQ-027 | Route SELECTED (NX-DEC-021, NX-REQ-067); behaviour PROPOSED; gap narrowed and still OPEN; four decisions still requested |
| NX-ARCH-GAP-004 | NX-REQ-030 | OPEN; method and options in section 4 |

AC-016 is not met by this part. It requires the number and width of the memory-access ports to be derived from documented bandwidth requirements. The missing inputs are the DDR4 data width and controller efficiency assumption, the CPU read and write demand and peak, the NPU model, activation and weight traffic, the concurrent display, Ethernet and camera traffic, and the headroom and QoS or latency constraints. The closure method is the rule in 4.2 once those inputs are documented. Until then the issue stays OPEN with Dinesh as owner; leaving it OPEN is a disposition of the gap, not a pass of the criterion.
