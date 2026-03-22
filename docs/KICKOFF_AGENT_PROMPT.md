# KICKOFF Agent Prompt (Open Courseware Lab)

说明：这是给 AI 执行的唯一主入口（runtime source of truth）。
给人阅读的说明文档在：`AGENT_MASTER_WORKFLOW_PROMPT.md`。

用法（每次新会话，推荐一步）：
1. 一条消息内同时发送：
   - 下方 kickoff 代码块（完整）；
   - 本次题目输入（必填：题目图片或题目 text）；
   - 可选解答输入（可选：解答图片或解答 text）。
2. 如平台限制附件/长文本，也可退化为两步发送（先 kickoff，再任务输入）。

一步消息模板（可直接复制）：

```markdown
<KICKOFF_BLOCK>
（把下方完整 kickoff 代码块粘贴在这里）
</KICKOFF_BLOCK>

<INPUT>
problem:
- type: image | text
- content: <题目图片或题目文本>

solution: (optional)
- type: image | text
- content: <解答图片或解答文本，可空>
</INPUT>

任务目标：
- 从输入自动完成：求解 -> 校验 -> 页面/动画(必要时3Blue1Brown风格视频) -> 本地审查 -> GitHub + Cloudflare 发布
```

```markdown
You are working in `open-courseware-lab`.

## Operating Mode
- Correctness first for children-facing content.
- Execute end-to-end unless blocked: implement -> validate -> report.
- Be proactive in running checks; do not push command burden to user.

## Modular Execution (single source of truth)
- Treat this file as the orchestration entry, and execute by stages:
  1) `lesson-stage-01-intake`
  2) `lesson-stage-02-solve-model`
  3) `lesson-stage-03-build-lesson`
  4) `lesson-stage-04-validate`
  5) `lesson-stage-05-release`
  6) `lesson-stage-06-retro-governance`
- Do not redefine the same rules in multiple prompt files; update stage skills/rules instead.
- After stage 04, run workflow contract audit:
  - `node ./scripts/qa-workflow-audit.mjs`
- Keep audit output as release evidence:
  - `reports/workflow-audit/latest.json`
- Every 10-15 lessons, run cycle review with:
  - `docs/workflow-cycle-review-template.md`

## End-to-End Auto Pipeline (default)
- Treat the following as the default fully automated flow unless user explicitly pauses:
  1) Ingest input (problem image / problem+solution image / plain text).
  2) Solve and cross-check; if useful, search web for similar problem patterns/solutions as reference (do not copy blindly).
  3) Build solution page (kid-friendly wording + LaTeX rendering).
  4) Build interactive animation that matches the solved model.
  5) If necessary (especially geometry/visual intuition bottlenecks), produce a 3Blue1Brown-style explainer video with narration.
  6) Run local release preview.
  7) Use browser-devtools tools to review local output; do frame-by-frame checks for animation/video and use LLM-assisted evidence-based review.
  8) If all checks PASS, publish to GitHub and Cloudflare Pages, then verify production URL.

## Web Reference Policy (for step 2/5)
- Prefer finding 2-3 high-quality external references when problem type is non-trivial.
- Use references for validation and explanation quality, not for unverified copy/paste.
- If references disagree, mark as conflict and block release until resolved.

## Hard Rules
- Python must run only in project `./.venv` (no host pollution, no extra envs).
- Prefer LaTeX rendering for formulas (KaTeX/MathJax for web, MathTex for Manim).
- Keep lesson consistency across `index.html`, `meta.json`, `lessons/manifest.json`, and assets.
- For Manim/video updates, keep VTT semantics/timing aligned with visuals.
- TTS stack in this project (current practice):
  - model/inference: `f5-tts` (`f5-tts_infer-cli`) in `./.venv`,
  - voice cloning mode: reference-audio conditioned generation (`--ref_audio` + explicit `--ref_text`),
  - audio/video post-process: `ffmpeg` + `ffprobe` (tempo fit, mux, stream checks).
- For TTS generation, always provide explicit `ref_text`; do not rely on auto-ASR for reference transcript.
- Prefer concise narration text over aggressive audio time-compression when speech sounds dense.
- Do not overwrite original problem images; create processed copies only.
- For geometry animations, coordinates must satisfy problem constraints numerically (e.g., collinearity/on-segment/ratio).
- Never declare "PASS" from visual impression alone; use measurable checks (DOM/computed style/numeric assertions).

## 3Blue1Brown-style Video Gate (only when needed)
- Trigger this mode when:
  - core learning objective depends on continuous geometric/algebraic transformation, or
  - static/web animation cannot provide sufficient intuition clarity.
- Requirements in this mode:
  - derive scene math first, then storyboard, then render;
  - narration must align with exact math states shown on screen;
  - frame-level sanity checks are mandatory at key timestamps;
  - if quality/confidence is insufficient, block release and fall back to clearer web-first explanation.

## Validation Gate
- Run:
  - `python scripts/validate-manim-lesson.py <lesson-dir>`
- If animation is edited, also run:
  - `python scripts/extract-animation-checkframes.py <lesson-dir> --profile assets/explain/qc-checkpoints.json`
- If image orientation/cropping is edited:
  - verify processed image orientation against source before release (no upside-down/mirroring).
- If scene logic/highlights are edited:
  - verify scene-to-highlight mapping via computed style/state sampling (not just screenshots).
- If geometry diagram is edited:
  - verify key constraints with numeric checks (example: `E on BD`, `F on BC`, `A-E-F collinear`, target ratio).
- If TTS/audio is edited:
  - verify final video duration matches target scene duration,
  - verify audio stream exists and decodes (codec/sample_rate/channels),
  - check for lexical leakage from reference text (unexpected words unrelated to lesson content).
- If any verification signals conflict, stop release and fix first; do not "ship and see".
- Report key outputs and blockers clearly.

## Browser Review Gate (must run before release)
- Open local preview in browser-devtools tooling and review:
  - solution tab correctness (numbers, units, final answer),
  - animation behavior across start/mid/end and scenario switches,
  - video keyframes for 3Blue1Brown-style output (if present).
- Capture screenshots for key checkpoints and keep them as review evidence.
- For frame-heavy review, use incremental seeks and LLM-assisted inspection; no release without evidence-backed PASS.

## Local Preview Gate (must pass before asking user to open)
- After generation/edit, automatically start local preview from repo root.
- Preferred port is `8080`; if occupied, automatically probe and switch to next available port (e.g., `8081`, `8082`, ...).
- Before sharing URL, self-check:
  - target file exists on disk,
  - server process cwd is repo root,
  - `curl` to lesson URL returns HTTP 200.
- Never ask user to open an URL before these checks pass.

## Accuracy Review Gate (input -> output strict audit)
- Always review output against input problem and provided solution.
- For math word problems, verify with at least two independent methods when feasible (e.g., relative speed + equation).
- Numeric/unit checks are mandatory (`km/h <-> m/s`, seconds/minutes/hours consistency).
- Animation semantics must match the solved model (timing, direction, labels, scenario transitions).
- If any mismatch or uncertainty exists, treat as release blocker and fix first.

## Release Discipline
- Commit only approved files.
- Avoid committing temporary artifacts (tts intermediate wav/txt/mp4, caches).
- For voiceover work, keep candidate outputs as `scene-01.tts-*.mp4`; only promote to `scene-01.mp4` after explicit user approval.
- For Cloudflare local deploy, use a clean staging directory to avoid `.cache`/large blobs.
- After deploy, re-check production URL (with cache-busting query when needed) before reporting completion.
- After audit passes, complete release flow unless user explicitly pauses:
  - push to GitHub (branch/PR or direct flow per repo convention),
  - publish to Cloudflare Pages production,
  - verify production URL and report final URL with checks performed.

## Response Style
- Reply in Chinese.
- Keep output concise and actionable.
- If unclear requirements, ask targeted clarification before risky changes.
- Do not ask optional preference questions like "whether to add unit hints / teacher script"; decide and execute by default.
- Default teaching enhancements for math word problems:
  - include a teacher-only unit-conversion hint block when units may confuse learners,
  - include a classroom-ready short voiceover script draft in teacher mode notes (even if no TTS render is requested yet).
- Run autonomous review before release and report evidence:
  - numeric assertions (unit/value checks),
  - browser checkpoint review (start/mid/end),
  - consistency check across problem/solution/animation/manifest.
```

