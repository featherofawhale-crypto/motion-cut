---
name: motion-cut
description: >-
  把分镜脚本（PDF / Keynote / 分镜表）做成可视化 motionboard 视频时间线，
  供剪辑师直接"看脚本"——蒸馏自真实汽车 TVC DaVinci 工程（已脱敏）。
  必须有分镜脚本输入；没有脚本不要触发。
  Use when the user asks to 把分镜脚本/shooting board 做成可视大纲视频、motionboard、
  animatic、给剪辑师看的动态脚本，或在 DaVinci/PR 里按分镜表搭带 VO/字幕/super 的
  大纲时间线。NOT for 无脚本的自由剪辑 / 慢叙事 / 纯调色 / 单镜头生成提示词。
license: MIT
metadata:
  source: 真实汽车 TVC 剪辑工程（已脱敏, DaVinci Resolve project）
  distilled-by: cangjie-skill v1 (lightweight)
  version: 0.5.2
---

# Motion Cut — 分镜脚本 → 可视化 motionboard

核心用途：给一份分镜脚本（PDF/Key/分镜表），产出一條能播放的大纲时间线
（DaVinci 或 PR），画面按 cut 顺序走、台词有 VO、卖点压 super、备选叠轨藏好、
每个镜头可回溯脚本原文——剪辑师拿到就能对着剪。

以下为支撑这条流水线的剪辑方法论与工程避坑，每条都带证据出处，
可在 `candidates/timelines_dump.json` 中复核。

## 字幕规范（央视，全宿主强约束）

无论 DaVinci 还是 PR，同期声/VO 字幕一律遵守，不许破例：

1. **每行 ≤14 个汉字**，长台词必须断行
2. **无标点**：逗号句号问号全去掉，语气停顿用空格代替
3. **无称谓/角色前缀**：不写「某某：」，角色区分靠音色与画面
4. **cue 起止 = 对应 VO 音频条在时间线上的实际起止**（摆完 VO 回读位置再写 SRT，
   禁止凭估算值写字幕时间）
5. 台词只用脚本原文，不自行改写；台词表先行（cut/角色/台词/语气/音色ID 五列）

## R — 原文证据（时间线数据）

> `bco-v7` V1 轨 91 镜：时长分布 <0.5s×14 / 0.5–1s×26 / 1–1.5s×19 /
> 1.5–2s×9 / 2–3s×14 / 3–4s×4 / >4s×2，中位 1.16s。

> `素材` 时间线 6 个 marker：CUT 1「城市路边…编曲」CUT 2「手机弹出
> 好友语音…」CUT 3「车辆穿行城市弯道…」CUT 4「功能卖点露出…」
> CUT 5「沿江…指尖敲击方向盘」CUT 6「平稳停在livehouse门口」。

> audio3–8：`436_stem1–6_shine-for-me` 六条音乐 stem 按场错落进出；
> audio10–18：九条音效轨分 whoosh / 脚步动作 / 车身 / 氛围 / rise 五族。

## I — 方法论骨架

**六步，严格按顺序：**

1. **选片编号**：建一条素材时间线集中所有可用素材；选中段标记后，进粗剪的镜头
   一律改名 `<轨号>-<四位序号>_源文件名`（如 `V1-0047_DJI_...D_B002.mov`）。
   序号单调递增 = 剪辑决策顺序，源文件名保留 = 随时回溯原始机位。
2. **分场 marker 先行**：在素材时间线上按剧本打 `CUT n` marker，每个 marker 的
   note 写一整句场描述（谁、在哪、做什么、产品功能露出点）。先结构后镜头。
3. **主轨节奏曲线**：V1 只放叙事主镜头。目标分配（以 2 分钟成片为参照）：
   中位镜头 1.0–1.3s；开场 2 镜放宽到 2–4s 建立空间；中段动作/功能段压到
   0.5–1s 连切；情绪点与收尾 logo hold 放到 3–6s。30s 产品 motion 短片用
   0.9s 起步、递增到 6s 收尾的收敛曲线。
