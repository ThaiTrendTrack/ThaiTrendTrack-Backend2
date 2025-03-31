import torch
from transformers import AutoTokenizer, AutoModel
import pandas as pd
import numpy as np
import pickle

# ✅ โหลดข้อมูล CSV
df = pd.read_csv("thai_movies_and_tv_series_2.csv")

# ✅ กำจัด NaN ใน Overview
df["overview"] = df["overview"].fillna("")

# ✅ โหลดโมเดล
tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
model = AutoModel.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")


# ✅ ฟังก์ชันแปลงข้อความเป็น embedding
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze(0).numpy()


# ✅ คำนวณ embeddings ของ overview เท่านั้น
movie_embeddings = np.array([get_embedding(text) for text in df["overview"]])

# ✅ บันทึก embeddings ลงไฟล์
with open("movie_embeddings.pkl", "wb") as f:
    pickle.dump(movie_embeddings, f)

print("✅ Successfully created new movie_embeddings.pkl!")