## Task Template (paste after kickoff)

```markdown
任务目标：
- <要做什么>

作用范围（文件/目录）：
- <path1>
- <path2>

验收标准：
- <标准1>
- <标准2>

约束：
- <例如：仅用 .venv，不改核心配置，不删文件>
```

## Pre-release Checklist Template (checkbox)

```markdown
发布前清单（Pre-release Checklist）：

- [ ] 输入题目与解答已对齐（题意、已知条件、目标量一致）
- [ ] 至少两种独立方法复核答案（如：相对速度法 / 方程法）
- [ ] 单位换算与数值核对通过（km/h、m/s、秒、分钟）
- [ ] 课程文件一致性通过（`index.html` / `meta.json` / `lessons/manifest.json` / assets）
- [ ] 公式渲染正确（KaTeX/MathJax/MathTex，无纯文本公式残留）
- [ ] 动画语义正确（方向、时序、标注、关键帧与解法一致）
- [ ] 已按需完成 web 参考核验（至少 2 个参考来源；冲突已消解）
- [ ] 如启用 3Blue1Brown 风格视频：关键帧逐帧审查通过（画面/旁白/数学状态一致）
- [ ] 本地预览已自动启动（端口冲突已自动回退）
- [ ] 本地 URL 自检通过（文件存在 + HTTP 200）
- [ ] 审核截图/证据已留存（关键帧、关键计算步骤）
- [ ] 无临时产物被纳入发布（缓存、中间文件、测试垃圾）
- [ ] GitHub 发布步骤完成（按仓库规范：分支/PR/合并）
- [ ] Cloudflare Pages 发布完成并回归检查（含 cache-busting）
- [ ] 最终线上 URL 可访问且内容与本地一致

发布结果：
- 生产 URL: <https://...>
- 核查结论: <PASS / BLOCKED>
- 阻塞项（如有）: <...>
```

## Auto-block on Failure (Release Stop Rule)

```markdown
失败自动阻断发版规则（Auto-block on Failure）：

- 触发条件（任一命中即 BLOCKED）：
  - 任一数学结论无法被复核通过，或出现单位/数值不一致；
  - 输入题目、解答、页面展示三者存在矛盾；
  - 本地预览自检失败（文件不存在、服务异常、URL 非 200）；
  - 动画语义与解法不一致（方向/时序/关键标注错误）；
  - 校验脚本报错或关键检查缺失；
  - Cloudflare 生产回归失败（线上不可访问或内容不一致）。

- 阻断动作（必须执行）：
  - 立即停止发布链路（不推送、不合并、不部署）；
  - 将核查结论标记为 `BLOCKED`；
  - 输出最小可复现证据（命令结果、截图、关键日志）；
  - 列出修复项与下一步，不得以“先上线再看”替代修复。

- 恢复条件（全部满足才可继续发布）：
  - 所有阻塞项关闭；
  - 完整重跑发布前清单并全绿；
  - 重新给出 `PASS` 结论与最终生产 URL。
```

