import re

"""
概要:文字列の成形クラス
"""
# ---------------- クリーン処理関数 ----------------
def clean_text(text: str) -> str:
    # NaN（文字列として現れているもの）を除去
    text = text.replace("NaN", "")

    # 改行・タブ・空白行を正規化
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip() != "" and line.strip().lower() != "nan"]

    # 空じゃない行だけ残して、再度1つの文字列へ
    cleaned_text = "\n".join(cleaned_lines)

    # 連続した空白の正規化（例: "  Go    3年 " → "Go 3年"）
    cleaned_text = re.sub(r"\s{2,}", " ", cleaned_text)

    # 重複する行を削除
    cleaned_text = remove_duplicate_lines(cleaned_text)

    return cleaned_text



def remove_duplicate_lines(text: str) -> str:
    # 行ごとに分割
    lines = text.splitlines()

    # 連続する同じ行が3回以上続く場合、それ以降は削除
    result = []
    last_line = None
    count = 1

    for line in lines:
        # 空行や"NaN"行はスキップ
        if line.strip() == "" or line.strip().lower() == "nan":
            continue

        if line == last_line:
            count += 1
        else:
            count = 1

        # 同じ行が3回続いた場合、それ以降は無視
        if count <= 3:
            result.append(line)

        last_line = line

    return "\n".join(result)

