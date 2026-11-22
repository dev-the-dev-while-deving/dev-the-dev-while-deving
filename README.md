<!-- Material 3 Expressive profile. Each image has a light and a dark version that follows the viewer's GitHub theme. -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" width="100%" alt="I build tools out of irritations. AI engineer — CS at RV University, BS Data Science at IIT Madras.">
</picture>

<p>
  <a href="https://termbrowse.vercel.app"><img src="https://img.shields.io/badge/termbrowse-live-386A20?style=for-the-badge" alt="termbrowse live"></a>
  <a href="#projects"><img src="https://img.shields.io/badge/see-projects-B7F397?style=for-the-badge&labelColor=042100" alt="See projects"></a>
</p>

I'm an AI engineer. Most of my projects start as a frustration: a browser that's too heavy, a study app that forces a choice, an agent demo that hides its failures. Right now I'm working on agents, small reasoning models and ML that runs on the edge.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/frontier-dark.svg">
  <img src="assets/frontier-light.svg" width="100%" alt="AI engineer on the frontier: AI agents, reasoning models, ML for control systems, edge AI and IoT, local-first software, agent red-teaming">
</picture>

## Flagship: Paidva, a research agent that shows its work

<a href="https://github.com/dev-the-dev-while-deving/paidva-research-agent">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/paidva-dark.svg">
  <img src="assets/paidva-light.svg" width="100%" alt="Paidva, my flagship: a research agent that shows its work. Tagged claims, sandboxed maths, verified citations, ranked confidence. Rust, V1.">
</picture>
</a>

Ask most AI research tools a question and you get a confident paragraph with links. Some links don't support the claim, the "95% sure" means nothing, and nobody checked the maths. **Paidva** is my answer to that. It's a Rust agent where **the model proposes and code decides**:

- **Every claim is tagged** `observed` · `sourced` · `inferred` · `knowledge` · `speculation`, so you can see where each sentence came from.
- **Every number is computed** in a sandboxed Python run and cross-checked against simulation, never recalled from memory.
- **Every citation is verified**: the quote must appear word for word in the source, and a separate checker must agree it supports the claim.
- **Every answer gets a confidence score you can rank by**, and false premises get flagged instead of answered.

**First eval round** (same model, alone vs. inside Paidva): on qwen3.8-27b, accuracy went from 65% to 87%, calibration error from 0.34 to 0.13, and dead citations went to zero across every run. The answers it was most confident about were right 80% of the time on the hard set, versus 38% for the plain model. The sample is still small, so these results aren't significant yet, and the write-up says so.

**Where it's going:** V1 proves the system beats the bare model. V2 has the agent propose its own improvements from its failures, and tests a reasoning layer built on Nyaya logic (*pramana* evidence types and *hetvabhasa* fallacy checks). V3 asks whether a small agent can **keep improving itself round after round** instead of stalling after one gain.