4. **音乐用 stem 分层**：要求/自制鼓、贝斯、和声、旋律、FX、vocal 分轨，
   每条 stem 一条音频轨，按场开关与错落进出制造段落感；不要把一整首混好的
   BGM 从头铺到尾。
5. **音效五族织体**：为 whoosh转场 / 脚步动作 / 产品本体（车身、机械） /
   环境氛围 / rise·impact 各占独立轨（量级：9+ 条音效轨）。每个硬切/转场
   至少有一个 whoosh 或 impact 点火；动作镜（走路、放置）必须贴同步音效。
6. **对照轨版本管理**：改版本时把上一版成片整轨垫在最上层视频轨（关闭显示
   备用），A/B 对比靠开关轨道而不是靠记忆。不同画幅版本（如 4:3）同样垫轨对照。

## A1 — 工程中已验证的实例

- 粗剪时间线 `粗剪_v1` → `bco-v7`：63 条时间线
  的演进全部遵守编号选片约定，任一镜头可凭 `V1-XXXX_源文件名` 回溯。
- 产品展示段 `产品motion`（31.7s）：镜头时长 2.16→1.60→…→
  3.80→6.24s，末镜 logo hold 最长，符合收敛曲线。
- `bco-v7` v9 轨垫 `bco-v6.mp4` 整段做对照；
  v5 轨垫 `bco-v6 4比3.mov` 做画幅参照。

## A2 — 何时触发

用户拿来一批素材（尤其车、3C、快消产品）要剪 30s–2min 的快节奏广告/TVC，
或问"怎么整理选片""节奏怎么卡""音效怎么铺""音乐怎么切"。

与相邻 skill 的区分：本 skill 管**剪辑结构与节奏**；画面内容生成提示词归
seedance-prompt-zh / aigc-tvc-director；成片字幕归 embedded-captions；
纯技术操作 DaVinci API 归 davinci-resolve。

## E — 执行步骤

1. 建 `素材` 时间线导入全部素材 → 按剧本打 CUT marker（note 写场描述）→
   拉出选中段并按规则 1 改名。
2. 建新时间线，V1 按规则 3 铺主镜头，先不管音乐，用硬切定节奏。
3. 音乐 stem 各占一轨，按场进出；VO 独占 audio1。
4. 按五族开音效轨，逐剪点贴 whoosh/同步音效，尾部 rise + impact。
5. 改版前把当前版导出成片垫到顶层轨（关闭显示），再动手改。

## B — 边界

- 慢叙事、情绪长片、纪录片不适用；此语法为高密度产品露出服务。
- 素材量小于 ~20 镜时编号选片是过度工程，直接剪。
- 多画幅交付（4:3 / 9:16）需单独垫轨参照，不要在主轨上改构图。
- 轨道分族依赖纪律，团队协作时把轨道命名规范写进工程模板，不要口头约定。

## v0.2 新增：大纲时间线自动化搭建（outline 实测）

### 分镜与素材
- **严格按脚本 cut 编号顺序铺片**，禁止按画面内容自行归场；缺素材的 cut 用占位图
  （深灰底+居中标明"cut N 待补素材"），保持结构完整
- **纯文字分镜（脚本只有描述、连官方示意图都没有）按内容三选一做示意**，禁止只放静态占位图：
  1. **实拍内容**（人骑马、开车、脸部特写等真实世界镜头）→ 用**高精度图形表示**
     （imagegen 生成写实级示意图，按脚本描述写清主体/景别/光线，角标注明"示意"）
  2. **CG 镜头** → 用 **Remotion / 3D 预演做动态示意**（见下条，不只限纯文字分镜）
  3. **其他** → Remotion / HyperFrames 动态示意，配方从 video-shotcraft 镜头库选：
     https://vincentwei1021.github.io/video-shotcraft/library.html
     （152 个镜头配方卡 / 209 种风格，含 开场品牌/排版/UI/运镜/转场/节奏/收尾 等分类，
     agent 按该 cut 的脚本描述挑最贴近的实现）
