#!/usr/bin/env bash
# Pod bootstrap for the ComfyUI VACE batch: Cloudflare R2 is the model origin
# (zero egress, ~$0.015/GB/mo), the pod's local disk is the working copy.
#
#   pod_bootstrap.sh models-push          # ONCE, on a pod that already has the models: manifest + upload to R2
#   pod_bootstrap.sh pull                 # every fresh pod: pull models + wan/ from R2, verify sizes, start ComfyUI
#   pod_bootstrap.sh out-push songs/<slug>  # after a batch: copy songs/<slug>/out/ to R2 (laptop pulls from there)
#   pod_bootstrap.sh wan-push             # from a pod (or laptop with rclone): refresh r2://.../wan/ from ./ (comfy, prompts, docs, songs)
#
# Env (same names the serverless worker uses -- set them as POD environment
# variables in the RunPod console, never in the repo or the image):
#   S3_BUCKET             bucket name
#   S3_ENDPOINT_URL       https://<acct>.r2.cloudflarestorage.com
#   AWS_ACCESS_KEY_ID     R2 API token id
#   AWS_SECRET_ACCESS_KEY R2 API token secret
# Optional:
#   COMFY_ROOT   ComfyUI checkout on the pod (default /workspace/ComfyUI; auto-detected if missing)
#   WAN_ROOT     where comfy/, prompts/, docs/, songs/ live on the pod (default /workspace/wan)
#   R2_PREFIX    key prefix inside the bucket (default "wan-models")
#   COMFY_PORT   default 8188
#   START_COMFY  1 (default) = start ComfyUI after pull if port is not answering; 0 = don't
set -euo pipefail

CMD="${1:-pull}"; shift || true
COMFY_ROOT="${COMFY_ROOT:-/workspace/ComfyUI}"
WAN_ROOT="${WAN_ROOT:-/workspace/wan}"
R2_PREFIX="${R2_PREFIX:-wan-models}"
COMFY_PORT="${COMFY_PORT:-8188}"
START_COMFY="${START_COMFY:-1}"
MANIFEST="MANIFEST.txt"

# The four model files (relative to <COMFY_ROOT>/models) + the LoRA. Keep in
# sync with comfy/vace_ref2v_api.json.
MODEL_FILES=(
  "diffusion_models/wan2.1_vace_14B_fp16.safetensors"
  "text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors"
  "vae/wan_2.1_vae.safetensors"
  "loras/Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank64.safetensors"
)

log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
die() { log "ERROR: $*"; exit 1; }

need_env() {
  local missing=0
  for v in S3_BUCKET S3_ENDPOINT_URL AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY; do
    [ -n "${!v:-}" ] || { log "missing env $v"; missing=1; }
  done
  [ "$missing" = 0 ] || die "set the R2 variables in the pod environment (RunPod console -> pod -> Environment Variables)"
  # rclone reads the remote "r2" straight from these -- no config file, nothing written to disk.
  export RCLONE_CONFIG_R2_TYPE=s3
  export RCLONE_CONFIG_R2_PROVIDER=Cloudflare
  export RCLONE_CONFIG_R2_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID"
  export RCLONE_CONFIG_R2_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY"
  export RCLONE_CONFIG_R2_ENDPOINT="$S3_ENDPOINT_URL"
  export RCLONE_CONFIG_R2_REGION=auto
  export RCLONE_CONFIG_R2_ACL=private
  export RCLONE_CONFIG_R2_NO_CHECK_BUCKET=true
}

ensure_rclone() {
  if ! command -v rclone >/dev/null 2>&1; then
    log "installing rclone"
    curl -fsSL https://rclone.org/install.sh | bash >/dev/null 2>&1 || die "rclone install failed (apt-get install rclone as a fallback)"
  fi
  rclone version | head -1
}

detect_comfy_root() {
  if [ ! -d "$COMFY_ROOT/models" ]; then
    local found
    found="$(find / -maxdepth 4 -type d -path '*ComfyUI/models' 2>/dev/null | head -1 || true)"
    [ -n "$found" ] || die "ComfyUI models dir not found; set COMFY_ROOT"
    COMFY_ROOT="$(dirname "$found")"
  fi
  log "COMFY_ROOT=$COMFY_ROOT"
}

file_size() { stat -c %s "$1" 2>/dev/null || stat -f %z "$1"; }

# rclone flags tuned for a handful of big files: parallel multipart, big chunks.
RC_FLAGS=(--transfers 4 --checkers 8 --multi-thread-streams 8 --multi-thread-cutoff 256M
          --s3-chunk-size 64M --s3-upload-concurrency 8 --stats 30s --stats-one-line --progress)

cmd_models_push() {
  need_env; ensure_rclone; detect_comfy_root
  local src="$COMFY_ROOT/models" dst="r2:$S3_BUCKET/$R2_PREFIX/models"
  : > "$src/$MANIFEST"
  for f in "${MODEL_FILES[@]}"; do
    [ -f "$src/$f" ] || die "missing $src/$f -- nothing pushed"
    printf '%s %s\n' "$(file_size "$src/$f")" "$f" >> "$src/$MANIFEST"
  done
  log "manifest:"; cat "$src/$MANIFEST"
  local t0; t0=$(date +%s)
  for f in "${MODEL_FILES[@]}"; do
    rclone copyto "$src/$f" "$dst/$f" "${RC_FLAGS[@]}"
  done
  rclone copyto "$src/$MANIFEST" "$dst/$MANIFEST"
  log "verifying sizes on R2"
  verify_remote "$dst" "$src/$MANIFEST"
  log "models-push done in $(( $(date +%s) - t0 )) s -> $dst"
}

