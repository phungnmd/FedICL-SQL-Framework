# P2.5 GKD cancellation — 2026-09-17

The on-policy GKD lane introduced at nested commits `924ee12` and `0c2ed4c`
was cancelled before publication because autoregressive student rollout plus
online 7B teacher scoring exceeded the available compute budget. Any server
process from that lane must be stopped before pulling replacement code. Its
artifacts are diagnostic only and must not be published as P2.5 evidence.

The replacement active queue is SeqKD versus KID. KID retains online teacher
feedback but approximates imperfect prefixes using a single student mask-fill
pass rather than autoregressive decoding. Git history preserves the superseded
GKD commands and implementation provenance.
