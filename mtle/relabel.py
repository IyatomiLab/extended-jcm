import argparse
import re
from tqdm.auto import tqdm

from utils.io_csv import load_csv, save_csv, Checkpointer
from utils.llm import OpenAIClient
from utils.prompts import ANNOTATION_SYSTEM_PROMPT, annotation_user_prompt

def extract_label(text: str) -> str:
    t = text.strip()
    if "1" in t: return "1"
    if "0" in t: return "0"
    return "2"

def relabel_sentence(client: OpenAIClient, sent: str) -> str:
    messages = [
        {"role": "system", "content": ANNOTATION_SYSTEM_PROMPT},
        {"role": "user", "content": annotation_user_prompt(sent)},
    ]
    out = client.chat(messages, max_tokens=10, temperature=0.0).strip()
    m = re.search(r"[012]", out)
    return m.group(0) if m else extract_label(out)

def run_relabel(args: argparse.Namespace) -> None:
    """Relabeling -> Save."""
    df = load_csv(args.input)
    if "llm_sent" not in df.columns:
        raise ValueError(f"Missing required column 'llm_sent' in input CSV.")
    if "llm_label" not in df.columns:
        df["llm_label"] = ""

    client = OpenAIClient(model=args.model, request_timeout=args.timeout)
    ckpt = Checkpointer(args.output, every=args.ckpt_every)

    # Step3: Relabeling
    start = args.start
    total = len(df) - start
    for j, text in tqdm(enumerate(df["llm_sent"].iloc[start:]), total=total, desc="label"):
        i = start + j
        s = str(text).strip()
        if s and s != "none":
            cands = [c.strip() for c in s.split(",") if c.strip()]
            labels = [relabel_sentence(client, c) for c in cands]
            print(labels)
            df.loc[i, "llm_label"] = ",".join(labels)
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
    args = p.parse_args()
    run_relabel(args)

if __name__ == "__main__":
    main()
