from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import requests
import random
import json
from datetime import datetime
import demjson3 as demjson
import re
import uuid
import os

app = FastAPI(title="TOEIC Part 2 Generator API")

# -----------------------------
# 配置
# -----------------------------
CHROMA_PATH = "/app/chroma_db"
JSONL_PATH = "/app/json/toeic_part4_db_ready.jsonl"
OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_collection("toeic_part3")
scenario_collection = chroma_client.get_collection("toeic_scenarios")

scenario_keywords = [
    "企業發展", "外食", "娛樂", "金融／預算", "一般商務", "保健", "房屋／公司地產",
    "製造業", "辦公室", "人事", "採購", "技術層面", "旅遊"
]

# -----------------------------
# Pydantic 請求模型
# -----------------------------
class GenerateRequest(BaseModel):
    scenario: str = None  # 可選，若未提供則隨機選擇

# -----------------------------
# 工具函數
# -----------------------------
def clean_text(text: str) -> str:
    """清理控制字元，保留 \\n"""
    text = re.sub(r'[\x00-\x09\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text.replace('\n', '\\n')

def generate_uuid() -> str:
    return str(uuid.uuid4())

# -----------------------------
# FastAPI 路由
# -----------------------------
@app.post("/generate_part4")
def generate_part2(req: GenerateRequest):
    # 選擇情境
    scenario_text = req.scenario or random.choice(scenario_keywords)

    # 查詢語意相似題目
    query_embedding = embedding_model.encode("Part 4 TOEIC, you can hear some talks given by a single speaker with 3 question.").tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=2)
    similar_questions = results["documents"][0] if results["documents"] else []

    scenario_embedding = embedding_model.encode(scenario_text).tolist()
    scenario_results = scenario_collection.query(query_embeddings=[scenario_embedding], n_results=1)
    scenario_context = scenario_results["documents"][0][0] if scenario_results["documents"] else scenario_text

    context = "\n\n".join(similar_questions)

    # 🔧 prompt
    prompt = f"""
你是一位專業 TOEIC 出題專家。請根據下列測驗情境與範例題目，生成一組新的 TOEIC Part 4 聽力題組，包含：

1. 一筆 listening_material（不含 ID）
2. 三筆 question（不含 ID 與 material_id）
內容必須全為英文。
常見的場景有這些:
· 圖書館/博物館/美術館介紹
· 公司政策宣布、會議簡報
· 表演開演前廣播
· 火車、公車上廣播
· 答錄機留言
· 演說
· 收音機裡的銀行、電力公司…等廣告
· 天氣預報
主要請以上面的場景為主要生成場景
輸出 JSON 格式如下（不要有說明、標題、Markdown）:
{{
  "listening_material": {{
    "audio_url": "音檔 先留空",
    "transcript": "單人獨白，對話稿開頭一定要有Questions 1 through 3. Refer to the following talk/ announcement/ telephone message... .直接接對話稿（\\n 表示換行）",
    "accent": "口音 先留空",
    "topic": "{scenario_text}",
    "speaker_count": "1",
    "listening_level": "難度(beginner,intermediate,advanced)",
    "created_at": "{datetime.now().isoformat()}",
    "updated_at": "{datetime.now().isoformat()}",
    "is_approved": "0",
    "rejection_reason": "先留空"
  }},
  "questions": [
    {{
      "question_text": "問題內容",
      "question_type": "listen",
      "question_category": "題目種類(tense,pos,syntax,vocab)tense時態, pos詞性, syntax語法, vocab詞彙",
      "passage_id": null,
      "question_image_url": null,
      "part"= "4",
      "option_a_text": "選項 A",
      "option_b_text": "選項 B",
      "option_c_text": "選項 C",
      "option_d_text": "選項 D",
      "is_correct": "正確解答(A, B, C, D)",
      "difficulty_level": "難度(1,2,3,4,5)數字越大越難",
      "explanation": "題目解析",
      "created_at": "{datetime.now().isoformat()}",
      "updated_at": "{datetime.now().isoformat()}"
    }}
  ]
}}

### 測驗情境：
{scenario_context}

### 範例題目（供風格參考）：
{context}

請確保輸出為合法的 JSON 陣列格式：
- 所有字串必須用雙引號包住
- 不可省略逗號
- `\n` 必須轉為字串表示（\\n），不可出現真正的換行
請直接輸出純 JSON 陣列，**不要有任何說明文字、標題、註解或 Markdown 格式。**
"""

    # 🔄 發送到本地 LLM
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={"model": "llama3", "prompt": prompt, "stream": False}
        )
        raw_output = response.json()["response"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM 生成錯誤: {e}")

    # 清理 & 解析 JSON
    cleaned_output = clean_text(raw_output)
    try:
        data = json.loads(cleaned_output)
    except json.JSONDecodeError:
        data = demjson.decode(cleaned_output)

    # 生成 UUID
    material_id = generate_uuid()
    data["toeic_listeningmaterial"]["material_id"] = material_id
    for q in data["questions"]:
        q["question_id"] = generate_uuid()
        q["material_id"] = material_id

    # 儲存 JSONL
    os.makedirs(os.path.dirname(JSONL_PATH), exist_ok=True)
    with open(JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    return {"data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_part4:app", host="0.0.0.0", port=11430, reload=True, log_level="debug")