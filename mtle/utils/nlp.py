from __future__ import annotations
from typing import List, Tuple
import spacy
import ginza

def load_jp_nlp():
    nlp = spacy.load("ja_ginza")
    ginza.set_split_mode(nlp, "C")
    return nlp

def extract_anchors(
    nlp: spacy.language.Language,
    text_a: str,
    text_b: str,
) -> Tuple[str, str]:
    """Extract common prefix and suffix from two sentences"""
    
    toks_a: List[str] = [str(t) for t in nlp(text_a)]
    toks_b: List[str] = [str(t) for t in nlp(text_b)]

    # ---- Common prefix (from the start) ----
    prefix_tokens: List[str] = []
    for ta, tb in zip(toks_a, toks_b):
        if ta == tb:
            prefix_tokens.append(ta)
        else:
            break
    prefix = "".join(prefix_tokens)
    if len(prefix) == 1:
        prefix = ""

    # ---- Common suffix (from the end) ----
    suffix_tokens: List[str] = []
    for ta, tb in zip(reversed(toks_a), reversed(toks_b)):
        if ta == tb:
            suffix_tokens.append(ta)
        else:
            break
    suffix_tokens.reverse()
    suffix = "".join(suffix_tokens)
    suffix = suffix.replace("。", "").replace(".", "")
    if len(suffix) == 1:
        suffix = ""

    return prefix, suffix