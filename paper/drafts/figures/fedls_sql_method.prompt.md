# FedLS-SQL method figure

Source: `../advisor_report_2026-11-11.md`, Method section.
Generator: built-in imagegen, image edit.
Style reference: architecture figure supplied by the owner in this session.

## Style edit prompt

EDIT THE EXISTING FedLS-SQL METHOD FIGURE USING THE UPLOADED REFERENCE'S VISUAL STYLE.

Two images are supplied. The image headed "Federated Coordination Server (Cloud)" with a "Key Innovations" sidebar is the STYLE REFERENCE ONLY. The image headed "1 Server distillation", "2 Federated SFT", "3 Federated DPO", with a lower inset "Inside each client: execution-guided preference learning", is the EDIT TARGET and the content source. Keep the edit target's method, semantic content and overall upper-overview / lower-client-inset arrangement. Do not transfer any method claims or architecture from the style reference.

STYLE TO MATCH CLOSELY:
White or nearly white canvas, thin crisp deep royal-blue outer borders and rounded-corner panels, compact navy title tabs with white bold text, restrained fine line icons drawn in navy, purple, forest green and orange. Use black readable regular-weight sans-serif body text and small colored bold subheadings. Panel bodies nearly white with extremely faint color tints only, like the reference. Database cylinders, neural-network diagrams, model icons, local-building/computer icons and document icons in the same formal technical line-art language as the reference. Slim arrow shafts and neat triangular arrowheads; color-code blue model broadcasts, purple adapter uploads (dashed), orange local SQL/preference flow, green local processing. A small four-item flow legend can sit in unused whitespace if needed, without displacing method content. Aim for precise journal architecture figure styling, not pastel cartoon cards.
Eliminate the target's thick colored header bands, large numbered circles, heavy rounded cartoon model tiles, chunky black arrows, pale-green neural-network blob motifs and tinted gradient backgrounds. Replace those with the reference's slim, clean, technical panels and smaller refined icons. No glossy lighting, no heavy borders, no shadows, no emojis. Use consistent text sizes and margins.
The top three stages can each use a navy tab with white title; lower inset uses a similar navy tab. Fine purple teacher/model outlines, orange SQL and pair construction outlines, green private client scope, blue server scope. Keep generous enough whitespace so the image is readable inside a paper. Preserve all content details in a high resolution wide landscape image, preferably 3200 by 1600 or larger equivalent aspect ratio. Do not crop text.

EXACT SEMANTIC REQUIREMENTS, from the target's original specification (the OLD pastel-style instructions below are superseded by the reference-style instructions above):
Use case: infographic-diagram.
Asset type: a publication-ready method overview figure for a machine-learning research paper, wide landscape approximately 2:1, high resolution, sharp legible English labels.
Primary request: Illustrate the EXACT three-stage FedLS-SQL method below. Produce a polished academic illustration rather than a generic box-only flowchart. White background, restrained soft pastel blue, mint/teal, pale peach and lavender, thin dark slate outlines, flat vector-like drawings of model blocks, tiny neural-network nodes, database cylinders, document stacks and local client workstations. Clear hierarchy, carefully aligned layout, generous breathing space, consistent sans-serif typography. No gradients, no glossy effects, no shadows, no emojis, no mascot, no decorative illustrations unrelated to the method. The DPO stage is the main visual emphasis.

COMPOSITION: A compact overview band occupies the upper 40 percent, flowing LEFT TO RIGHT through three numbered stages and ending in a small deployment model icon. Beneath it, one larger detailed inset expands ONLY stage 3, occupying the lower 60 percent. Avoid long paragraphs. Distinguish server and private client scopes with pale lightly dashed boundaries. All arrows must have unambiguous direction and never cross text.

UPPER BAND:
Stage 1, pale blue: heading "1  Server distillation". Inside server boundary, a public database cylinder labeled "Public BIRD" supplies prompts to a large frozen teacher icon labeled "Teacher 7B" and a smaller student icon labeled "Student 1.5B + LoRA". A clear teacher-to-student arrow labeled "Logit KD". Footer "2 epochs". Teacher remains confined to this stage.
A single rightward student-model arrow connects to stage 2.
Stage 2, pale mint: heading "2  Federated SFT". Show a server model above FIVE small client icons or model-and-database groups, visually separated, labeled "5 private Spider clients". Bidirectional communication between server and clients denotes broadcast model and upload adapters, with short visible labels "Global model" and "LoRA adapters". Local label "Gold SQL supervision", server label "FedAvg", footer "3 rounds". Do NOT depict private databases being uploaded.
A single rightward model arrow connects to stage 3.
Stage 3, pale peach: heading "3  Federated DPO". Draw an elegant cycle between "Global model", a group of five private client icons and a server aggregator labeled "Pair-weighted FedAvg". Show small pair cards on client side, not server side. Footer "3 rounds". A neat magnification connector drops from this stage into the lower detailed inset.
Final small deployed-model icon to right, heading "Deployment", label "Student 1.5B", with a small "Question + schema" input and "SQL" output. Teacher is not connected to inference.

