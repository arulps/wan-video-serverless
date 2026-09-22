#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Which endpoint this deploy targets. Default: the 5B endpoint. The VACE
# endpoint's workflow sets ENDPOINT_CONFIG=config/endpoint-vace.json.
CONFIG="${ENDPOINT_CONFIG:-$ROOT/config/endpoint.json}"
case "$CONFIG" in /*) ;; *) CONFIG="$ROOT/$CONFIG" ;; esac
[ -f "$CONFIG" ] || { echo "FATAL: endpoint config not found: $CONFIG"; exit 1; }
echo "== endpoint config: $CONFIG =="
export RUNPOD_API_KEY="${RUNPOD_API_KEY:?RUNPOD_API_KEY must be set}"

PY="${PYTHON:-python3}"

cfg() { "$PY" "$ROOT/scripts/config_get.py" "$CONFIG" "$@"; }

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
# RunPod cached model (host-side, unbilled). Format is the full HF URL + revision.
# Passed on EVERY update so a deploy can never silently drop it (verified needed
# 2026-09-21: `serverless update` without it left the reference in doubt).
MODEL_REF="${MODEL_REFERENCE:-$(cfg endpoint.modelReference --default '')}"
MODEL_REF_ARGS=()
if [ -n "$MODEL_REF" ]; then
    MODEL_REF_ARGS=(--model-reference "$MODEL_REF")
fi
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
    # Re-bind the template on EVERY deploy. Without --template-id the endpoint
    # keeps whatever template it was already pointing at, so a freshly built
    # image could be upserted into a template the endpoint no longer used and
    # the deploy would report success while changing nothing that runs.
    runpodctl serverless update "$EP_ID" \
        --template-id "$TPL_ID" \
        --workers-min "$(cfg endpoint.workersMin)" \
        --workers-max "$(cfg endpoint.workersMax)" \
        --idle-timeout "$(cfg endpoint.idleTimeoutSec)" \
        "${MODEL_REF_ARGS[@]}"
    echo "updated endpoint $EP_ID (template $TPL_ID, model ref ${MODEL_REF:-none})"

    # runpodctl 2.14.0 `serverless update` has NO --execution-timeout flag (it
    # exists only on create; CI run 35636080696 failed on it). Settings that the
    # CLI cannot update on an existing endpoint go through the REST API instead:
    #   PATCH https://rest.runpod.io/v1/endpoints/{id}   (docs.runpod.io/api-reference)
    # Fields verified there: executionTimeoutMs, gpuTypeIds (priority order),
    # workersMin/Max, idleTimeout, templateId. gpuTypeIds is taken from
    # endpoint.gpuTypeIds (a JSON list) when present, else the single gpuId.
    EXEC_MS=$(( $(cfg endpoint.executionTimeoutSec) * 1000 ))
    GPU_IDS_JSON="$(cfg endpoint.gpuTypeIds --default '' --raw-json)"
    if [ -z "$GPU_IDS_JSON" ] || [ "$GPU_IDS_JSON" = "null" ]; then
        GPU_IDS_JSON="$("$PY" -c 'import json,sys; print(json.dumps([sys.argv[1]]))' "$DESIRED_GPU")"
    fi
    PATCH_BODY="$("$PY" -c 'import json,sys; print(json.dumps({"executionTimeoutMs": int(sys.argv[1]), "gpuTypeIds": json.loads(sys.argv[2])}))' "$EXEC_MS" "$GPU_IDS_JSON")"
    echo "== REST PATCH endpoint $EP_ID: $PATCH_BODY =="
    PATCH_RESP="$(curl -sS -w '\nHTTP %{http_code}' -X PATCH \
        -H "Authorization: Bearer $RUNPOD_API_KEY" -H "Content-Type: application/json" \
        "https://rest.runpod.io/v1/endpoints/$EP_ID" -d "$PATCH_BODY" || true)"
    echo "$PATCH_RESP" | tail -c 600
    case "$PATCH_RESP" in
        *"HTTP 2"*) echo "endpoint PATCH applied (executionTimeoutMs=$EXEC_MS)";;
        *) echo "ERROR: endpoint PATCH failed - execution timeout / GPU list NOT applied"; exit 1;;
    esac

    # The previous version compared the configured GPU against a substring grep
    # of the whole endpoint JSON and, on any mismatch, DELETED and recreated the
    # endpoint. That hands you a new endpoint id while .env still holds the old
    # one -- the origin of the 404-chasing documented in RUNBOOK section 6.
    # Warn; never destroy. Deleting an endpoint is a deliberate human act.
    CURRENT="$(runpodctl serverless get "$EP_ID" -o json 2>/dev/null || true)"
    if [ -n "$CURRENT" ] && ! grep -Fq "$DESIRED_GPU" <<< "$CURRENT"; then
        echo "WARNING: endpoint $EP_ID does not report GPU '$DESIRED_GPU'."
        echo "WARNING: NOT recreating it. Change the GPU in the RunPod console,"
        echo "WARNING: or delete the endpoint by hand if that is really intended."
    fi
fi

if [ -z "$EP_ID" ]; then
    # No trailing '|| true' here. If create fails -- an unsupported flag on this
    # runpodctl version, a quota refusal, a bad --gpu-id -- we want the real
    # error and a non-zero exit, not a silent fall-through to the FATAL below
    # with the actual cause swallowed.
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
        --min-cuda-version "$(cfg endpoint.minCudaVersion)" \
        "${MODEL_REF_ARGS[@]}"
    runpodctl serverless list -o json 2>/dev/null > "$EP_FILE" || true
    EP_ID="$(find_id_by_name "$EP_NAME" "$EP_FILE" || true)"
    echo "created endpoint: ${EP_ID:-FAILED}"
fi

if [ -z "${EP_ID:-}" ]; then
    echo "FATAL: endpoint '$EP_NAME' was not created"
    exit 1
fi

# Rotate workers onto the new image.
#
# runpodctl updates the TEMPLATE, but already-running worker containers keep the
# image they booted with. Without this step a deploy leaves stale workers serving
# the old code while every dashboard says the template is current -- the exact
# trap written up in RUNBOOK section 6, which until now had to be worked around
# by hand on every deploy.
#
# Scaling max to 0 terminates any in-flight job, which is acceptable immediately
# after a build. Set ROTATE_WORKERS=0 to skip.
# 2026-09-21: a fixed 30 s sleep was not enough. FlashBoot keeps idle workers
# warm on the OLD image and they were still serving after the restore, so the
# selftest saw a stale worker (empty PYTORCH_CUDA_ALLOC_CONF) and the run had to
# be rotated by hand. Now: scale to 0, then POLL /health until every worker
# count is 0 (or ROTATE_MAX_WAIT_SEC elapses), and only then restore.
worker_count() {
    curl -fsS -H "Authorization: Bearer $RUNPOD_API_KEY" \
        "https://api.runpod.ai/v2/$EP_ID/health" 2>/dev/null | "$PY" -c '
import json, sys
try:
    w = json.load(sys.stdin).get("workers", {})
    print(sum(int(w.get(k, 0) or 0) for k in ("idle", "initializing", "ready", "running", "throttled", "unhealthy")))
except Exception:
    print(-1)
'
}

if [ "${ROTATE_WORKERS:-1}" = "1" ]; then
    echo "== rotating workers onto $TPL_IMAGE =="
    runpodctl serverless update "$EP_ID" --workers-min 0 --workers-max 0
    max_wait="${ROTATE_MAX_WAIT_SEC:-420}"
    waited=0
    while :; do
        n="$(worker_count)"
        echo "  drain: workers=$n after ${waited}s"
        if [ "$n" = "0" ]; then break; fi
        if [ "$waited" -ge "$max_wait" ]; then
            echo "WARNING: workers still present after ${max_wait}s; restoring anyway."
            echo "WARNING: a stale worker may serve the old image until it idles out -"
            echo "WARNING: the selftest job's alloc_conf/image check will catch it."
            break
        fi
        sleep 15
        waited=$((waited + 15))
    done
    runpodctl serverless update "$EP_ID" \
        --workers-min "$(cfg endpoint.workersMin)" \
        --workers-max "$(cfg endpoint.workersMax)"
    echo "workers rotated; next cold start will pull $TPL_IMAGE"
else
    echo "NOTE: ROTATE_WORKERS=0 -- running workers may still serve the OLD image."
fi

echo
echo "Done. Endpoint: $EP_NAME ($EP_ID)"
echo "Image: $TPL_IMAGE"
echo "Test: curl -H \"Authorization: Bearer \$RUNPOD_API_KEY\" -H 'Content-Type: application/json'"
echo "  https://api.runpod.ai/v2/$EP_ID/runsync -d '{\"input\":{\"prompt\":\"a cat surfing\"}}'"