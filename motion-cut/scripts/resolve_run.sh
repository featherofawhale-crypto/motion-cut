#!/bin/zsh
# resolve_run.sh — 达芬奇脚本的唯一正确启动方式（防崩版）
# 用法: tools/resolve_run.sh <script.py> [log名]
# 规则见 docs/达芬奇脚本稳定性-runbook.md:
#   1) 不硬杀脚本进程 (无 alarm / timeout)
#   2) 跑前清场: 检查 Resolve 进程 + 模态窗
#   3) 输出双写到日志, 外部读日志判断进度
set -u
SCRIPT="$1"
LOG="${2:-/tmp/resolve_run_$(basename "$SCRIPT" .py).log}"

export LANG=zh_CN.UTF-8 PYTHONUTF8=1
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve 19/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$RESOLVE_SCRIPT_API/Modules"

# --- 预检: Resolve 进程 ---
if ! pgrep -x Resolve >/dev/null; then
    echo "Resolve 未运行, 启动中..."
    open -a "/Applications/DaVinci Resolve 19/DaVinci Resolve.app"
    sleep 25
fi

# --- 预检: 模态窗 ---
WINS=$(osascript -e 'tell application "System Events" to tell process "Resolve" to get name of every window' 2>/dev/null || echo "查询失败")
if echo "$WINS" | grep -qE "问题报告|Report"; then
    echo "!! 检测到崩溃报告窗, 请先处理(点忽略), 中止: $WINS"
    exit 2
fi
echo "预检通过, 窗口: $WINS"
echo "日志: $LOG"

# --- 跑 (不硬杀; 脚本自带重试与分段落盘) ---
python3 -u "$SCRIPT" 2>&1 | tee "$LOG"
exit ${pipestatus[1]}
