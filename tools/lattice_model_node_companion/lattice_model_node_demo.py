#!/usr/bin/env python3
"""Generate the local Lattice Model Node Companion browser demo."""

from __future__ import annotations

import html
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SEED_PATH = BASE_DIR / "natural_world_lattice_seed.json"
ENGINES_PATH = BASE_DIR / "local_model_engines.json"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "lattice_model_node_demo.html"


COLORS = {
    "core": "#f5c542",
    "Nest 1": "#61dafb",
    "Nest 2": "#7ee787",
    "Nest 3": "#ffb86b",
    "Nest 4": "#ff7ab6",
    "Nest 5": "#c79cff",
    "Adapter": "#8bd3ff",
}


X_BY_NEST = {
    "core": 80,
    "Nest 1": 260,
    "Nest 2": 470,
    "Nest 3": 705,
    "Nest 4": 930,
    "Nest 5": 1140,
    "Adapter": 1350,
}


def load_seed() -> dict:
    return json.loads(SEED_PATH.read_text(encoding="utf-8"))


def load_engines() -> dict:
    if not ENGINES_PATH.exists():
        return {"engines": []}
    return json.loads(ENGINES_PATH.read_text(encoding="utf-8"))


def build_positions(nodes: list[dict]) -> dict[str, dict[str, int]]:
    grouped: dict[str, list[dict]] = {}
    for node in nodes:
        grouped.setdefault(node["nest"], []).append(node)

    positions: dict[str, dict[str, int]] = {}
    for nest, nest_nodes in grouped.items():
        x = X_BY_NEST.get(nest, 80)
        gap = 72 if nest != "Nest 2" else 62
        for index, node in enumerate(nest_nodes):
            if nest == "core":
                y = 220 + index * 76
            else:
                y = 80 + index * gap
            positions[node["id"]] = {"x": x, "y": y}
    return positions


def svg_markup(data: dict, positions: dict[str, dict[str, int]]) -> str:
    node_by_id = {node["id"]: node for node in data["nodes"]}
    edge_parts = []
    for edge in data["edges"]:
        source = positions[edge["source"]]
        target = positions[edge["target"]]
        edge_parts.append(
            f'<line class="edge source-{edge["source"]} target-{edge["target"]}" '
            f'x1="{source["x"] + 130}" y1="{source["y"] + 24}" '
            f'x2="{target["x"]}" y2="{target["y"] + 24}">'
            f"<title>{html.escape(edge['relation'])}</title></line>"
        )

    node_parts = []
    for node in data["nodes"]:
        pos = positions[node["id"]]
        color = COLORS.get(node["nest"], "#9aa7b2")
        label = html.escape(node["label"])
        node_parts.append(
            f'<g class="node" data-node-id="{node["id"]}" tabindex="0" '
            f'transform="translate({pos["x"]},{pos["y"]})">'
            f'<rect width="152" height="48" rx="14" fill="#101b26" '
            f'stroke="{color}" stroke-width="2" />'
            f'<circle cx="16" cy="24" r="6" fill="{color}" />'
            f'<text x="30" y="21">{label}</text>'
            f'<text x="30" y="37" class="mini">{html.escape(node["status"])}</text>'
            f"<title>{html.escape(node_by_id[node['id']]['description'])}</title>"
            f"</g>"
        )

    return "\n".join(edge_parts + node_parts)


