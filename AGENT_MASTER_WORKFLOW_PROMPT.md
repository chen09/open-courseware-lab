# Master Lesson Workflow Prompt (Copy/Paste)

Use this file as a human-facing guide and wrapper reference.

## Role Split (Human vs AI)
- Primary runtime prompt for AI execution: `docs/KICKOFF_AGENT_PROMPT.md`
- Human-facing architecture and onboarding doc: `AGENT_MASTER_WORKFLOW_PROMPT.md` (this file)
- Stage-level executable details: `.cursor/skills/lesson-stage-*/SKILL.md`

## Runtime Policy
- Do not treat this file as the primary runtime prompt in normal lesson production.
- For new problems, start from `docs/KICKOFF_AGENT_PROMPT.md` only.
- Keep this file focused on explanation, onboarding context, and compatibility.

> Note: `docs/KICKOFF_AGENT_PROMPT.md` is the active orchestration source.
> Keep this file as a reusable wrapper template, and put detailed process updates into:
> - `docs/KICKOFF_AGENT_PROMPT.md`
> - `.cursor/skills/lesson-stage-*/SKILL.md`
> - `docs/workflow-modular-architecture.md`

## Legacy Wrapper Prompt (Compatibility Appendix)
The following large prompt block is kept for compatibility with old workflows.
When in doubt, prefer `docs/KICKOFF_AGENT_PROMPT.md`.

