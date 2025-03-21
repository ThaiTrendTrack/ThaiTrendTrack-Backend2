import torch
from transformers import AutoTokenizer, AutoModel
import pandas as pd
import numpy as np
import pickle
import os
from deep_translator import GoogleTranslator
from difflib import get_close_matches

# ✅ โหลดข้อมูล CSV
df = pd.read_csv("thai_movies_and_tv_series_2.csv")

# ✅ กำจัด NaN ใน Overview และ Cast
df["overview"] = df["overview"].fillna("")
df["cast"] = df["cast"].fillna("")

# ✅ โหลดโมเดล
print("🔄 Loading model...")
tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
model = AutoModel.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")


# ✅ ฟังก์ชันแปลงข้อความเป็น embedding
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze(0).numpy()


# ✅ คำนวณ embeddings ของ overview เท่านั้น
if "movie_embeddings.pkl" not in os.listdir():
    print("🔄 Generating movie embeddings...")
    movie_embeddings = np.array([get_embedding(text) for text in df["overview"]])
    with open("movie_embeddings.pkl", "wb") as f:
        pickle.dump(movie_embeddings, f)
    print("✅ Successfully created movie_embeddings.pkl!")
else:
    print("✅ movie_embeddings.pkl already exists.")


# ✅ ฟังก์ชันค้นหาภาพยนตร์หรือซีรีส์จากชื่อนักแสดง (เปลี่ยนมาใช้ deep_translator)
def translate_text(text):
    translated = GoogleTranslator(source='auto', target='en').translate(text)
    return translated if translated else text  # ป้องกันกรณีไม่มีผลลัพธ์จากการแปล


def find_movies_by_actor(actor_name):
    translated_name = translate_text(actor_name)
    print(f"🔍 Searching for movies with actor: {translated_name} ({actor_name})")

    # ค้นหาตรงตัวก่อน
    results = df[df["cast"].str.contains(translated_name, case=False, na=False)]

    # ถ้าไม่พบ ให้ลองค้นหาชื่อที่คล้ายกัน
    if results.empty:
        all_actors = set(
            name.strip() for sublist in df["cast"].dropna().str.split(",") for name in sublist
        )
        similar_names = get_close_matches(translated_name, all_actors, n=5, cutoff=0.5)

        if similar_names:
            print(f"🔍 No exact match found. Searching for similar names: {', '.join(similar_names)}")
            results = df[df["cast"].apply(lambda x: any(sim_name in x for sim_name in similar_names))]

    if results.empty:
        print(f"❌ No movies or TV series found for actor: {translated_name} ({actor_name})")
    else:
        print(f"🎬 Movies and TV series featuring {translated_name} ({actor_name}):")
        print(results[["thai_title", "overview"]])


# 🔍 ทดสอบค้นหานักแสดง
if __name__ == "__main__":
    actor_name = input("Enter actor name: ")
    find_movies_by_actor(actor_name)
