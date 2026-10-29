# FedLS-SQL method image generation

Source: `paper/results/REPORT_FEDLS-SQL_2026-10-28.pdf`, method section; checked against `paper/notes/RESEARCH_STATE.md` and `paper/notes/DIRECTION_PROPOSAL.md`.

Mode: built-in image_gen. Output: `fedls_sql_method_imagegen_v1.png`.

Status: visual draft. Some arrow endpoints in the client replay bus and per-client adapter paths need refinement before publication.

## Generation prompt

Use case: infographic-diagram.
Create one polished scientific METHOD DIAGRAM for an ML research paper titled "FedLS-SQL". Landscape canvas, approximately 16:9, high resolution, crisp readable English typography, pure white background, flat vector-like academic illustration, thin precise arrows, restrained navy/teal with amber for teacher targets. Generous whitespace. No photorealism, decorative backgrounds, 3D, gradients, shadows, or invented performance claims.

This must faithfully depict the following method. Organize into two clear numbered panels left to right, plus a compact deployment output on the far right. Strong hierarchy; concise labels.

PANEL 1 occupying left third, header "1  Server warm-start", within a pale blue SERVER boundary.
- A public database cylinder labeled "BIRD public data".
- Frozen teacher model block labeled "Qwen2.5-Coder-7B" and small badge "Frozen teacher". A snowflake or padlock icon is optional.
- Student block labeled "Qwen2.5-Coder-1.5B-Instruct" and "Train LoRA".
- Public data feeds the teacher and student. Teacher soft targets feed a small distillation junction leading into student.
- Under that junction write EXACTLY "0.5 gold CE + 0.5 KL" and below "T = 2   |   2 epochs".
- Student output arrow to the global adapter in panel 2 labeled "Warm-start adapter".
- A separate amber branch from teacher targets into a small cache block labeled "Compressed replay cache", with subtitle "Top-50 token probabilities + tail mass". This cache represents precomputed targets on public examples, not the teacher model.
- The cache has a dashed amber arrow to a shared public replay bus feeding ALL displayed clients in panel 2. Label the bus "Public subset + cached targets" and "One-time download: ~33 MB/client". This transmission is separate from per-round adapters.

PANEL 2 occupying central and right majority, header "2  Federated learning with client replay".
- At its upper center a SERVER aggregation box labeled "Sample-weighted FedAvg", with a small global adapter icon labeled "Global LoRA adapter".
- Below it, three evenly spaced client boxes labeled "Client 1", "Client 2", "Client 5", with an ellipsis between Client 2 and Client 5 indicating 5 clients total.
- Every client contains a cylinder "Private Spider", a small amber cache icon "Public replay", and a small student model "1.5B + LoRA". Data stays inside client boxes.
- Under the representative center client, a readable loss callout: "Private SQL CE + public replay KD". Below this, EXACTLY "Replay examples = 0.2 x private examples".
- Draw navy DOWN arrows from global adapter to each client student, label the group "Broadcast adapter". Draw teal UP arrows from each client student back to FedAvg, label "Upload LoRA only". Offset upward and downward paths to prevent overlap; arrowheads must be clear.
- An outer loop arrow around this adapter exchange has a clear badge "3 rounds". Small nearby text "5 non-IID clients".
- Public replay cache bus uses dashed amber arrows to the cache INSIDE each client. The frozen teacher remains only in Panel 1 at the server. Never draw a teacher inside any client.
- Under the client group small label "Private data stays local".

OUTPUT at far right or upper right beyond panel 2, visually connected FROM the final global adapter after the round loop:
"Deploy student only", small model icon "1.5B + LoRA", and a short input-output line "Question + schema → SQL". Ensure deployment is downstream of aggregation, not from the teacher.

Bottom small legend: solid navy/teal arrows "Per-round adapter exchange"; dashed amber arrow "One-time public replay transfer".
Top main title EXACTLY "FedLS-SQL"; small subtitle "Server-side distillation with client-side teacher-target replay".
Do not add accuracy tables, charts, results, ablation arms, extra training stages, ICL, a teacher at clients, private-data uploads, or claims of differential privacy. Keep every text label horizontal and legible. Arrows must stop at actual boxes. Balanced publishable composition.

## Refinement prompt

Edit this FedLS-SQL diagram. Preserve all content, typography, colors, and panel layout. Correct arrow connectivity only, and keep all labels readable.
1. The amber dashed "Public subset + cached targets" line currently wrongly terminates at Sample-weighted FedAvg. Remove that arrowhead into FedAvg. Route it downward to join the amber horizontal replay bus at y approximately 385, below "Broadcast adapter". Its only destinations are the THREE amber public replay cache icons inside Client 1, Client 2, Client 5. This is a one-time cache-to-client transfer, never cache-to-aggregator.
2. The navy "Warm-start adapter" arrow currently ends in blank space near Client 1. Reroute it using a clean right-angle path in available whitespace to connect to the actual LEFT EDGE of the "Sample-weighted FedAvg" server box. It must not stop in blank space. Keep the label next to the path, avoid overlaps.
3. Each of the 3 client student model icons must have TWO distinct connected paths to FedAvg: navy down from FedAvg to student, teal up from student to FedAvg. In particular Client 1 needs a teal upload arrow, which is missing. All paths start/end on the actual student icon or aggregator boundary. Do not connect these arrows to private database icons or public cache icons.
4. The deployment arrow at right must begin at the right edge of the FedAvg box, run to "Deploy student only". Move the "3 rounds" loop badge into nearby whitespace if necessary so the deployment arrow is continuous and directly attached to the aggregator.
Do not change scientific text or add information. Retain the exact label "Top-50 token probabilities + tail mass". Retain all English labels and the white background.