```markdown
If asked in English: Execute an end-to-end production workflow for one interactive multilingual lesson, including problem extraction, multi-method solving, web research, multi-model cross-verification, implementation, QA, git PR flow, and production deployment.

请接手并直接执行，不要只给方案。  
你是本项目的执行代理，需要完成从“题目输入”到“上线发布”的全流程。

---

## 0) 任务目标（必须达成）

把我提供的一道题（图片或文字）做成可分享的互动课件，并完成上线。

**必须包含：**
- 题目抽取与纠错
- 多种解法（至少 2 种）
- 多模型交叉验证（尽可能 2~3 个独立模型/渠道）
- 中/日/英三语讲解
- 可交互网页（图文 + 动画/可视化，能课堂展示）
- 更新目录首页（自动卡片体系）
- Git 分支 -> PR -> 合并 main -> Cloudflare Pages 发布

---

## 1) 输入材料（我会提供其一或多项）

- 题目图片：`[PATH_OR_URL]`
- 题目文字：`[PASTE_TEXT]`
- 参考答案（可选）：`[PASTE_ANSWER]`
- 学段（可选）：`[elementary/middle/high]`
- 学科（可选）：`[math/physics/chemistry]`
- 期望语言重点（可选）：`[zh/ja/en]`
- 视觉偏好（可选）：`[简洁/卡通/黑板风/考试风]`

---

## 2) 强制执行规范（不可省略）

1. **先做再汇报**，每个阶段给我可复制命令  
2. **中文沟通**，代码/注释默认英文  
3. **风险先预警**（路径、资源、版权、部署、移动端）  
4. **禁止本地绝对路径资源**（必须相对路径）  
5. **发布前必须通过 QA 清单**（见第 10 节）  
6. **必须保留可追溯证据**：  
   - 解题过程  
   - 交叉验证记录  
   - PR 链接  
   - 发布链接

---

## 3) 项目结构规范（必须遵守）

新题一律放在：

`lessons/<subject>/<grade>/<topic>/<problem-slug>/`

目录至少包含：
- `index.html`
- `meta.json`
- `assets/...`（题图、示意图、动图等）

根目录自动目录页依赖：
- `lessons/manifest.json`

新增/更新题目后必须执行：
- `node ./scripts/generate-lessons-manifest.mjs`

---

## 4) 解题执行要求（教学与严谨并重）

你必须输出并在网页中体现：

1. **题目抽取版**
   - 原题
   - 已知条件
   - 求解目标
   - 变量定义与单位

2. **解法 A（学生友好分步）**
   - 每步一句话 + 一个公式/算式
   - 对每步给“为什么这样做”

3. **解法 B（方程/严谨版）**
   - 完整建模
   - 关键等式推导
   - 结论回代验证

4. **（若可行）解法 C（替代思路）**
   - 比如图像法、比例法、反推法、极值法等

5. **一致性校验**
   - 三种解法结果一致
   - 单位一致
   - 边界合理
   - 与参考答案比对（若有）

---

## 5) 多模型交叉验证（尽量执行到位）

目标：降低单模型幻觉风险。

请尝试使用**多个独立解题来源**（可包括）：
- 模型来源 A（主模型）
- 模型来源 B（次模型）
- 模型来源 C（可选）
- 外部高质量资料（教材/题库/讲解站点）

输出一张“验证矩阵”：
- 来源
- 关键方程
- 最终答案
- 差异点
- 你最终采信理由

若工具权限限制导致无法调用多个模型，必须明确：
- 哪些来源可用
- 哪些不可用
- 你如何补偿验证（如增加独立推导 + 网络资料交叉）

---

## 6) 网络检索要求（必须做）

你必须检索并引用以下内容：
1. 同类型题目或知识点讲解（至少 2 条）
2. 该知识点常见误区（至少 1 条）
3. 可用于课堂口头解释的简洁类比（至少 1 条）

输出时附链接，并说明它们如何影响你的讲解设计。

---

## 7) 网页课件要求（必须实现）

页面至少包含三大 Tab：
- 原题
- 解法
- 动画/可视化

并具备：
- 老师模式（逐步显示）
- 语言切换（zh/ja/en）
- 自动语言轮播（可开关）
- 移动端适配（390px + 320px）
- 关键步骤高亮（避免信息淹没）

可视化建议（按题型）：
- 运动类：时间轴 + 位置变化动画
- 几何类：图形构造/辅助线逐步出现
- 代数类：式子变形动画
- 化学/物理：状态变化或流程图动画

如果能做动图/视频，优先：
- 在 `assets/` 放置可发布文件
- 页面提供播放与说明

---

## 8) `meta.json` 规范（必须更新）

至少包含：
- `id`
- `title`（ja/zh/en）
- `subject`
- `gradeBand`
- `topic`
- `slug`
- `entry`
- `assets`
- `features`

---

## 9) 实施与发布流程（必须完整走完）

按顺序执行：
1. 创建题目目录与资源
2. 实现/更新 lesson `index.html`
3. 更新 `meta.json`
4. 运行 manifest 生成脚本
5. 本地启动并验证
6. 新建分支
7. 提交 commit
8. 推送并创建 PR
9. 合并到 `main`
10. Cloudflare Pages 部署生产

---

## 10) 发布前 QA 清单（全部通过才可发版）

### 功能
- [ ] Tab 切换正常
- [ ] 老师模式逐步显示正常
- [ ] 三语切换正常
- [ ] 自动轮播正常
- [ ] 动画/可视化控制正常

### 内容
- [ ] 题干与条件无遗漏
- [ ] 至少两种解法且答案一致
- [ ] 三语术语一致、表达自然
- [ ] 课堂提示可直接使用

### 兼容
- [ ] 390px 可用
- [ ] 320px 可用
- [ ] 无阻塞性横向溢出
- [ ] 主要按钮可点击

### 发布
- [ ] PR 已创建并可访问
- [ ] 已合并 main
- [ ] 生产链接可访问
- [ ] 根目录首页能显示该题卡片并可跳转

---

## 11) 最终输出格式（必须按此结构回复）

1. **执行摘要（3-6条）**
2. **题目抽取结果**
3. **解法 A/B(/C) + 一致性结论**
4. **多模型与外部资料验证矩阵**
5. **本次修改文件列表**
6. **关键命令（可复制）**
7. **PR 链接**
8. **生产链接**
9. **风险与后续建议**

---

## 12) 本次题目信息（由我填写）

- 题目主题：`[填写]`
- 输入材料：`[填写文本/图片路径/链接]`
- 是否有参考答案：`[有/无]`
- 目标学段：`[填写]`
- 目标学科：`[填写]`
- 截止时间：`[填写，可选]`

请现在开始执行，不要停在计划阶段。
```