- **CG / 三维 / 文字包装类镜头（任何 cut 都适用，不只纯文字分镜）**：
  - 涉及三维内容 → 用 **3D 预演**（Three.js / Spline 等）搭示意
  - 有参考视频/画面 → 按参考用 Remotion 做镜头运动/图形演绎
  - **没有参考、只有文字描述也能做**——按描述自行设计镜头与图形
  - 文字包装（slogan 排版、标题演绎、信息卡片）→ Remotion/HyperFrames 直接做
  - 输出：透明通道叠加（prores 4444）或整帧示意，角标注明"示意"
- 同分镜多文件：最重要的主选 V1 显示；备选**全部叠在同分镜位置的上层轨**（V2、V3…）并 SetClipEnabled(False) 隐藏，禁止挪到尾部备选池（v0.3 修正：备选池会让人以为素材丢了）
- 图片分镜与视频分镜用不同 clip 颜色（视频 Green / 图片 Sky / 占位 Sand）
- 防黑边：非 16:9 素材 SetProperty ZoomX/ZoomY = max(tl/src)/min(tl/src)；源片自带黑边再加大

### Text+ 字幕规范
- super：V3 轨、左下角、阿里巴巴普惠体 Medium、clip 颜色 Orange
- 备注：V4 轨、画面居中、小字半透明(Blend 0.5)、clip 颜色 Lavender
- 同期声/VO 走字幕轨道：SRT 导入素材池后 AppendToTimeline(recordFrame=0)
- 字幕遵守「字幕规范（央视）」章节五条强约束

### DaVinci API 避坑（实测）
- `InsertFusionTitleIntoTimeline` 是连锁插入（ripple），会推动其后**所有未锁轨道**（含时间线 marker）
  → 插标题前锁全部轨，**marker 永远最后打**
- 标题插入目标轨 = 当时最上方有内容的视频轨 → 先在目标轨放 dummy 片段"定轨"，插完删 dummy
- 音频 `recordFrame` 摆放若落在长音频内部会静默失败 → 先用 startFrame/endFrame 限长
- TTS/AI 生成的单声道音频进达芬奇前统一 `ffmpeg -af pan=stereo|c0=c0|c1=c0`
- ImportMedia 返回顺序不可靠 → 按 GetName() 建映射再使用

### 音频生产
- VO/同期声只用脚本原文台词，台词表先行（cut/角色/台词/语气/音色ID 五列）
- 角色-音色一一对应，车载语音助手类角色全片唯一音色；豆包 TTS 2.0 HTTP API：
  POST https://openspeech.bytedance.com/api/v3/tts/unidirectional
  Header `X-Api-Key` + `X-Api-Resource-Id: seed-tts-2.0`，语气用 `context_texts` 传
- 音效五族分轨不变；优先复用项目 SFX 库

### 动效（Remotion）
- 浮现类元素（语音助手条/弹窗/UI浮层）用 Remotion 做 3840x2160 透明通道：
  `npx remotion render src/index.ts <Comp> out.mov --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png`
- 动效放独立视频轨（V1 之上、SUPER 之下），clip 颜色 Fuchsia
- 参考库: video-shotcraft —— https://vincentwei1021.github.io/video-shotcraft/library.html
  （github vincentwei1021/video-shotcraft）；纯文字分镜的动态示意也从这里选配方

## v0.3 新增：VO 时长对齐 + 稳定性工程（0825 outline 实测）

### VO 说完才切镜（台词优先原则）
- 分镜时长 = max(素材时长, 该 cut 台词组总时长 + 行间隔 0.5s)；先算 VO 需求再排 pos 累加
- 图片分镜：直接延长到 VO 说完
- 视频分镜：末帧定格补长。ffmpeg 抽末帧（`-ss <dur-0.08> -frames:v 1`），
  **再转成定长 mp4 上轨**（`-loop 1 -t <秒> -r 25`）。
  坑：`standardStillDuration` 项目设置对 AppendToTimeline 的 still 不生效，png 上轨永远是默认 5s
