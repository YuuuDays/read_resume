import gradio as gr
from openai import OpenAI
import PyPDF2
import pandas as pd
import os
from dotenv import load_dotenv
from utils.string_shaping import clean_text

# --- 環境変数ロードとOpenAIクライアント初期化 ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- ファイルからテキスト抽出 ---
def extract_text_from_file(file) -> str:
    print(f"[extract_text_from_file] type: {type(file)}")
    file_name = file.name

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file_name.endswith(".xlsx"):
        return extract_text_from_excel(file)
    else:
        return "対応しているのはPDFと.xlsxのみです"

def extract_text_from_pdf(file) -> str:
    reader = PyPDF2.PdfReader(file)
    return "".join(page.extract_text() for page in reader.pages)

def extract_text_from_excel(file) -> str:
    df = pd.read_excel(file)
    return df.to_string(index=False)

# --- ChatGPT用プロンプトの作成 ---
def create_prompt(cleaned_text: str) -> str:
    return f"以下の履歴書の内容を読み込んで、記載されているプログラミング言語とその使用年数だけを全て抽出して、簡潔にまとめてください。：\n\n{cleaned_text}"

# --- ChatGPTへ問い合わせ ---
def get_analysis_from_openai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt4.0",
        messages=[
            {"role": "system", "content": "貴方は履歴書を見て欲しい人材を判断する人事担当者です"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    return response.choices[0].message.content.strip()

# --- メインの分析関数 ---
def analyze_resume(file) -> str:
    print(f"[analyze_resume] file type: {type(file)}")
    raw_text = extract_text_from_file(file)

    if raw_text == "対応しているのはPDFと.xlsxのみです":
        print("[WARN] 対応外ファイル")
        return raw_text

    cleaned_text = clean_text(raw_text)
    print("========== 抽出されたテキスト ==========")
    print(raw_text)
    print("========== 成形されたテキスト ==========")
    print(cleaned_text)

    prompt = create_prompt(cleaned_text)
    result = get_analysis_from_openai(prompt)

    print("============================")
    print(f"成形前: {len(raw_text)}文字, 成形後: {len(cleaned_text)}文字")
    print("============================")

    return result

# --- Gradioインターフェース構築 ---
def create_interface():
    return gr.Interface(
        fn=analyze_resume,
        inputs=gr.File(label="履歴書をアップロード(PDFまたはExcel)"),
        outputs="text",
        title="履歴書解析AI",
        description="PDF(.pdf)またはExcel(.xlsx)形式の技術履歴書をアップロードすると、記載されているプログラミング言語とその使用年数だけを全て抽出してAIが自動で要約する"
    )

if __name__ == "__main__":
    iface = create_interface()
    iface.launch(share=True)
