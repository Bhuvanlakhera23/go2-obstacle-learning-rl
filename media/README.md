# Supplementary qualitative videos

These are author-supplied simulator screencasts, added to the repository README
after the technical-report release. They are not new evaluation runs, independently
adjudicated traversal evidence or an extension of the report's benchmark.

| Public clip | Original recording | Policy identification |
|---|---|---|
| `fixed-mixture-stair-climb.mp4` | `Screencast from 10-22-2026 04:52:08 PM.webm` | User-confirmed Fixed-Mixture Policy |
| `pretrained-reference-stair-attempt.mp4` | `Screencast from 10-22-2026 05:00:04 PM.webm` | User-confirmed Model5099, publicly named Pretrained Reference |

The author describes a **28 cm** obstacle setup. Whether that refers to each
riser or the total obstacle height is not documented in the supplied recording
metadata. The clips contain no measurement/configuration record establishing
the geometry or a cryptographic link to the report's checkpoint identities.
The recordings show selected manual demonstrations, not matched commands,
randomizations, independent training seeds or a measured success rate. In
particular, the comparison is with the **historical reference**, not the
Adaptive-Frontier Policy. No general superiority or new hardware result follows.

The original WebM files remain unchanged with the authors. For browser playback,
the complete video timelines were converted to H.264 MP4 at 30 fps, with one
black bottom row added to make the odd source height even (1172×629 → 1172×630).
No temporal trimming, speed change, synthetic frame generation, contact overlay
or simulation execution was used. Conversion samples the original variable-rate
timeline at 30 fps; exact compressed frame bytes differ. Source metadata is
stripped; neither source contains an audio stream. The PNG previews are actual
frames extracted from the corresponding recordings, not generated illustrations.

The README's looping GIFs now use the newer author-supplied MP4 files:
`Screencast from 10-22-2026 04_52_08 PM.mp4` (Fixed-Mixture Policy, 45.55 s)
and `Screencast from 10-22-2026 05_00_04 PM.mp4` (Pretrained Reference, 45.005 s).
Their complete supplied timelines are converted at 400 pixels wide and 8 fps,
with infinite looping and original playback speed (subject to GIF frame-delay
rounding). No additional temporal trimming is applied during GIF conversion.
These newer source files remain unchanged with the authors; their hashes are
recorded in the provenance manifest. The linked full-resolution MP4s and static
previews still refer to the earlier, longer recordings described above.

Source/derived checksums, durations and conversion settings are recorded in
[MEDIA_UPDATE.json](../MEDIA_UPDATE.json). The original
[VERIFICATION.json](../VERIFICATION.json), scientific tables, figures, manuscript,
`v1.1.0` tag and pre-existing Zenodo package remain unchanged. The inventory
checker accepts only this explicit README/media supplement; all other original
files retain their recorded hashes.

The supplementary recordings/previews are shared as report media under
[CC BY 4.0](../LICENSE.md), with attribution to Bhuvan Lakhera and Deepan
Muthirayan. No checkpoint, simulator source or robot asset is distributed.