verify_remote() {  # <remote dir> <manifest>
  local dst="$1" man="$2" ok=1
  while read -r size f; do
    local rs
    rs="$(rclone lsjson "$dst/$f" | python3 -c 'import sys,json;l=json.load(sys.stdin);print(l[0]["Size"] if l else "missing")')"
    if [ "$rs" = "$size" ]; then log "  OK   $f $size"; else log "  BAD  $f local=$size remote=$rs"; ok=0; fi
  done < "$man"
  [ "$ok" = 1 ] || die "remote sizes differ from manifest"
}

verify_local() {  # <local models dir> <manifest>
  local dir="$1" man="$2" ok=1
  while read -r size f; do
    local ls_
    ls_="$(file_size "$dir/$f" 2>/dev/null || echo missing)"
    if [ "$ls_" = "$size" ]; then log "  OK   $f $size"; else log "  BAD  $f expected=$size got=$ls_"; ok=0; fi
  done < "$man"
  [ "$ok" = 1 ] || die "local model files do not match the manifest -- do not start a batch"
}

wait_ready() {  # blocks until /object_info/UNETLoader lists the VACE UNET, or 15 min
  local url="http://127.0.0.1:$COMFY_PORT/object_info/UNETLoader" t0; t0=$(date +%s)
  while [ $(( $(date +%s) - t0 )) -lt 900 ]; do
    if curl -fsS -A "Mozilla/5.0 WanComfyDriver" "$url" 2>/dev/null | grep -q "wan2.1_vace_14B_fp16.safetensors"; then
      log "ComfyUI ready on :$COMFY_PORT (UNETLoader lists the VACE model)"; return 0
    fi
    sleep 5
  done
  die "ComfyUI did not become ready in 15 min"
}

cmd_pull() {
  need_env; ensure_rclone; detect_comfy_root
  local T0; T0=$(date +%s)
  local src="r2:$S3_BUCKET/$R2_PREFIX/models" dst="$COMFY_ROOT/models"
  mkdir -p "$dst/diffusion_models" "$dst/text_encoders" "$dst/vae" "$dst/loras"
  rclone copyto "$src/$MANIFEST" "$dst/$MANIFEST" || die "no $MANIFEST on R2 -- run 'models-push' once first"
  # rclone copy skips files that already match by size+modtime, so a re-run on a
  # warm pod (or a pod whose disk kept the files) costs seconds.
  while read -r _ f; do
    rclone copyto "$src/$f" "$dst/$f" "${RC_FLAGS[@]}"
  done < "$dst/$MANIFEST"
  local T1; T1=$(date +%s)
  log "models pulled in $(( T1 - T0 )) s; verifying"
  verify_local "$dst" "$dst/$MANIFEST"

  # runner + prompts + songs, so the batch runs on the pod against 127.0.0.1 (no proxy, no 403)
  mkdir -p "$WAN_ROOT"
  if rclone lsf "r2:$S3_BUCKET/$R2_PREFIX/wan/" >/dev/null 2>&1; then
    rclone sync "r2:$S3_BUCKET/$R2_PREFIX/wan/" "$WAN_ROOT/" --exclude "**/out/**" --exclude "__pycache__/**" --stats-one-line
    log "wan/ synced to $WAN_ROOT"
  else
    log "no $R2_PREFIX/wan/ on R2 -- copy comfy/, prompts/, docs/, songs/ to $WAN_ROOT by hand (or run 'wan-push' from the laptop)"
  fi

  if [ "$START_COMFY" = 1 ]; then
    if ! curl -fsS -A "Mozilla/5.0 WanComfyDriver" "http://127.0.0.1:$COMFY_PORT/system_stats" >/dev/null 2>&1; then
      log "starting ComfyUI"
      ( cd "$COMFY_ROOT" && nohup python main.py --listen 0.0.0.0 --port "$COMFY_PORT" > /workspace/comfyui.log 2>&1 & )
    fi
    wait_ready
  fi
  local T2; T2=$(date +%s)
  log "BOOT-TO-READY: models $(( T1 - T0 )) s, total $(( T2 - T0 )) s"
  log "next: cd $WAN_ROOT && python comfy/batch_runner.py --song songs/<slug> --hosts http://127.0.0.1:$COMFY_PORT --dry-run"
}

cmd_wan_push() {
  need_env; ensure_rclone
  for d in comfy prompts docs songs; do [ -d "$d" ] || die "run from the repo root (missing ./$d)"; done
  for d in comfy prompts docs songs; do
    rclone sync "./$d/" "r2:$S3_BUCKET/$R2_PREFIX/wan/$d/" --exclude "**/out/**" --exclude "__pycache__/**" --exclude "*.pyc" --stats-one-line
  done
  log "wan/ pushed"
}

cmd_out_push() {
  need_env; ensure_rclone
  local song="${1:-}"; [ -n "$song" ] || die "usage: out-push songs/<slug>"
  [ -d "$song/out" ] || die "no $song/out"
  local slug; slug="$(basename "$song")"
  rclone copy "$song/out/" "r2:$S3_BUCKET/songs/$slug/out/" --stats-one-line --progress
  rclone copyto "$song/shots.csv" "r2:$S3_BUCKET/songs/$slug/shots.csv"
  log "out/ pushed -> r2:$S3_BUCKET/songs/$slug/out/  (laptop: rclone copy r2:$S3_BUCKET/songs/$slug/out/ songs/$slug/out/)"
}

case "$CMD" in
  models-push) cmd_models_push ;;
  pull)        cmd_pull ;;
  wan-push)    cmd_wan_push ;;
  out-push)    cmd_out_push "$@" ;;
  *) die "unknown command $CMD (models-push | pull | wan-push | out-push <song>)" ;;
esac
