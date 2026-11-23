#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/apps/learn_Loop_engineering"
SEED_IMAGE_DIR="/opt/learn_Loop_engineering"

# 1) 호스트 볼륨(/apps)에 learn_Loop_engineering 소스가 없으면 이미지 내 clone 본을 로컬 볼륨으로 동기화
ensure_app_source_on_volume() {
  if [ ! -d "${APP_DIR}/.git" ]; then
    echo "[entrypoint] /apps 볼륨에 learn_Loop_engineering 초기화 중..."
    mkdir -p "${APP_DIR}"
    if [ -d "${SEED_IMAGE_DIR}/.git" ]; then
      cp -a "${SEED_IMAGE_DIR}/." "${APP_DIR}/"
      echo "[entrypoint] 이미지 clone 본을 ${APP_DIR} (로컬 볼륨 연계)에 배치 완료"
    else
      git clone https://github.com/yojulab/learn_Loop_engineering.git /tmp/_seed_repo
      cp -a /tmp/_seed_repo/. "${APP_DIR}/"
      rm -rf /tmp/_seed_repo
      echo "[entrypoint] git clone 완료: ${APP_DIR}"
    fi
  else
    echo "[entrypoint] 로컬 볼륨 소스 확인됨: ${APP_DIR}"
  fi
}

# 2) Langfuse 인증 API(/api/public/v2/prompts) 준비 대기 후 ch11 seed_prompts.py 자동 실행
seed_ch11_prompts() {
  local host="${LANGFUSE_HOST:-}"
  local pk="${LANGFUSE_PUBLIC_KEY:-}"
  local sk="${LANGFUSE_SECRET_KEY:-}"
  local support_dir="${APP_DIR}/ch11-eval-and-llmops"

  if [ -z "${host}" ] || [ -z "${pk}" ] || [ -z "${sk}" ]; then
    echo "[entrypoint] LANGFUSE_HOST/KEY 미설정 — ch11 seed_prompts 건너뜀"
    return 0
  fi

  if [ ! -f "${support_dir}/seed_prompts.py" ]; then
    echo "[entrypoint] seed_prompts.py 없음 (${support_dir}) — 건너뜀"
    return 0
  fi

  echo "[entrypoint] Langfuse 인증 API 대기 중 (${host})..."
  python3 - <<'PY'
import base64
import os
import sys
import time
import urllib.error
import urllib.request

host = os.environ["LANGFUSE_HOST"].rstrip("/")
pk = os.environ["LANGFUSE_PUBLIC_KEY"]
sk = os.environ["LANGFUSE_SECRET_KEY"]
auth_header = "Basic " + base64.b64encode(f"{pk}:{sk}".encode("utf-8")).decode("ascii")

# 1) Wait until both Langfuse server AND headless project API keys are ready (HTTP 200)
deadline = time.time() + 120
ready = False
last_err = ""
while time.time() < deadline:
    try:
        req = urllib.request.Request(
            f"{host}/api/public/v2/prompts",
            headers={"Authorization": auth_header, "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                ready = True
                break
    except urllib.error.HTTPError as e:
        last_err = f"HTTP {e.code}"
    except Exception as e:
        last_err = str(e)
    time.sleep(2)

if not ready:
    print(f"[entrypoint] ERROR: Langfuse API 준비 타임아웃 ({host}, last={last_err})", file=sys.stderr)
    sys.exit(1)

# 2) Run ch11 seed_prompts idempotently
support_dir = "/apps/learn_Loop_engineering/ch11-eval-and-llmops"
sys.path.insert(0, support_dir)
from langfuse_ops import LangfuseOpsClient  # noqa: E402
from seed_prompts import seed_default_prompts  # noqa: E402

ops = LangfuseOpsClient(store_dir="/tmp/langfuse_seed_store", host=host, public_key=pk, secret_key=sk)
for _m in ("gemini-cli", "claude-cli"):
    ops.ensure_custom_model(_m, f"(?i)^({_m}|openai/{_m})$", input_price=0.0000001, output_price=0.0000004)

def _has_label(name: str, label: str) -> bool:
    try:
        ops.get_prompt(name=name, label=label)
        return True
    except Exception:
        return False

if _has_label("support-answer", "production") and _has_label("support-answer", "candidate"):
    print("[entrypoint] ch11 seed_prompts: 'support-answer' (production, candidate) 이미 등록됨 — 건너뜀")
else:
    seed_default_prompts(ops)
    p_prod = ops.get_prompt("support-answer", label="production")
    p_cand = ops.get_prompt("support-answer", label="candidate")
    print(
        f"[entrypoint] ch11 seed_prompts 등록 완료: "
        f"production=v{p_prod.version}, candidate=v{p_cand.version} -> {host}"
    )

# 3) Run ch11 seed_langfuse_dashboard idempotently so Dashboard / Traces / Scores / Datasets are populated
traces = ops.list_traces(limit=1)
if traces:
    print("[entrypoint] ch11 seed_langfuse_dashboard: 기존 트레이스 존재 — 건너뜀")
else:
    dashboard_script = os.path.join(support_dir, "seed_langfuse_dashboard.py")
    if os.path.isfile(dashboard_script):
        import subprocess
        proc = subprocess.run(
            [sys.executable, dashboard_script, "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            print(f"[entrypoint] ch11 seed_langfuse_dashboard 적재 완료: {proc.stdout.strip()}")
        else:
            print(f"[entrypoint] WARN: seed_langfuse_dashboard 실패: {proc.stderr.strip()}", file=sys.stderr)
PY
}

start_cli_bridges() {
  local proxy_dir="${APP_DIR}/ch11-eval-and-llmops/litellm_proxy"
  if [ -f "${proxy_dir}/gemini_openai_bridge.py" ] && ! pgrep -f "gemini_openai_bridge.py" >/dev/null 2>&1; then
    nohup python3 "${proxy_dir}/gemini_openai_bridge.py" --host 0.0.0.0 --port "${GEMINI_BRIDGE_PORT:-4010}" >/tmp/gemini_bridge.log 2>&1 &
    echo "[entrypoint] gemini_openai_bridge 백그라운드 기동 완료 (port=${GEMINI_BRIDGE_PORT:-4010})"
  fi
  if [ -f "${proxy_dir}/claude_openai_bridge.py" ] && ! pgrep -f "claude_openai_bridge.py" >/dev/null 2>&1; then
    nohup python3 "${proxy_dir}/claude_openai_bridge.py" --host 0.0.0.0 --port "${CLAUDE_BRIDGE_PORT:-4011}" >/tmp/claude_bridge.log 2>&1 &
    echo "[entrypoint] claude_openai_bridge 백그라운드 기동 완료 (port=${CLAUDE_BRIDGE_PORT:-4011})"
  fi
}

ensure_app_source_on_volume
start_cli_bridges
seed_ch11_prompts

exec "$@"