LOWER INSET:
Heading "Inside each client: execution-guided preference learning".
One wide lightly dashed private-client boundary encloses a clear LEFT TO RIGHT sequence of four illustrated steps. Each step's title is short, with no more than two short supporting lines. Use meaningful document, database and model icons.

A: title "Sample SQL". Incoming arrow from the current global model to local student. Show a question card and a fan of tiny SQL cards. Supporting labels "8 samples / question" and "T = 0.7".
B: title "Execute & label". Show those sample SQL cards executing against a local private database, with a gold SQL result used for comparison. Visually split into three labeled outcomes: "Correct", "Wrong result", "Execution error". A check mark for Correct and simple cross symbols for others are appropriate scientific pictograms.
C: title "Build pairs". Show two horizontally paired cards with green "Chosen" and muted coral "Rejected"; chosen means correct execution result, rejected is either wrong result or execution error. Supporting labels "Most similar correct / wrong SQL" and "At most 2 pairs / question". Below this step in small but readable type, two branch notes: "None correct: gold SQL as chosen" and "All correct: skip". Samples are not reused within a question.
D: title "Local training". Draw local student model, a frozen reference model and paired cards. Equation-like prominent label "L = L_DPO + L_NLL". Supporting labels "beta = 0.1; 2 local epochs" and "Reference: global model at round start". NLL trains on chosen SQL. Arrow exits private boundary carrying ONLY a small adapter block labeled "LoRA adapter".

At right of private inset, outside the client boundary, draw the SERVER aggregator icon labeled "Pair-weighted FedAvg". Adapter upload arrow from local training to server. Return arrow along the bottom from this server to the sampling step labeled "Broadcast updated global model; resample next round". This is a 3-round loop. The reference copy refreshes from the global model at the beginning of every round, not from the teacher.
Within the bottom edge of private client boundary, place a restrained lock/database pictogram and exact label "Data, SQL samples and preference pairs stay local". This is structural data isolation, so do not show differential privacy or cryptographic claims.
Keep the whole drawing visually balanced with large readable text and a coherent pastel academic illustration style. No metrics, plots, reported experimental results, paper title banner, figure number, caption, citations or watermark. No teacher on clients. Do not introduce retrieval, CoT, rewards or GRPO. English labels only.


ADDITIONAL INVARIANTS:
- The picture must show exactly five clients in each federated overview stage.
- The uploaded reference's retrieval, ICL, encrypted uploads, secure aggregation, TLS, differential privacy, schema embeddings, knowledge cache, reasoning and structure losses must NOT appear. Those are NOT part of this method.
- Reference model inside local training is the frozen global model at the round start, not the 7B teacher.
- Public BIRD supplies data for the server student/teacher distillation, not private Spider data.
- Deployed student alone receives question and schema and generates SQL. Depiction must clearly link Question + schema -> Student 1.5B -> SQL within the Deployment panel.
- "Correct" and "Wrong result" labels refer to comparison of execution results to gold; "Execution error" means SQL cannot execute.
- "No sample reuse" may appear as a small label within Build pairs if space allows.
- Keep exact names "FedLS-SQL", "LoRA", "FedAvg", "DPO", "NLL" if used.
FINAL STYLE PRIORITY: emulate the provided technical blue-bordered reference, not the existing soft-pastel figure.

## Reference model clarification edit

Edit only the lower "D. Local training" panel of this FedLS-SQL method illustration. Preserve the entire image's blue-bordered technical academic style, layout, every other panel, all labels, all arrows and all method details.
The purple frozen reference network currently resembles the server's teacher. This causes a serious misunderstanding. The DPO reference is NOT the 7B teacher. It is a frozen copy of the GLOBAL STUDENT 1.5B at the beginning of the round.
Inside "D. Local training", replace the two model icons with two IDENTICAL small green student neural-network model icons, matching the upper deployment student design. Left icon: tiny orange LoRA badge, label exactly "Trainable student" with "1.5B" below. Right icon: same green student network icon, NO snowflake, NO brain, NO teacher symbol, NO 7B, label exactly "Frozen reference" with "Student 1.5B" below. Distinguish frozen status by a small unobtrusive gray "frozen" tag or simple dashed outline only. Keep both models visually the same size and same network structure.
Keep the equation L = L_DPO + L_NLL intact. In the bullets beneath, replace "Reference: global model at round start" with the concise exact phrase "Reference: global student at round start". Preserve beta = 0.1, 2 local epochs, and NLL trains on chosen SQL. Ensure all text fits without overlap or clipping.
The large Teacher 7B in the top-left Server distillation panel stays unchanged. That is the only teacher in the figure.
Do not change anything else. High resolution, all labels readable.
