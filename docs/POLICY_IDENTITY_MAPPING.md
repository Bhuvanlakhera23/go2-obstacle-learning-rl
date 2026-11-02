# Reproducibility appendix: policy and checkpoint identity

Public names change presentation only. No checkpoint file was renamed, copied
into this repository, retrained or modified.

| Public policy name | Original policy key / designation | Original checkpoint name | SHA-256 |
|---|---|---|---|
| Pretrained Reference | `model5099` / Model5099 | `model_5099.pt` | `0c6c006ff321f16d720dfe49a1da39b04ac562051cbd0a10a37fffc713abe4a0` |
| Fixed-Mixture Policy | `fixed` / Foundation-02B fixed | `B/fixed/endpoint.pt` | `c6cb76eb173bc834539f7fb07cc9d276b85342205c4025fa3cbb3d53e2da86d9` |
| Adaptive-Frontier Policy | `adaptive` / Foundation-02B adaptive | `B/adaptive/endpoint.pt` | `30c0b4e51b8b7f8e305d77b576d556ecbd940c35de8ea72e3efbdf47a2e3662b` |
| Common initializer (not another evaluated arm) | Shared full model weights, fresh Adam | `B/initialization.pt` | `673eca55abbca593ff9fa0bc40c54d0f1e28c059d0f39b1f8bb3c02dd5e089f2` |

B is the original logical artifact root described in [evidence sources](EVIDENCE_SOURCES.md).
Original `source` CSV columns and logical hash inventories retain original file
keys for traceability. Those are provenance identifiers, not alternative public
policy names. All policy/arm label columns use the public names. Every other
cell, including all numerical strings, is identical to RC1.

The two trained arms share initializer, reward, seed 73 and a 131,072,000-transition
budget each. The Pretrained Reference does not receive that continuation budget;
its contrast is historical and non-causal. The naming change does not create
three matched training arms or additional independent seeds.

Compatible retained implementation: `b77127af5225b3523fc48fbeb88abbe0349d459f`.
Aggregate implementation SHA-256:
`003a9ade6e5e2e34595f5b3233502f07f99f247dc3739efc7323d62ff9efc83a`.
Original training task identity:
`819d059658f61fea1dd3f321debbb78235af442d20c2744a11749fcc18433911`.
Original evaluation task identity:
`118720f99c1bed2d90f258238677c4c7e1402309ecffb63e820461596cf4134c`.

Full historical evidence remains separate and excluded. These exact hashes do
not imply publicly available binaries or certify a complete historical runtime.
