# Public terminal-label aggregation

The new implementation was written from the published table schema and report
aggregation definitions. The retained original audit was inspected to verify the
numeric terminal-code dictionary and grouping semantics; its implementation was
not imported, copied or distributed. No private traversal algorithm is rebuilt.

| Stored code | Meaning used by this reducer |
|---|---|
| outcome 1 / reason 10 | Detector-defined completion |
| outcome 2 | Hard failure |
| outcome 6 / reason 13 | Obstacle timeout |
| outcome 7 / reason 14 | Ordinary retention horizon; not climbing completion |
| reasons 6 / 7 / 8 / 9 / 11 / 15 | Fall / collision / corridor-or-tile / wrong-way / stuck / native termination |

Unknown, active, censored and invalid categories are rejected, not dropped.
A completion must also retain `attempted=True`, `hind_complete=True`, payout 1
and at least 0.30 s dwell within the report's 1e-6 summary comparison precision.
This is internal label consistency, not independent validation of contact support.

Each of three policies, three suites and two evaluation seeds must contain exactly
384 distinct first-episode environment IDs (0–383). Task ID is environment ID
modulo 24. The CSV has 6,912 records; no restart episodes are added. The source
column is retained historical provenance, not an executable file dependency.

Cohorts: all records; exact fixture; fixture family; isolated/staircase height
(10, 13, 16, 18 cm); explicit isolated/staircase 16/18 cm frontier; both descent
families; and ordinary direction from the signed command. Native fixtures are
excluded from the explicit high cohort. The pretrained reference is historical,
not a third equal-budget continuation arm.

Counts sum terminal labels. Tracking, effort and smoothness are arithmetic means
of the episode summaries, with each episode weighted equally. Axis means use
`tracking_axes` in vx, vy, yaw-rate order. Neither duration weighting nor imagined
contact events are introduced. The seed table uses only the four frontier fixtures.
The high-failure table has only the published reason columns and fails explicitly
if a new high-task hard-failure reason cannot be represented.

All 639 published summary rows can be reconstructed. Original source strings and
training exposure/history tables are not regenerated from episode labels: the
latter need training logs not present here. Reproducing a terminal label from
physical contacts would need trajectories, per-foot support signals and the
original detector; that is outside this public analysis.
