"""Sample 10 SQL per question from the pretrained model for a few short Spider train
questions of client 1 (alpha_0.1/k5), label by execution with the repo's evaluator.
Run from fedicl-sql root: uv run python <this file> out.jsonl"""
import json
import sys

from fedls_sql.data.spider import load_csv
from fedls_sql.eval import sql_pool
from fedls_sql.models.student import StudentModel
from fedls_sql.preference.sampling import label_question
from fedls_sql.training.dataset import zero_shot_prompt

CSV = "processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5/client_1_train.csv"
rows = load_csv(CSV)
short = [r for r in rows if len(r.query) <= 75 and len(r.question) <= 60
         and any(k in r.query.upper() for k in ("JOIN", "GROUP BY", "ORDER BY"))]
print(len(rows), "rows,", len(short), "short candidates")
pick = short[:: max(1, len(short) // 16)][:16]
model = StudentModel("Qwen/Qwen2.5-Coder-1.5B-Instruct", repetition_penalty=1.0)
out = open(sys.argv[1], "w")
with sql_pool.use(2):
    for i, ex in enumerate(pick):
        prompt = zero_shot_prompt(ex, schema_style="ddl_rows", evidence_mode="none")
        [drawn] = model.sample_batch([prompt], 10, temperature=1.0, top_p=1.0,
                                     max_new_tokens=256, seed=i)
        rec = label_question(ex, drawn, evaluator="spider")
        outs = [s["outcome"] for s in rec["samples"]]
        print(i, ex.source_row_id, ex.question, "|", {o: outs.count(o) for o in set(outs)}, flush=True)
        out.write(json.dumps(rec) + "\n")
        out.flush()
