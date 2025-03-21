import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle

# ✅ โหลดข้อมูล CSV
df = pd.read_csv("thai_movies_and_tv_series_2.csv")

# ✅ กำจัดค่า NaN
df["overview"].fillna("", inplace=True)
df["genres"].fillna("", inplace=True)
df["thai_title"].fillna(df["english_title"], inplace=True)


def load_embeddings():
    embedding_file = "movie_embeddings.pkl"
    try:
        with open(embedding_file, "rb") as f:
            embeddings = pickle.load(f)
        return np.array(embeddings).reshape(len(embeddings), -1)
    except FileNotFoundError:
        print("❌ Error: Embeddings file not found.")
        return None


movie_embeddings = load_embeddings()
if movie_embeddings is None:
    exit()

# ✅ โหลดโมเดล NLP
tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
model = AutoModel.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")


def get_embedding(text):
    prompt = f"ให้คำแนะนำหนังที่ตรงกับคำอธิบายต่อไปนี้: '{text}' โดยคำนึงถึงแนวหนัง เรื่องย่อ และความนิยม"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze(0).numpy()


# ✅ กำหนดหมวดหมู่ของแนวหนัง
genre_keywords = {
    "โรแมนติก": ["รัก", "โรแมนติก", "แฟน", "ความรัก", "อกหัก", "หวาน"],
    "สยองขวัญ": ["ผี", "สยองขวัญ", "น่ากลัว", "หลอน", "ฆาตกรรม", "วิญญาณ"],
    "แอคชั่น": ["บู๊", "แอคชั่น", "ต่อสู้", "ยิง", "ระเบิด"],
    "ตลก": ["ตลก", "ขำ", "ฮา", "สนุก"],
    "ดราม่า": ["ดราม่า", "ชีวิต", "เศร้า", "น้ำตา", "ซึ้ง"],
    "วิทยาศาสตร์": ["ไซไฟ", "วิทยาศาสตร์", "หุ่นยนต์", "อนาคต"],
    "แฟนตาซี": ["เวทมนตร์", "แฟนตาซี", "เทพนิยาย", "อัศวิน"],
    "อาชญากรรม": ["อาชญากรรม", "ตำรวจ", "นักสืบ", "สืบสวน"]
}


def find_movies(genres=None, cast=None, description=None, start_date=None, end_date=None, top_n=5):
    if not any([genres, cast, description, start_date, end_date]):
        print("⚠️ กรุณากรอกข้อมูลอย่างน้อย 1 ช่อง")
        return

    df_filtered = df.copy()

    if genres in genre_keywords:
        df_filtered = df_filtered[df_filtered["genres"].str.contains(genres, case=False, na=False)]
    if cast:
        df_filtered = df_filtered[df_filtered["cast"].str.contains(cast, case=False, na=False)]
    if start_date and end_date:
        df_filtered = df_filtered[
            (df_filtered["release_date"] >= start_date) & (df_filtered["release_date"] <= end_date)]

    if description:
        user_embedding = get_embedding(description).reshape(1, -1)
        df_filtered["similarity"] = cosine_similarity(user_embedding, movie_embeddings[:len(df_filtered)])[0]
        df_filtered = df_filtered.sort_values(by="similarity", ascending=False)

    top_results = df_filtered.head(top_n)

    if top_results.empty:
        print("⚠️ ไม่พบผลลัพธ์ที่ตรงกับคำค้นหา")
        return

    print("🔍 ค้นหาผลลัพธ์ที่แม่นยำที่สุดให้คุณ:")
    for _, row in top_results.iterrows():
        print(f"🔹 {row['thai_title']} ({row['english_title']})")
        print(f"🎭 แนวหนัง: {row['genres']}")
        print(f"📖 เรื่องย่อ: {row['overview'][:500]}...")  # แสดงเรื่องย่อมากขึ้น
        print(f"📅 วันที่ฉาย: {row['release_date']}")
        print(f"⭐ คะแนน: {row.get('rating', 'ไม่ระบุ')}")
        print(f"🖼️ โปสเตอร์: {row['poster_path']}")
        print("---------------------------------")


# ✅ รับ Input จาก UI
print("เลือกแนวหนัง:")
for genre in genre_keywords.keys():
    print(f"- {genre}")
user_genre = input("🎭 แนวหนัง: ")
user_cast = input("🎬 นักแสดง: ")
user_description = input("📖 คำบรรยาย: ")
user_start_date = input("📅 วันที่เริ่มต้น: ") or None
user_end_date = input("📅 วันที่สิ้นสุด: ") or None

find_movies(genres=user_genre, cast=user_cast, description=user_description, start_date=user_start_date,
            end_date=user_end_date)