**[→ Read the code and try it](https://github.com/dev-the-dev-while-deving/paidva-research-agent)** · <sub>Rust · free-tier open-weight models · $0/month · open source (AGPL-3.0)</sub>

## Building now

<a href="https://github.com/dev-the-dev-while-deving/meant">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/now-dark.svg">
    <img src="assets/now-light.svg" width="100%" alt="Building now: Meant, swap the scroll for what you meant to do. Android app, v0.3.">
  </picture>
</a>

**Latest pushes** <sub>(updated daily)</sub>

<!-- LATEST:START -->
- [**paidva-research-agent**](https://github.com/dev-the-dev-while-deving/paidva-research-agent) · Paidva: a research and statistics agent that shows its work. Tagged claims, sandboxed maths, verified citations, confidence you can rank by. Rust · free-tier models · AGPL-3.0. · <sub>pushed 2026-11-22</sub>
- [**meant**](https://github.com/dev-the-dev-while-deving/meant) · Meant: swap the scroll for what you meant to do (Android) · <sub>pushed 2026-11-15</sub>
- [**MiniNet**](https://github.com/dev-the-dev-while-deving/MiniNet) · Fortress-Net: a self-healing, AI-assisted secure network built in Mininet (OVS, FRR, strongSwan, Suricata) · <sub>pushed 2026-11-08</sub>
<!-- LATEST:END -->

<a id="projects"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/built-dark.svg">
  <img src="assets/built-light.svg" width="100%" alt="Things I built: a rotating 3D wireframe icosahedron beside 3D extruded lettering">
</picture>

<a href="https://github.com/dev-the-dev-while-deving/termbrowse">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/termbrowse-dark.svg">
    <img src="assets/termbrowse-light.svg" width="100%" alt="termbrowse — reads the web from a terminal (Rust)">
  </picture>
</a>

<a href="https://github.com/dev-the-dev-while-deving/Enigma-Hackthon"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/enigma-dark.svg"><img src="assets/enigma-light.svg" width="49%" alt="ENIGMA — Bayesian MPC agent for safe highway driving"></picture></a>
<a href="https://github.com/dev-the-dev-while-deving/breakbench"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/breakbench-dark.svg"><img src="assets/breakbench-light.svg" width="49%" alt="breakbench — breaks AI agents on purpose"></picture></a>
<a href="https://github.com/dev-the-dev-while-deving/rolldeep-lab"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/rolldeep-dark.svg"><img src="assets/rolldeep-light.svg" width="49%" alt="ROLLDEEP — a free local study lab"></picture></a>
<a href="https://github.com/dev-the-dev-while-deving/SmartStocks"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/smartstock-dark.svg"><img src="assets/smartstock-light.svg" width="49%" alt="SmartStock — inventory and order management"></picture></a>
<a href="https://github.com/dev-the-dev-while-deving/cut-studio"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/cut-dark.svg"><img src="assets/cut-light.svg" width="49%" alt="CUT — neon-brutalist site with a WebGL scene"></picture></a>
<a href="https://github.com/dev-the-dev-while-deving/MiniNet"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/mininet-dark.svg"><img src="assets/mininet-light.svg" width="49%" alt="Fortress-Net (MiniNet) — a self-healing secure network built in Mininet"></picture></a>

## Writing

- [**Breaking AI agents on purpose**](writing/breaking-agents-on-purpose.md): why breakbench keeps every failure as a replayable record, and why it scores tool calls instead of words.
- [**A coding agent that proves its work**](writing/a-coding-agent-that-proves-its-work.md): nextharness, and why "tests pass" was wrong 7 times out of 12 on my hard tasks.

## Commits

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/skyline-dark.svg">
  <img src="assets/skyline-light.svg" width="100%" alt="My contributions as a 3D isometric skyline, one block per day. Updated nightly.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/shiplog-dark.svg">
  <img src="assets/shiplog-light.svg" width="100%" alt="Animated git graph: commits on main, a feature branch, and a merge">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com?user=dev-the-dev-while-deving&hide_border=true&border_radius=48&background=282B24&ring=9CD67D&fire=9CD67D&currStreakNum=E2E4D9&sideNums=E2E4D9&currStreakLabel=9CD67D&sideLabels=C3C8BB&dates=C3C8BB&stroke=C3C8BB">
  <img src="https://streak-stats.demolab.com?user=dev-the-dev-while-deving&hide_border=true&border_radius=48&background=EDF0E4&ring=386A20&fire=386A20&currStreakNum=1A1C16&sideNums=1A1C16&currStreakLabel=386A20&sideLabels=43483E&dates=43483E&stroke=43483E" width="100%" alt="GitHub commit streak">
</picture>

## Languages

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/languages-dark.svg">
  <img src="assets/languages-light.svg" width="100%" alt="Languages: Rust, TypeScript, Python, Kotlin, C">
</picture>

## Stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <img src="assets/stack-light.svg" width="100%" alt="Stack: Rust, TypeScript, Python, Kotlin, C, React, Next.js, Vite, Flask, PyTorch, scikit-learn, SQLite, MySQL, Supabase, Arduino, Git. Into: AI agents, ML for control systems, edge and IoT, local-first software.">
</picture>

## Contact

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/contact-dark.svg">
  <img src="assets/contact-light.svg" width="100%" alt="Got an irritation? Let's build the fix.">
</picture>

[GitHub](https://github.com/dev-the-dev-while-deving)
