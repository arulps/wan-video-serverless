#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$ROOT/config/endpoint.json"
export RUNPOD_API_KEY="${RUNPOD_API_KEY:?RUNPOD_API_KEY must be set}"

PY="${PYTHON:-python3}"

cfg() { "$PY" "$ROOT/scripts/config_get.py" "$CONFIG" "$1"; }

if ! command -v runpodctl >/dev/null 2>&1; then
    echo "runpodctl not found; downloading..."
    os="$(uname -s)"
    arch="$(uname -m)"
    case "$os:$arch" in
        Linux:x86_64)  asset="runpodctl-linux-amd64" ;;
        Linux:arm64)   asset="runpodctl-linux-arm64" ;;
        Darwin:arm64)  asset="runpodctl-darwin-arm64" ;;
        Darwin:x86_64) asset="runpodctl-darwin-amd64" ;;
        *) echo "unsupported platform: $os $arch"; exit 1 ;;
    esac
    ver="${RUNPODCTL_VERSION:-v2.14.0}"
    curl -fsSL "https://github.com/runpod/runpodctl/releases/download/$ver/$asset" -o /usr/local/bin/runpodctl
    chmod +x /usr/local/bin/runpodctl
fi

TPL_NAME="$(cfg template.name)"
TPL_IMAGE="${TEMPLATE_IMAGE:-$(cfg template.image)}"
TPL_DISK="$(cfg template.containerDiskGb)"

TPL_ENV="$("$PY" - "$CONFIG" <<'PYEOF'
import json
import os
import sys

tpl = json.load(open(sys.argv[1], encoding="utf-8"))["template"]
env = dict(tpl.get("env") or {})
for key in os.environ:
    if key.startswith("TPL_ENV_") and os.environ[key]:
        env[key[len("TPL_ENV_"):]] = os.environ[key]
print(json.dumps(env, separators=(",", ":")))
PYEOF
)"

find_id_by_name() {
    "$PY" - "$1" "$2" <<'PYEOF'
import json
import sys

name, path = sys.argv[1], sys.argv[2]
try:
    with open(path, encoding="utf-8") as fp:
        data = json.load(fp)
except Exception:
    sys.exit(0)

if isinstance(data, dict):
    data = [data]

def walk(node):
    if isinstance(node, dict):
        if node.get("name") == name and isinstance(node.get("id"), str) and node["id"]:
            print(node["id"])
            return True
        for value in node.values():
            if walk(value):
                return True
    elif isinstance(node, list):
        for value in node:
            if walk(value):
                return True
    return False

walk(data)
PYEOF
}

REGISTRY_AUTH_ID="${RUNPOD_REGISTRY_AUTH_ID:-}"
if [ -z "$REGISTRY_AUTH_ID" ]; then
    REG_FILE="$(mktemp)"
    if runpodctl registry list -o json 2>/dev/null > "$REG_FILE"; then
        REGISTRY_AUTH_ID="$(find_id_by_name "ghcr-wan" "$REG_FILE" || true)"
    fi
    rm -f "$REG_FILE"
fi
REG_AUTH_ARGS=()
if [ -n "$REGISTRY_AUTH_ID" ]; then
    REG_AUTH_ARGS=(--registry-auth-id "$REGISTRY_AUTH_ID")
fi

echo "== upserting template: $TPL_NAME =="
EP_FILE=""
TPL_FILE="$(mktemp)"
trap 'rm -f "$TPL_FILE" "$EP_FILE"' EXIT
runpodctl template list --type user -o json 2>/dev/null > "$TPL_FILE" || true
TPL_ID="$(find_id_by_name "$TPL_NAME" "$TPL_FILE" || true)"
if [ -n "$TPL_ID" ]; then
    runpodctl template update "$TPL_ID" --image "$TPL_IMAGE" --container-disk-in-gb "$TPL_DISK" --env "$TPL_ENV" "${REG_AUTH_ARGS[@]}"
    echo "updated template $TPL_ID"
