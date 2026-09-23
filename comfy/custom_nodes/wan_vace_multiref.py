"""WanVaceToVideoMultiRef -- VACE reference conditioning with SEPARATE reference images.

Why this exists (verified against ComfyUI comfy_extras/nodes_wan.py, 2026-09-22 build):
the core `WanVaceToVideo` node takes a `reference_image` batch but uses only the
first image (`reference_image[:1]`), so feeding it several character tiles is
silently the same as feeding one. Our two-child failures (T17/T18/T20) come from
putting both children on ONE 1280x720 sheet. The original VACE pipeline
(`src_ref_images`) and ComfyUI's own Phantom node encode each reference image on
its own and concatenate the latents on the frame axis; this node does exactly that
for VACE. Everything else -- control video, masks, trim -- is a verbatim copy of
the core node so the two are interchangeable in a workflow (same inputs, same
outputs, `trim_latent` = number of reference images).

Install: copy this file into <ComfyUI>/custom_nodes/ (scripts/pod_bootstrap.sh
`pull` does it from wan/comfy/custom_nodes/) and (re)start ComfyUI; then
GET /object_info/WanVaceToVideoMultiRef must answer.
"""
import torch

import comfy.latent_formats
import comfy.model_management
import comfy.utils
import node_helpers
import nodes


class WanVaceToVideoMultiRef:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "vae": ("VAE",),
                "width": ("INT", {"default": 832, "min": 16, "max": nodes.MAX_RESOLUTION, "step": 16}),
                "height": ("INT", {"default": 480, "min": 16, "max": nodes.MAX_RESOLUTION, "step": 16}),
                "length": ("INT", {"default": 81, "min": 1, "max": nodes.MAX_RESOLUTION, "step": 4}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1000.0, "step": 0.01}),
            },
            "optional": {
                "control_video": ("IMAGE",),
                "control_masks": ("MASK",),
                "reference_image": ("IMAGE",),   # a BATCH: every image is a separate reference
            },
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "LATENT", "INT")
    RETURN_NAMES = ("positive", "negative", "latent", "trim_latent")
    FUNCTION = "encode"
    CATEGORY = "conditioning/video_models"
    DESCRIPTION = "WanVaceToVideo, but every image in the reference_image batch is encoded as its own reference (like Phantom / original VACE src_ref_images)."

    def encode(self, positive, negative, vae, width, height, length, batch_size, strength,
               control_video=None, control_masks=None, reference_image=None):
        latent_length = ((length - 1) // 4) + 1
        if control_video is not None:
            control_video = comfy.utils.common_upscale(control_video[:length].movedim(-1, 1), width, height, "bilinear", "center").movedim(1, -1)
            if control_video.shape[0] < length:
                control_video = torch.nn.functional.pad(control_video, (0, 0, 0, 0, 0, 0, 0, length - control_video.shape[0]), value=0.5)
        else:
            control_video = torch.ones((length, height, width, 3)) * 0.5

        ref_latent = None
        if reference_image is not None:
            refs = comfy.utils.common_upscale(reference_image.movedim(-1, 1), width, height, "bilinear", "center").movedim(1, -1)
            encoded = []
            for i in range(refs.shape[0]):
                encoded.append(vae.encode(refs[i:i + 1, :, :, :3]))     # each -> [1, 16, 1, h/8, w/8]
            ref_latent = torch.cat(encoded, dim=2)                        # [1, 16, N, h/8, w/8]
            ref_latent = torch.cat([ref_latent, comfy.latent_formats.Wan21().process_out(torch.zeros_like(ref_latent))], dim=1)

        if control_masks is None:
            mask = torch.ones((length, height, width, 1))
        else:
            mask = control_masks
            if mask.ndim == 3:
                mask = mask.unsqueeze(1)
            mask = comfy.utils.common_upscale(mask[:length], width, height, "bilinear", "center").movedim(1, -1)
            if mask.shape[0] < length:
                mask = torch.nn.functional.pad(mask, (0, 0, 0, 0, 0, 0, 0, length - mask.shape[0]), value=1.0)

        control_video = control_video - 0.5
        inactive = (control_video * (1 - mask)) + 0.5
        reactive = (control_video * mask) + 0.5

        inactive = vae.encode(inactive[:, :, :, :3])
        reactive = vae.encode(reactive[:, :, :, :3])
        control_video_latent = torch.cat((inactive, reactive), dim=1)
        if ref_latent is not None:
            control_video_latent = torch.cat((ref_latent, control_video_latent), dim=2)

        vae_stride = 8
        height_mask = height // vae_stride
        width_mask = width // vae_stride
        mask = mask.view(length, height_mask, vae_stride, width_mask, vae_stride)
        mask = mask.permute(2, 4, 0, 1, 3)
        mask = mask.reshape(vae_stride * vae_stride, length, height_mask, width_mask)
        mask = torch.nn.functional.interpolate(mask.unsqueeze(0), size=(latent_length, height_mask, width_mask), mode='nearest-exact').squeeze(0)

        trim_latent = 0
        if ref_latent is not None:
            mask_pad = torch.zeros_like(mask[:, :ref_latent.shape[2], :, :])
            mask = torch.cat((mask_pad, mask), dim=1)
            latent_length += ref_latent.shape[2]
            trim_latent = ref_latent.shape[2]

        mask = mask.unsqueeze(0)

        positive = node_helpers.conditioning_set_values(positive, {"vace_frames": [control_video_latent], "vace_mask": [mask], "vace_strength": [strength]}, append=True)
        negative = node_helpers.conditioning_set_values(negative, {"vace_frames": [control_video_latent], "vace_mask": [mask], "vace_strength": [strength]}, append=True)

        latent = torch.zeros([batch_size, 16, latent_length, height // 8, width // 8], device=comfy.model_management.intermediate_device())
        return (positive, negative, {"samples": latent}, trim_latent)


NODE_CLASS_MAPPINGS = {"WanVaceToVideoMultiRef": WanVaceToVideoMultiRef}
NODE_DISPLAY_NAME_MAPPINGS = {"WanVaceToVideoMultiRef": "WanVaceToVideo (multi-reference, separate tiles)"}
