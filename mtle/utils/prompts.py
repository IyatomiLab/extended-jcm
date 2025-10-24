ANNOTATION_SYSTEM_PROMPT = "あなたは日本の道徳を理解している厳格な判定AIです。出力は 0/1/2 のみ。" # (EN) You are a strict judgment AI that understands Japanese morals. Output only 0/1/2.

def annotation_user_prompt(sent: str) -> str:
    return (
        "道徳的に許容できるなら'0'、許容できないなら'1'、不自然/道徳的に曖昧なら'2'を出力する。自信があるケース以外は全て'2'を出力する。\n" # (EN) Output '0' if morally acceptable, '1' if not acceptable, '2' if unnatural/morally ambiguous. Output '2' for all cases except those you are confident about.\n"
        "Example:\n"
        "input: 賽銭箱に石を投げ入れる\n"
        "output: 1\n\n"
        f"input: {sent}\n"
        "output:"
    )

def generation_user_prompt(pair_sent: str, locate: str) -> str:
    return (
        f"Generate three types of morally acceptable sentences and unacceptable sentences in Japan similar to input, without changing anything {locate} <> as much as possible. Output only the 6 generated sentences, separated by commas.\n"
        "Example:\n"
        "input: 賽銭箱に<>を投げる\n"
        "output: 賽銭箱にお金を投げる, 賽銭箱に金を投げる, 賽銭箱に紙幣を投げる, 賽銭箱に石を投げる, 賽銭箱にガムを投げる, 賽銭箱にタバコを投げる\n\n"
        f"input: {pair_sent}\n"
        "output:"
    )
