import gradio as gr
from openai import OpenAI
import PyPDF2
import pandas as pd
import io, os, re
from dotenv import load_dotenv
import numpy as np
from itertools import groupby
from utils.string_shaping import clean_text


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------------------------------

def analyze_resume(file):
    resume_text = extract_text_from_file(file)
    # クリーン処理を追加
    cleaned_text = clean_text(resume_text)
    print("========== 抽出されたテキスト ==========")
    print(resume_text)  # 成形前36万7000行
    print("========== 成形されたテキスト ==========")
    print(cleaned_text)  # 成形後6000行　→(重複3行)4020行

    # ChatGPTに投げる
    # (モデルの 振る舞い・前提・役割 を定義する（性格、専門性など）)
    prompt = f"以下の履歴書の内容を読み込んで、記載されているプログラミング言語とその使用年数だけを全て抽出して、簡潔にまとめてください。：\n\n{cleaned_text}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "貴方は履歴書を見て欲しい人材を判断する人事担当者です"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    """
    入力：3000トークン × $0.0005 = $0.0015
    出力：1000トークン × $0.0015 = $0.0015
    合計：$0.0015 + $0.0015 = $0.003（≒0.45円）

    100回	    約 45円
    500回	    約 225円
    1,000回	    約 450円
    10,000回	約 4,500円
    """

    return response.choices[0].message.content.strip()


# 概要:対象ファイルの拡張子判断
def extract_text_from_file(file):
    file_name = file.name

    # PDF
    if file_name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    # Excelの場合(.xlsx)
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(file)
        return df.to_string(index=False)

    # その他
    else:
        return "対応しているのはPDFと.xlsxのみです"


# Gradioインターフェイス
iface = gr.Interface(
    fn=analyze_resume,
    inputs=gr.File(label="履歴書をアップロード(PDFまたはExcel)"),
    outputs="text",
    title="履歴書解析AI",
    description="PDFまたはExcel 形式の履歴書をアップロードすると内容をAIが自動で要約する"
)

iface.launch()
