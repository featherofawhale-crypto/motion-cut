#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pr_ui_text: 用 UI 自动化(文字工具)在 PR 时间线上创建原生可编辑文字。
流程: MCP 定位播放头+目标轨 -> Quartz 点击节目监视器 -> 剪贴板粘贴文字 -> JSX 收尾定长。
用法: python3 pr_ui_text.py <seq_name> <track_index> <start_s> <end_s> <text> <click_x> <click_y> [scale]
环境变量: PR_SEQ_ID (目标序列 id, 必传), PR_MCP_PYTHON (带 mcp 库的 python),
          PR_TOOLS_DIR (pr_mcp_client.py / pr_jsx_eval.mjs 所在目录, 默认本脚本目录)
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PR_MCP_PYTHON = os.environ.get("PR_MCP_PYTHON", "python3")
TOOLS_DIR = os.environ.get("PR_TOOLS_DIR", HERE)

SEQ, TRACK, T0, T1, TEXT, CX, CY = (sys.argv[1], int(sys.argv[2]), float(sys.argv[3]),
                                     float(sys.argv[4]), sys.argv[5], int(sys.argv[6]), int(sys.argv[7]))
SCALE = sys.argv[8] if len(sys.argv) > 8 else "55"


def osa(script: str) -> None:
    subprocess.run(["osascript", "-e", script], check=True)


def click(x: int, y: int) -> None:
    code = (
        "import Quartz,time\n"
        f"p=Quartz.CGPointMake({x},{y})\n"
        "for t in (Quartz.kCGEventLeftMouseDown, Quartz.kCGEventLeftMouseUp):\n"
        "    e=Quartz.CGEventCreateMouseEvent(None,t,p,Quartz.kCGMouseButtonLeft)\n"
        "    Quartz.CGEventPost(Quartz.kCGHIDEventTap,e); time.sleep(0.08)\n"
    )
    subprocess.run(["python3", "-c", code], check=True)


SEQ_ID = os.environ.get("PR_SEQ_ID")
if not SEQ_ID:
    sys.exit("请设 PR_SEQ_ID 为目标序列 id (list_sequences 可查)")


def mcp(tool: str, args: dict) -> dict:
    import json
    r = subprocess.run([PR_MCP_PYTHON,
                        os.path.join(TOOLS_DIR, "pr_mcp_client.py"), tool,
                        json.dumps(args, ensure_ascii=False)],
                       check=True, capture_output=True, text=True)
    raw = r.stdout
    d = json.loads(raw[raw.index("{"):])
    sc = d.get("structuredContent") or {}
    if d.get("isError") or sc.get("success") is False:
        raise RuntimeError(f"{tool}: {raw[-300:]}")
    return sc


# 1) MCP: 目标轨 + 播放头 (带 sequenceId + 读回验证)
mcp("set_target_track", {"trackType": "video", "trackIndex": TRACK, "targeted": True})
mcp("set_playhead_position", {"sequenceId": SEQ_ID, "time": T0})
ph = mcp("get_playhead_position", {"sequenceId": SEQ_ID})
got = float(ph.get("position", -1))
if abs(got - T0) > 0.2:
    raise RuntimeError(f"播放头未就位: want {T0} got {got}")

# 2) UI: 文字工具 -> 点击 -> 粘贴 -> esc -> 选择工具
osa('tell application "Adobe Premiere Pro 2024" to activate')
time.sleep(0.8)
osa('tell application "System Events" to key code 53')  # esc: 防上次卡在文本编辑态
osa('tell application "System Events" to keystroke "v"')  # 选择工具
time.sleep(0.3)
osa('tell application "System Events" to keystroke "t"')
time.sleep(0.4)
click(CX, CY)
time.sleep(0.8)
subprocess.run(["pbcopy"], input=TEXT.encode(), check=True)
osa('tell application "System Events" to keystroke "v" using command down')
time.sleep(0.6)
osa('tell application "System Events" to key code 53')  # esc 退出编辑
osa('tell application "System Events" to keystroke "v"')  # 回选择工具
time.sleep(0.5)

# 3) JSX: 全轨找新图形剪辑(起点最接近 T0 的"图形"), 定长到 T1, 缩放
jsx = f"""(function(){{
  var seq=null;
  for(var si=0;si<app.project.sequences.numSequences;si++) if(app.project.sequences[si].name==="{SEQ}"){{seq=app.project.sequences[si];break;}}
  if(!seq) return "seq not found";
  var best=null,bd=1e9;
  var bestTr=-1;
  for(var ti=0;ti<seq.videoTracks.numTracks;ti++){{
    var tr=seq.videoTracks[ti];
    for(var i=0;i<tr.clips.numItems;i++){{
      var c=tr.clips[i];
      var hasText=false;
      for(var ci2=0;ci2<c.components.numItems;ci2++) if(c.components[ci2].matchName==="AE.ADBE Text") hasText=true;
      if(!hasText) continue;
      var d=Math.abs(c.start.seconds-{T0});
      if(d<bd){{bd=d;best=c;bestTr=ti;}}
    }}
  }}
  if(!best||bd>1.0) return "not found";
  var t=new Time(); t.seconds={T1}; best.end=t;
  for(var ci=0;ci<best.components.numItems;ci++){{
    var comp=best.components[ci];
    if(comp.displayName==="运动"){{
      for(var pi=0;pi<comp.properties.numItems;pi++){{
        var p=comp.properties[pi];
        if(p.displayName==="缩放") p.setValue({SCALE},1);
      }}
    }}
  }}
  app.project.save();
  return "ok V"+(bestTr+1)+" "+best.start.seconds.toFixed(2)+"-"+best.end.seconds.toFixed(2);
}})()"""
r = subprocess.run(["node", os.path.join(TOOLS_DIR, "pr_jsx_eval.mjs"), jsx],
                   capture_output=True, text=True, timeout=60)
print(r.stdout.strip() or r.stderr.strip())
