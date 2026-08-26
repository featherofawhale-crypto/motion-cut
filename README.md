# motion-cut

把分镜脚本（PDF / Keynote / 分镜表）做成**可视化 motionboard 视频时间线**的 Codex/Claude skill ——
让剪辑师不用对着 PDF 想象画面，直接在 DaVinci Resolve 或 Premiere Pro 里"看脚本"。

蒸馏自吉利银河 TT TVC 真实工程（70+ 时间线，aco→bco 多版本演进），并在 DaVinci Resolve 19
与 Premiere Pro 2024 上全流程实测。

## 它做什么

输入一份分镜脚本，产出一条能播放的大纲时间线：

- **按 cut 顺序铺画面**：有素材放素材（视频/图片），缺素材放脚本官方示意图，再没有放占位图——结构永远完整
- **台词有声音**：TTS 生成 VO 上轨，画面长度跟着台词走（话说完才切镜：图片延长、视频末帧定格补长）
- **信息标清楚**：每个 cut 打 marker 写脚本原文；有卖点的 cut 压 super；台词上字幕轨；场首放备注
- **备选不丢**：一镜多条的备选叠在同位置上层轨并禁用，主选永远在第一轨
- **素材分类**：按 主素材/备选/VO/动效/SFX 分箱管理

## 安装

```bash
# Codex
cp -R motion-cut ~/.codex/skills/

# Claude Code
cp -R motion-cut ~/.claude/skills/
```

然后直接说：「把这份分镜脚本做成 motionboard」。

## 目录

```
motion-cut/
├── SKILL.md            # 方法论 + 全套工程避坑指南（DaVinci/PR 双宿主实测）
├── test-prompts.json   # 触发/不触发测试用例
└── scripts/
    ├── resolve_run.sh      # DaVinci 脚本安全启动器（防 SIGSEGV 三连崩）
    ├── pr_mcp_client.py    # Premiere MCP stdio 驱动（配 adobe-premiere-pro-mcp 用）
    ├── pr_jsx_eval.mjs     # 经 CEP 面板 CDP 端口在 PR 里跑任意 ExtendScript
    └── pr_ui_text.py       # PR 原生可编辑文字的 UI 自动化创建（官方接口写不了文字）
```

## PR 侧依赖

- [adobe-premiere-pro-mcp](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP)（npm 安装，CEP 桥面板）
- CEP 面板开远程调试：extension 目录放 `.debug`（PPRO 端口 8877）后重启 PR
- macOS（osascript / Quartz 事件做 UI 自动化）

环境变量：`PR_MCP_SERVER`（MCP server 路径）、`PR_CDP_PORT`（默认 8877）、
`PR_SEQ_ID`（pr_ui_text.py 的目标序列）、`PR_MCP_PYTHON`（带 mcp 库的 python）、`PR_TOOLS_DIR`。

## DaVinci 侧依赖

- DaVinci Resolve 19（Studio 版脚本 API 最完整）
- 项目内字体：阿里巴巴普惠体 Medium（super/字幕规范）

## 血泪教训（都写在 SKILL.md 里）

- DaVinci：绝不硬杀连着 Resolve 的脚本进程；SRT 上轨前播放头归零；分镜表必须按 PDF 渲染页核对
- PR：`import_media` 的 binName 失效要用 JSX moveBin 兜底；ExtendScript 写「源文本」会把文字层
  渲染崩，原生文字只能 UI 自动化建；调文字大小/位置用文本组件，别用剪辑级运动缩放

## License

MIT