- 定格帧与同分镜视频用同一 clip 颜色，视觉上是"一个镜头"

### 字幕上轨两条路
- SRT 路径（推荐，文本精确）：cue 起止=VO 音频条实际起止回写；
  **上轨前必须播放头归零**（SetCurrentTimecode('00:00:00:00')），否则 cue 整体偏移到片尾
- 自动识别路径（CreateSubtitlesFromAudio）：**先把音效轨撤空再识别**（音效会被识成 [MUSIC]/垃圾 cue），
  GUI 对话框语言选"中文普通话-简体"，识完再把音效摆回去；API 调用不认 transcriptionLanguage 设置（19.1.4 实测）

### 分镜表提取（血泪，0826 cut11 事件）
- **shooting board 是多栏版式，pdftotext 的文本流会把 cut 归属打乱**（本次把 cut14/15 对调、
  cut11 张冠李戴、漏掉 cut46）→ 分镜表必须以 **PDF 渲染页/逐格截图** 为准核对，
  用 fitz `get_text('words')` 拿 cut 头部坐标 + `get_image_info()` 按栏位归属图片
- 脚本里每个 cut 的官方示意图都在 PDF 里，**有图必须放图**（这是给剪辑师看的 motion 大纲，
  文字占位图等于没放）；提取流水线：PDF 栏位裁剪 → assets/script_frames/cutNN.png

### 达芬奇脚本稳定性（血泪，详见 docs/达芬奇脚本稳定性-runbook.md）
- **绝不硬杀连着 Resolve 的脚本进程**（alarm/kill -9 会让 fusionscript 不干净断开，
  Resolve 在 ScriptSymbol 析构时 SIGSEGV——0826 三连崩全是这个堆栈）
- 长构建分段落盘：每阶段 SaveProject + 日志；脚本必须干净退出
- 不删仍被任何时间线（含备份）引用的媒体池素材
- 脚本一律经 tools/resolve_run.sh 启动（预检进程/模态窗、日志双写、无 alarm）

## v0.4 新增：Premiere Pro 自动化通路（0826 MCP 实测，mcp-test 工程）

同一套剪辑方法论落到 Premiere 时的工程通路，全部实测过：

### 连接（一次性配置）
- MCP server：`node ~/.local/lib/node_modules/adobe-premiere-pro-mcp/dist/index.js`（283 个工具），
  env `PREMIERE_TEMP_DIR=/tmp/premiere-mcp-bridge`；测试驱动用 `scripts/pr_mcp_client.py`
  （`--list-tools` / `<tool> '<json>'`）
- PR 侧的桥是 CEP 面板 MCPBridgeCEP，**面板必须点 Start Bridge 才监听**；免手工方案：
  在面板 bridge-cep.js 的 DOMContentLoaded 里加 `setTimeout(window.startBridge, 500)` 自动启动
- 面板调试：extension 目录放 `.debug`（PPRO 端口 8877）并**重启 Premiere 才生效**，
  之后 `scripts/pr_jsx_eval.mjs '<jsx>'` 可经 CDP 直接跑任意 ExtendScript（面板 HTML 不挂 AX，
  AppleScript/System Events 拿不到窗口，坐标点击也不可靠；Quartz CGEvent 点击可兜底）

### 工具能力与坑
- 建序列 `create_sequence` **必须传 presetPath**（.sqpreset 绝对路径），否则弹原生对话框卡死脚本；
  用户预设一般在 `~/Documents/Adobe/Premiere Pro/24.0/Profile-*/Settings/自定义/`
- `import_media` 的 **binName 参数实测失效**：物料全部落根目录（bin 照建但为空）。
  素材分类须用 JSX 兜底：先建 bin，再 `projectItem.moveBin(bin)`
- JSX 里**边遍历 root.children 边 moveBin 会跳项**（索引失效）：先收集到数组再统一搬
- 重复 import 同一路径会去重（不产生重复项），可安全重跑
- `add_to_timeline`：sequenceId + projectItemId + 0-based trackIndex + 秒为单位的 time，
  返回实际 in/out/duration；`add_marker` / `save_project` / `list_sequence_tracks` 均正常
