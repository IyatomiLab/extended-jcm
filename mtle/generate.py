import argparse
import os
import re
from typing import List
from tqdm.auto import tqdm

from utils.io_csv import load_csv, save_csv, Checkpointer
from utils.llm import OpenAIClient
from utils.prompts import generation_user_prompt
from utils.nlp import load_jp_nlp, extract_anchors

def generate_six_sentences(client: OpenAIClient, mask_sent: str, locate: str) -> str:
    """Generate six sentences using the LLM based on the provided template."""
    messages = [{"role": "user", "content": generation_user_prompt(mask_sent, locate)}]
    return client.chat(messages, max_tokens=800, temperature=0.5)

def fix_candidates_by_anchor(top: str, bottom: str, raw: str) -> str:
    """Normalize comma-separated generations using known prefix/suffix anchors."""
    s = raw.replace("\n", ",").replace("<", "").replace(">", "")
    cands = [c.strip() for c in s.split(",") if c.strip()]
    out: List[str] = []
    if top:
        for cand in cands:
            parts = re.split(re.escape(top) + r"+", cand)
            if len(parts) >= 2:
                rebuilt = (top + parts[-1].strip()).rstrip("、").replace(", ", "")
                out.append(rebuilt)
    elif bottom:
        for cand in cands:
            parts = re.split(re.escape(bottom) + r"+", cand)
            if len(parts) >= 2:
                rebuilt = (parts[0].strip() + bottom).rstrip("、").replace(", ", "")
                out.append(rebuilt)
    else:
        out = cands
    return ",".join(out)


def run_generate(args: argparse.Namespace) -> None:
    """Mask Creation -> Sentence Generation -> Save."""
    df = load_csv(args.input)
    for col in ("label", "sent"):
        if col not in df.columns:
            raise ValueError(f"Missing required column '{col}' in input CSV.")
    df = df[['sent','label']]
    if "mask_sent" not in df.columns:
        df["mask_sent"] = ""
    if "llm_sent" not in df.columns:
        df["llm_sent"] = ""

    nlp = load_jp_nlp()
    client = OpenAIClient(model=args.model, request_timeout=args.timeout)
    ckpt = Checkpointer(args.output, every=args.ckpt_every)

    n = len(df)
    for i in tqdm(range(args.start, n), desc="expand"):
        if i + 1 >= n:
            df.loc[i, "llm_sent"] = "none"
            continue

        # Step1: Mask Creation
        sent = str(df.loc[i, "sent"])
        sent_next = str(df.loc[i + 1, "sent"])

        top, bottom = extract_anchors(nlp, sent, sent_next)
        mask_sent = (top or "") + "<>" + (bottom or "")
        if len(mask_sent) < 6:
            df.loc[i, "llm_sent"] = "none"
            continue
        df.loc[i, "mask_sent"] = mask_sent
        locate = "before" if top else "after"

        # Step2: Sentence Generation
        success = False
        for _ in range(args.retries):
            raw = generate_six_sentences(client, mask_sent, locate)
            fixed = fix_candidates_by_anchor(top, bottom, raw)
            cands = [c.strip() for c in fixed.split(",") if c.strip()]
            if len(cands) == 6:
                df.loc[i, "llm_sent"] = ", ".join(cands)
                success = True
                break
        if not success:
            df.loc[i, "llm_sent"] = "none"

        ckpt.step(df)

    save_csv(df, args.output)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--model", type=str, default="gpt-4o-mini")
    p.add_argument("--timeout", type=int, default=30)
    p.add_argument("--ckpt-every", type=int, default=20)
    p.add_argument("--retries", type=int, default=3)
    args = p.parse_args()
    run_generate(args)

if __name__ == "__main__":
    main()