else
    runpodctl template create --name "$TPL_NAME" --image "$TPL_IMAGE" --container-disk-in-gb "$TPL_DISK" --env "$TPL_ENV" --serverless "${REG_AUTH_ARGS[@]}" -o json 2>/dev/null > "$TPL_FILE" || true
    TPL_ID="$(find_id_by_name "$TPL_NAME" "$TPL_FILE" || true)"
    if [ -z "$TPL_ID" ]; then
        runpodctl template list --type user -o json 2>/dev/null > "$TPL_FILE" || true
        TPL_ID="$(find_id_by_name "$TPL_NAME" "$TPL_FILE" || true)"
    fi
    if [ -n "$TPL_ID" ]; then
        echo "created/confirmed template $TPL_ID"
    else
        echo "FATAL: could not find or create template '$TPL_NAME'"
        rm -f "$TPL_FILE"
        exit 1
    fi
fi

EP_NAME="$(cfg endpoint.name)"
DESIRED_POOL="${GPU_POOL:-$(cfg endpoint.gpuPool)}"
DESIRED_GPU="$(cfg endpoint.gpuId 2>/dev/null || true)"
if [ -z "$DESIRED_GPU" ]; then
    DESIRED_GPU="$DESIRED_POOL"
fi

echo "== upserting endpoint: $EP_NAME =="
EP_FILE="$(mktemp)"
runpodctl serverless list -o json 2>/dev/null > "$EP_FILE" || true
EP_ID="$(find_id_by_name "$EP_NAME" "$EP_FILE" || true)"
if [ -n "$EP_ID" ]; then
    CURRENT="$(runpodctl serverless get "$EP_ID" -o json 2>/dev/null || true)"
    if [ -n "$CURRENT" ] && grep -Fq "$DESIRED_GPU" <<< "$CURRENT"; then
        runpodctl serverless update "$EP_ID" \
            --workers-min "$(cfg endpoint.workersMin)" \
            --workers-max "$(cfg endpoint.workersMax)" \
            --idle-timeout "$(cfg endpoint.idleTimeoutSec)"
        echo "updated endpoint $EP_ID"
    else
        echo "GPU pool differs from config; recreating endpoint"
        runpodctl serverless delete "$EP_ID" || true
        EP_ID=""
    fi
fi

if [ -z "$EP_ID" ]; then
    runpodctl serverless create \
        --name "$EP_NAME" \
        --template-id "$TPL_ID" \
        --gpu-id "$DESIRED_GPU" \
        --workers-min "$(cfg endpoint.workersMin)" \
        --workers-max "$(cfg endpoint.workersMax)" \
        --execution-timeout "$(cfg endpoint.executionTimeoutSec)" \
        --idle-timeout "$(cfg endpoint.idleTimeoutSec)" \
        --flash-boot="$(cfg endpoint.flashBoot)" \
        --scale-by "$(cfg endpoint.scaleBy)" \
        --scale-threshold "$(cfg endpoint.scaleThreshold)" \
        --min-cuda-version "$(cfg endpoint.minCudaVersion)" || true
    runpodctl serverless list -o json 2>/dev/null > "$EP_FILE" || true
    EP_ID="$(find_id_by_name "$EP_NAME" "$EP_FILE" || true)"
    echo "created endpoint: ${EP_ID:+yes}"
fi

if [ -z "${EP_ID:-}" ]; then
    echo "FATAL: endpoint '$EP_NAME' was not created"
    exit 1
fi

echo
echo "Done. Endpoint: $EP_NAME ($EP_ID)"
echo "Test: curl -H \"Authorization: Bearer \$RUNPOD_API_KEY\" -H 'Content-Type: application/json'"
echo "  https://api.runpod.ai/v2/$EP_ID/runsync -d '{\"input\":{\"prompt\":\"a cat surfing\"}}'"