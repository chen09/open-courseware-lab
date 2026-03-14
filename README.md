# open-courseware-lab

Open-source interactive K-12 courseware for math, physics, chemistry, and future subjects, with multilingual support and web-first delivery.

## Overview

This repository hosts interactive lesson pages designed for family and classroom learning.

Each lesson can include:

- clear problem statement
- step-by-step solution
- animated visualization
- multilingual text support

## Content structure

Lessons are organized as:

- `lessons/<subject>/<grade>/<topic>/<problem-slug>/`

Current subject taxonomy:

- `math`
- `physics` (planned)
- `chemistry` (planned)

## Current lesson

- `lessons/math/elementary/speed-distance/jiro-taro-catchup-rest/`
  - `index.html` (lesson entry)
  - `assets/problem-001.png` (problem image)
  - `meta.json` (classification metadata)
  - Problem / Solution / Animation tabs
  - Teacher mode (step-by-step reveal)
  - Language switch + auto language rotation

## Why this project

- Build reusable lesson templates across subjects
- Support more languages over time
- Share lessons easily via URL (LINE / WeChat / browser)

## Quick start

Run a local static server from repository root:

```bash
python3 -m http.server 8080