- list_project_items 的 treePath 不反映 moveBin 之后的位置（可能缓存），核结构用 JSX walk

### 文字与图形（0826 outline 全量重建实测，v0.4.2 修订）
- `create_caption_track` 直接吃 import_media 导入的 SRT，字幕轨一次成型 ✓
- **ExtendScript 写不了文字内容**：`getMGTComponent()` 恒 null；遍历 components 给
  「源文本」setValue 能写进去（读回正确）但**渲染直接崩**（文字层整层消失）。
  MOGRT 模板路径（add_text_overlay）同样死在这条上
- **原生可编辑文字的唯一可靠路径 = UI 自动化**：`pr_ui_text.py`
  （MCP 设播放头+目标轨 → Quartz 点击轨道头聚焦时间线 → `t` 文字工具 →
  点击节目监视器定锚点 → 剪贴板 pbcopy + ⌘V 粘贴中文 → esc 退出编辑态 → `v` 回选择工具）。
  注意：播放头必须先在时间线面板聚焦才同步 UI；粘贴前 esc+v 防上一次编辑态残留造成文字翻倍
- **调文字大小/位置用文本组件**（`AE.ADBE Text` 的「缩放」「位置」，setValue 数值/数组可用），
  **绝不用剪辑级「运动」缩放**——绕锚点缩放会把长文本甩出画面（备注截断事故）
- 版式分区（1920x1080 实测）：super 左下 文本位置 `[0.13,0.82]` 缩放 55；
  备注顶部居中 `[0.33,0.08]` 缩放 40；字幕轨底部居中（PR 默认）。三者互不遮挡
- **super 按卖点 cut 放置**（时长=该 cut 时长），不整场铺满；备注只在场首放 ~5s
- `set_clip_properties`（scale/opacity）在 24.4.1 上失效 → JSX 运动组件兜底；
  位置参数必须用数组 `[x,y]`，字符串报 Illegal Parameter type
- `capture_frame` 的时间参数不可靠（可能导播放头帧），验证以节目监视器截图为准
- 覆盖层/备选上轨一律 `linkAudio:false`（否则素材自带声会砸到 VO 轨）

### 完整重建参考实现
`build_pr.py`（参考实现，见 PR 章节）（47 cut 大纲全量：主轨/备选禁用/VO对齐/定格补长/
SRT字幕/SFX/markers）+ `fix_supers_pr.py`（PNG overlay 方案）+ `pr_classify.jsx`
（素材箱分类）。三件套即 PR 版 build7。

### 与 DaVinci 通路的分工
方法论六条规则（选片编号/分场 marker/节奏曲线/stem 分层/音效五族/对照轨）两软件通用；
工程操作按宿主选 resolve_run.sh（DaVinci）或 pr_mcp_client.py + pr_jsx_eval.mjs（Premiere）。
MCP 工具能做的事走 MCP，MCP 做不了的（如素材归 bin）直接 JSX，不要硬掰 MCP 参数。

## v0.5 新增：前置纪律与交付契约（学自后期启动助手，0827）

以下机制不改变六步方法论，只给大纲搭建加上输入、标注、合规与交付纪律。

### STEP 0 — 输入确认与版本优先级（开工前必做）
- 必须先确认拿到的是**客户最终确认版分镜脚本**。版本优先级：
  最终确认脚本 > 客户最新修改意见 > 最新会议纪要 > 拍摄方案 > 早期策划稿。
  不得用旧版分镜表或未确认稿覆盖最终稿。
- 至少确认：项目名称、成片时长、分辨率/帧率/画幅（含是否多画幅交付）、
  是否需要 VO、是否需要 super/备注字幕、宿主（DaVinci / PR）。
- 输入缺失或版本存疑时**停工询问**，不带着疑问开跑。

### 命名权限边界（不得擅自改名的素材）
- **只允许命名本 skill 自己产出的东西**：脚本参考示意图、占位图、定格补长片段、
  动效叠加层等生成物料，以及时间线上的 clip 显示名（clip 改名不动源文件）。
