# FedLS-SQL method figure

Source: `../advisor_report_2026-11-11.md`, Method section.
Generator: built-in imagegen.

## Prompt

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