def render_html(data: dict) -> str:
    engines = load_engines()
    positions = build_positions(data["nodes"])
    payload = json.dumps(data, ensure_ascii=False)
    engine_payload = json.dumps(engines, ensure_ascii=False)
    positions_payload = json.dumps(positions)
    svg = svg_markup(data, positions)
    title = html.escape(data["meta"]["title"])
    schema = html.escape(data["meta"]["schema"])

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    :root {{
      --bg: #071014;
      --panel: #0f1a22;
      --panel-2: #111f2a;
      --text: #f4f7fb;
      --muted: #a7b3c2;
      --line: #244353;
      --gold: #f5c542;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at 12% 8%, rgba(245, 197, 66, 0.14), transparent 22rem),
        radial-gradient(circle at 85% 20%, rgba(97, 218, 251, 0.12), transparent 22rem),
        linear-gradient(135deg, #071014 0%, #0a1219 60%, #071014 100%);
      color: var(--text);
      font-family: Avenir Next, Futura, Trebuchet MS, sans-serif;
    }}
    header {{
      padding: 24px 28px 12px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(28px, 4vw, 52px);
      letter-spacing: -0.04em;
    }}
    .tagline {{
      margin: 0;
      color: var(--muted);
      max-width: 980px;
      line-height: 1.45;
    }}
    .schema {{
      display: inline-block;
      margin-top: 12px;
      padding: 8px 12px;
      border: 1px solid rgba(245,197,66,0.42);
      border-radius: 999px;
      color: #ffe38a;
      background: rgba(245,197,66,0.08);
      font-size: 13px;
    }}
    main {{
      display: grid;
      grid-template-columns: minmax(330px, 420px) minmax(640px, 1fr);
      min-height: calc(100vh - 135px);
    }}
    aside {{
      border-right: 1px solid rgba(255,255,255,0.08);
      padding: 20px;
      background: rgba(5, 12, 17, 0.48);
    }}
    .map-wrap {{
      overflow: auto;
      padding: 20px;
    }}
    .card {{
      background: linear-gradient(180deg, rgba(17,31,42,0.95), rgba(10,18,25,0.96));
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 18px;
      padding: 16px;
      box-shadow: 0 18px 40px rgba(0,0,0,0.18);
      margin-bottom: 16px;
    }}
    label {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    input {{
      width: 100%;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 14px;
      padding: 12px 14px;
      color: var(--text);
      background: #08131b;
      outline: none;
      font-size: 15px;
    }}
    button {{
      border: 0;
      border-radius: 999px;
      padding: 9px 12px;
      margin: 8px 6px 0 0;
      cursor: pointer;
      color: #071014;
      background: var(--gold);
      font-weight: 700;
    }}
    button.secondary {{
      color: var(--text);
      background: #1b2d3a;
      border: 1px solid rgba(255,255,255,0.1);
    }}
    .chat {{
      display: grid;
      gap: 10px;
      margin-top: 14px;
    }}
    .bubble {{
      padding: 12px 14px;
      border-radius: 16px;
      line-height: 1.45;
      font-size: 14px;
    }}
    .bubble.user {{
      justify-self: end;
      background: #1b6fed;
      max-width: 88%;
    }}
    .bubble.ai {{
      background: #142331;
      border: 1px solid rgba(255,255,255,0.08);
    }}
    .node-detail h2 {{
      margin: 0 0 8px;
      font-size: 22px;
    }}
    .node-detail p {{
      margin: 8px 0;
      color: var(--muted);
      line-height: 1.45;
    }}
    .pill {{
      display: inline-block;
      margin: 4px 6px 0 0;
      padding: 5px 8px;
      border-radius: 999px;
      background: #1e3543;
      color: #d9edf7;
      font-size: 12px;
    }}
    .engine-list {{
      display: grid;
      gap: 10px;
      margin-top: 10px;
    }}
    .engine {{
      padding: 10px 12px;
      border-radius: 14px;
      background: #0b1720;
      border: 1px solid rgba(255,255,255,0.09);
    }}
    .engine strong {{
      display: block;
      font-size: 13px;
    }}
    .engine code {{
      display: block;
      margin-top: 6px;
      color: #f5c542;
      white-space: normal;
      font-size: 11px;
    }}
    .engine small {{
      color: var(--muted);
    }}
    svg {{
      min-width: 1530px;
      min-height: 980px;
      background:
        linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px),
        linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px);
      background-size: 80px 80px;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 22px;
    }}
    .edge {{
      stroke: var(--line);
      stroke-width: 1.4;
      opacity: 0.55;
    }}
    .node {{
      cursor: pointer;
      transition: opacity 140ms ease, transform 140ms ease;
    }}
    .node text {{
      fill: var(--text);
      font-size: 11px;
      font-weight: 700;
      pointer-events: none;
    }}
    .node text.mini {{
      fill: var(--muted);
      font-size: 8.5px;
      font-weight: 500;
    }}
    .node.dim, .edge.dim {{ opacity: 0.13; }}
    .node.hot rect {{
      filter: drop-shadow(0 0 12px rgba(245,197,66,0.55));
      stroke-width: 3;
    }}
    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }}
    .legend span {{
      font-size: 12px;
      color: var(--muted);
    }}
    @media (max-width: 980px) {{
      main {{ grid-template-columns: 1fr; }}
      aside {{ border-right: 0; border-bottom: 1px solid rgba(255,255,255,0.08); }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p class="tagline">Local, no-credit browser companion for mapping Mirror Architecture across formal systems, matter, nutrition, coherence, biology, natural systems, and future physics/material AI adapters.</p>
    <span class="schema">{schema}</span>
  </header>
  <main>
    <aside>
      <section class="card">
        <label for="prompt">Ask / filter the lattice</label>
        <input id="prompt" placeholder="Try: nutrition, NVIDIA, fusion, HRV, PFAS, water..." />
        <button id="ask">Ask map</button>
        <button class="secondary" id="reset">Reset</button>
        <div class="legend">
          <span>Click nodes or ask short prompts.</span>
          <span>No external calls.</span>
          <span>No credits spent.</span>
        </div>
        <div class="chat" id="chat">
          <div class="bubble ai">Companion online. Pick a node or ask how a domain maps through the nests.</div>
        </div>
      </section>
      <section class="card node-detail" id="detail">
        <h2>Mirror Architecture</h2>
        <p>Unified architecture layer that maps state, control, transform, invariant, drift, coherence, and score across domains.</p>
        <span class="pill">core</span><span class="pill">active spine</span>
      </section>
      <section class="card">
        <label>Local model engines</label>
        <div class="engine-list" id="engine-list"></div>
      </section>
    </aside>
    <section class="map-wrap">
      <svg viewBox="0 0 1530 980" role="img" aria-label="Lattice node map">
        {svg}
      </svg>
    </section>
  </main>
  <script>
    const DATA = {payload};
    const ENGINES = {engine_payload};
    const POSITIONS = {positions_payload};
    const nodeById = Object.fromEntries(DATA.nodes.map(node => [node.id, node]));
    const chat = document.querySelector("#chat");
    const promptInput = document.querySelector("#prompt");
    const detail = document.querySelector("#detail");
    const engineList = document.querySelector("#engine-list");

    function addBubble(text, who = "ai") {{
      const bubble = document.createElement("div");
      bubble.className = `bubble ${{who}}`;
      bubble.textContent = text;
      chat.appendChild(bubble);
      chat.scrollTop = chat.scrollHeight;
    }}

    function connectedIds(id) {{
      const ids = new Set([id]);
      DATA.edges.forEach(edge => {{
        if (edge.source === id) ids.add(edge.target);
        if (edge.target === id) ids.add(edge.source);
      }});
      return ids;
    }}

    function showNode(id, announce = true) {{
      const node = nodeById[id];
      if (!node) return;
      const neighbors = connectedIds(id);
      document.querySelectorAll(".node").forEach(el => {{
        const nodeId = el.dataset.nodeId;
        el.classList.toggle("dim", !neighbors.has(nodeId));
        el.classList.toggle("hot", nodeId === id);
      }});
      document.querySelectorAll(".edge").forEach(el => {{
        const keep = el.classList.contains(`source-${{id}}`) || el.classList.contains(`target-${{id}}`);
        el.classList.toggle("dim", !keep);
      }});
      detail.innerHTML = `
        <h2>${{node.label}}</h2>
        <p>${{node.description}}</p>
        <span class="pill">${{node.nest}}</span>
        <span class="pill">${{node.type}}</span>
        <span class="pill">${{node.status}}</span>
      `;
      if (announce) addBubble(`${{node.label}} maps as ${{node.nest}}: ${{node.description}}`);
    }}

    function resetMap() {{
      document.querySelectorAll(".node,.edge").forEach(el => el.classList.remove("dim", "hot"));
      showNode("mirror_architecture", false);
      addBubble("Reset to the full lattice. The build is local-only and ready for iterative nest expansion.");
    }}

    function renderEngines() {{
      engineList.innerHTML = "";
      ENGINES.engines.forEach(engine => {{
        const el = document.createElement("div");
        el.className = "engine";
        el.innerHTML = `
          <strong>${{engine.label}}</strong>
          <small>${{engine.status}} · ${{engine.maps_to.join(", ")}}</small>
          <code>${{engine.command}}</code>
        `;
        el.addEventListener("click", () => {{
          addBubble(`${{engine.label}}`, "user");
          addBubble(`${{engine.description}} Command: ${{engine.command}}`);
        }});
        engineList.appendChild(el);
      }});
    }}

    function findMatches(query) {{
      const q = query.trim().toLowerCase();
      if (!q) return [];
      return DATA.nodes.filter(node => (
        node.label.toLowerCase().includes(q) ||
        node.id.toLowerCase().includes(q) ||
        node.description.toLowerCase().includes(q) ||
        node.type.toLowerCase().includes(q) ||
        node.nest.toLowerCase().includes(q)
      ));
    }}

    function answerPrompt(query) {{
      const q = query.trim().toLowerCase();
      if (!q) return "Ask a short mapping prompt: source mirror, unified proof, prototype lanes, nutrition, NVIDIA, fusion, HRV, PFAS, terahertz, topology, water, plasma, cells, or materials.";
      if (q.includes("source") || q.includes("source mirror")) {{
        showNode("source_mirror_pattern", false);
        return "The Source Mirror Pattern is the named recurring structure across formal systems, matter, dynamics, biology, cosmic systems, AI hidden states, and prototype engines.";
      }}
      if (q.includes("unified") || q.includes("proof")) {{
        showNode("unified_mirror_proof", false);
        return "The Unified Mirror Proof is the living evidence spine: AI measurement, encoded circuits, hardware, biology, formal math, matter, dynamics, cosmic convergence, and local engines.";
      }}
      if (q.includes("prototype") || q.includes("lane") || q.includes("precursor")) {{
        showNode("prototype_lanes", false);
        return "Prototype lanes are crossover build paths: PFAS breakdown, terahertz cellular mapping, HRV-AI tuning, Quantum Insider tracks, and later local engines.";
      }}
      if (q.includes("engine 02") || q.includes("engine02") || q.includes("nest 2 engine") || q.includes("chemistry engine") || q.includes("matter engine")) {{
        showNode("engine02_nest2_matter", false);
        return "Engine 02 is the built Nest 2 local demonstrator: element-family recovery, molecular graph validity, H2O motif scoring, mineral/redox/nutrition rows, and contaminant bad-descendant controls.";
      }}
      if (q.includes("topology") || q.includes("topography")) {{
        showNode("nest1_expanded_formal", false);
        return "Expanded Nest 1 separates topology from topography: topology tracks connectedness and deformation-stable structure; topography tracks surfaces, ridges, basins, gradients, and localization.";
      }}
      if (q.includes("nutrition") || q.includes("food") || q.includes("protein") || q.includes("carb") || q.includes("fat") || q.includes("vitamin")) {{
        showNode("food_chemistry", false);
        return "Nutrition maps first as Nest 2 chemistry: proteins, carbs, fats, vitamins, minerals, hydration, and food transforms. It bridges upward into Nest 4 metabolism, HRV/EEG, cells, microbiome, and physiology.";
      }}
      if (q.includes("terahertz") || q.includes("thz")) {{
        showNode("terahertz_cellular_lane", false);
        return "Terahertz is a Nest 3 -> Nest 4 precursor lane: spectral pattern, water/molecular response, cellular/DNA state movement, measured state vectors, and bounded controls.";
      }}
      if (q.includes("nvidia") || q.includes("physicsnemo") || q.includes("physics")) {{
        showNode("nvidia_physicsnemo", false);
        return "NVIDIA PhysicsNeMo is a future adapter slot, not a claim surface yet. It belongs beside Nest 3 for fields, fluids, plasma, resonance, PDE-like dynamics, and engineered physics simulations.";
      }}
      if (q.includes("material") || q.includes("mattergen") || q.includes("chgnet") || q.includes("mace") || q.includes("matgl")) {{
        showNode("materials_models", false);
        return "Materials models plug into Nest 2: elements, molecules, crystals, minerals, lattices, and atomistic graph structure. The companion keeps a stable node schema so those adapters can be added later.";
      }}
      if (q.includes("pfas") || q.includes("forever") || q.includes("pharma") || q.includes("plastic")) {{
        showNode("pfas_pharma_microplastics", false);
        return "Persistent contaminants map through Nest 2 bond topology and reaction pathways, then Nest 3 remediation conditions. The score must include safe endpoints and penalties for harmful descendants.";
      }}
      if (q.includes("hrv") || q.includes("eeg") || q.includes("human")) {{
        showNode("hrv_eeg", false);
        return "HRV/EEG are Nest 4 biosignal adapters. HRV has the first matrix; EEG is the planned simultaneous layer. Later this can become a live human-state input into the map.";
      }}
      if (q.includes("fusion") || q.includes("solar") || q.includes("hydrogen")) {{
        showNode("fusion_solar", false);
        return "Hydrogen starts in Nest 2 as element/isotope structure. Fusion moves into Nest 3 plasma and energy dynamics. Solar becomes Nest 5 because plasma, fusion, EM fields, cycles, and planetary coupling converge.";
      }}
      if (q.includes("water") || q.includes("h2o")) {{
        showNode("h2o", false);
        return "H2O maps as Nest 2 molecular structure with a Nest 3 bridge: bond angle, polarity, hydrogen bonding, hydration shells, phase, terahertz, and biology-facing water networks.";
      }}
      const matches = findMatches(q);
      if (matches.length) {{
        showNode(matches[0].id, false);
        return `Found ${{matches.length}} matching node(s). Showing ${{matches[0].label}} first.`;
      }}
      showNode("mirror_architecture", false);
      return "I do not have that node yet. Add it to natural_world_lattice_seed.json with a nest, state object, invariant, drift mode, and bridge relation.";
    }}

    document.querySelectorAll(".node").forEach(node => {{
      node.addEventListener("click", () => showNode(node.dataset.nodeId));
      node.addEventListener("keydown", event => {{
        if (event.key === "Enter") showNode(node.dataset.nodeId);
      }});
    }});

    document.querySelector("#ask").addEventListener("click", () => {{
      const query = promptInput.value;
      addBubble(query || "(empty prompt)", "user");
      addBubble(answerPrompt(query), "ai");
    }});

    promptInput.addEventListener("keydown", event => {{
      if (event.key === "Enter") document.querySelector("#ask").click();
    }});

    document.querySelector("#reset").addEventListener("click", resetMap);
    renderEngines();
    showNode("mirror_architecture", false);
  </script>
</body>
</html>
"""


def main() -> None:
    data = load_seed()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_html(data), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print("Open that file in a browser to test the local companion UI.")


if __name__ == "__main__":
    main()