- **不得改名的**：拍摄素材源文件、音乐文件、音效文件、客户提供的任何素材——
  源文件名一律保持原样（选片编号规则里的 `_源文件名` 后缀就是为此服务）。
- 音乐/音效的 `MUS_…` / `SFX_…` 规范命名**只适用于本 skill 下载归档的副本**，
  归档时在 `02_AUDIO/MUSIC` 里另存命名副本，原始下载文件不原地改名。

### 脚本事实 vs 搭建推断（标注纪律）
- cut 表、场描述 marker note、super、示意图描述中，明确区分两列来源：
  **脚本原文**（逐字引用）与**搭建推断**（agent 的理解/设计）。
  不得把推断写成脚本要求。示意图/占位图角标"示意"本身就是此纪律的一部分，保持。

### 《脚本风险提示》（发现问题不改原文）
- 沿用"台词只用脚本原文"铁律；发现分镜表自身问题（cut 编号错乱、栏位错位、
  图文不符、台词病句、时长明显不够说完 VO）时**不改脚本**，输出《脚本风险提示》：
  cut 号 / 问题 / 证据（PDF 页码或坐标）/ 建议问客户的话术。
  （0826 cut11 事件本质是这类问题，今后除工程记录外同步产出风险提示。）

### 音乐检索与授权（仅限版权音乐网站）
- 大纲时间线需要参考音乐/正式音乐时，先出 Music Brief：
  Genre / Mood / BPM / Instrument / Energy / Structure（对应段落情绪）。
- 搜索用 `Genre + Mood + Energy + Instrument` 组合关键词，不搜"宣传片音乐"这种大词。
- 版权音乐网站：曲多多 / Musicbed / Artlist / Epidemic Sound / PremiumBeat / AudioJungle；
  免费低成本：Pixabay Music / YouTube Audio Library / Mixkit。
- 每首记录：曲名 / 平台 / URL / 时长 / BPM / 情绪 / 推荐段落 / 授权类型 /
  是否商用 / 是否要求署名 / 下载日期。下载归档到 `02_AUDIO/MUSIC`，
  命名 `MUS_平台_编号_曲名_情绪_BPM`；License 文件/截图存 `LICENSE/`。
- **授权不明确标 `LICENSE_UNCONFIRMED`，只能进大纲试剪，不得进最终交付。**

### 音乐检索操作通路（0827 实测分级，按能力选路）
- **路 A｜Mixkit 无浏览器直通（已实测，首选兜底）**：
  `scripts/mixkit_search.py <tag> [--download N --out DIR]`，无需浏览器、无需登录。
  原理：tag 列表页内嵌 JSON-LD（曲名/流派/作者/时长/mp3 直链/授权声明），
  curl 直接抓页解析下载，授权页 https://mixkit.co/license/#musicFree 可达。
  已验证 tag：corporate / cinematic（其余 tag 跑时验证）。macOS 框架版 Python 缺 CA
  证书，脚本内部走 curl 不走 urllib。
- **路 B｜Musicbed 无浏览器直通（0827 实测）**：
  `scripts/musicbed_search.py mb "<query>" [--preview N --out DIR]`，
  POST `novus-api.musicbed.com/api/search/songs` 返回全字段 JSON
  （曲名/艺人/时长/流派/30s 试听直链），30s 试听可直接下载；
  **全长 preview 端点 401 = 登录墙**，下载的试听文件名带 `_LOGIN_GATED` 标记。
- **路 C｜环球 UPM 无浏览器搜候选（0827 实测）**：
  `scripts/musicbed_search.py upm "<query>" [--locale en-hk]`，
  SSR 搜索页解析 itemprop 元数据（id/曲名/关键词/时长）。
  **试听音频 CDN 403 需浏览器**；SSR 页偶发 40s+ 慢响应，脚本已放宽超时到 120s。
- **路 D｜需真实浏览器的商业库（0827 实测，均无需登录即可读候选）**：
  - 曲多多 = **haifanwu.com**（旧域名 qudodo.com 已失效，勿用）：
    `/library` 未登录可读曲名/场景情绪标签/BPM/时长/分轨标记；"立即下载"需登录，
    有"试用无水印"机制。
  - PremiumBeat：curl 403（Cloudflare），浏览器内
    `/zh/royalty-free-music?term=<query>` 可读曲名/艺人/时长/BPM/流派/情绪；
    下载需账号。
  - Artlist：curl 直接超时，浏览器内
    `/royalty-free-music/search?search=<query>` 可读曲名/艺人/流派/时长；
    下载需 Sign In + 订阅。
  - Pixabay Music：Cloudflare 拦 curl，同走浏览器。
  - 浏览器控制用 in-app browser 或用户本机**任意浏览器**（不依赖 Chrome），
    商业库下载一律操作用户已登录会话，无登录态只出候选表，不得假装已下载。
    授权合规主体是用户/客户，agent 只负责记录与归档。
- 三路都失败时按「降级总原则」输出关键词 + 候选表 + 命名/目录方案。

### 动效与文字的分工（v0.5.2 修订：动效归 AI，AE 只管文字备注）
- **动效示意一律走 AI/程序化生成**（Remotion / HyperFrames / imagegen / 3D 预演，
  即 v0.2 已有通路），不拆"AE 包装清单"——避免与用户的 AI 动效流水线冲突。
- **AE 在大纲阶段的职责收窄为时间线文字**：super（卖点字）、备注（场说明）、
  字幕轨。读脚本时输出《时间线文字清单》，字段：
  cut 号 / 类型（super / 备注 / 字幕）/ 文案（脚本原文，区分搭建推断）/ 位置 / 时长。
- 若后期确实需要 AE 成片包装（跟踪合成/HUD/三维），不在这里展开，
  转交后期启动助手类流程处理，本 skill 不加 L1–L5 分级。

### 素材缺口核查
- 逐 cut 核对后输出《素材缺口清单》，状态分类：
  `OK` 已有素材 / `CHECK FOOTAGE` 可能有待核 / `CLIENT` 需客户提供 /
  `STOCK` 走图库 / `AI` 生成示意（动效示意默认走这条）/ `3D` 三维预演 /
  `POST` 留给后期（AE 等，本 skill 不实现）。
- 缺素材的 cut 仍按占位/示意规则上轨保持结构完整，清单随交付物一起给剪辑师。

### 降级总原则
- 任何一步因权限/崩溃/网站不可达做不到时：**不得假装已完成**，明确说明哪步没做成，
  同时输出可人工执行的完整替代方案（关键词、URL、命名、目标目录、操作步骤），
  能力恢复后续跑。

### 执行优先级（时间不够时按此裁剪）
- P0（没有就不算 motionboard）：分镜按 cut 顺序上轨、VO/台词、场 marker。
- P1：SRT 字幕、super、缺素材占位/示意、《素材缺口清单》。
- P2：音效五族、音乐 stem 分层、《时间线文字清单》、授权记录。
- P3：备选叠轨、对照轨、多画幅参照。

### 交付清单（完工判定）
交给剪辑师前逐项打勾，缺一不可：
- [ ] cut 表（cut/脚本原文/搭建推断分列）
- [ ] 台词表（cut/角色/台词/语气/音色ID）
- [ ] SRT 字幕（cue 起止=VO 实际起止，遵守央视五条）
- [ ] 分场 marker（note 写整句场描述）
- [ ] 缺素材 cut 占位/示意齐全 + 《素材缺口清单》
- [ ] 《时间线文字清单》（super/备注/字幕，动效示意归 AI 不列 AE 清单）
- [ ] 音乐/SFX 授权记录（含 LICENSE_UNCONFIRMED 标记）
- [ ] 《脚本风险提示》（无问题也要产出，写"无"）
- [ ] 工程已 SaveProject，版本号/日期可回溯

全部打勾才可说"已具备交剪条件"；否则明确说"当前不具备交剪条件，缺：___"。
