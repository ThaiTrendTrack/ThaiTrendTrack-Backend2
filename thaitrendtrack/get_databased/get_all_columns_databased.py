# import requests
# import csv
# import concurrent.futures  # ✅ Faster API calls
#
# # API Key and Base URLs
# API_KEY = '33b7e0a891dc3f77534d78102c3d1546'
# MOVIE_URL = 'https://api.themoviedb.org/3/discover/movie'
# TV_URL = 'https://api.themoviedb.org/3/discover/tv'
#
# params = {
#     'api_key': API_KEY,
#     'region': 'TH',
#     'language': 'th-TH',
#     'sort_by': 'popularity.desc',
#     'include_adult': 'false',
#     'with_original_language': 'th',
#     'page': 1
# }
#
# # ✅ Use `requests.Session()` for speed optimization
# session = requests.Session()
#
#
# # ✅ Function to get streaming platforms in a simple format
# def get_watch_providers(content_id, content_type):
#     url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers?api_key={API_KEY}"
#     response = session.get(url)
#     if response.status_code == 200:
#         provider_data = response.json().get("results", {})
#         platforms = set()  # ✅ Use a set to keep unique providers
#
#         for country, data in provider_data.items():
#             providers = data.get("flatrate", [])  # Streaming platforms
#             streaming = ', '.join([provider["provider_name"] for provider in providers]) if providers else "N/A"
#             if streaming != "N/A":
#                 platforms.add(f"{country}: {streaming}")  # ✅ Store in set format
#
#         return "; ".join(sorted(platforms)) if platforms else "N/A"  # ✅ Convert set to readable string
#     return "N/A"
#
#
# # ✅ Function to get movie/TV details (genres + status)
# def get_details(content_id, content_type):
#     url = f"https://api.themoviedb.org/3/{content_type}/{content_id}?api_key={API_KEY}&language=th-TH"
#     response = session.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         genres = ", ".join([genre["name"] for genre in data.get("genres", [])])
#         status = data.get("status", "N/A")  # "Released", "In Production"
#         return genres, status
#     return "N/A", "N/A"
#
#
# # ✅ Function to get correct English title
# def get_english_title(content_id, content_type):
#     url = f"https://api.themoviedb.org/3/{content_type}/{content_id}?api_key={API_KEY}&language=en-US"
#     response = session.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("title" if content_type == "movie" else "name", "N/A")
#     return "N/A"
#
#
# # ✅ Function to get top 5 cast (with images)
# def get_cast(content_id, content_type):
#     url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/credits?api_key={API_KEY}"
#     response = session.get(url)
#     if response.status_code == 200:
#         cast = response.json().get("cast", [])[:5]  # Only top 5 actors
#         return ', '.join([
#             f"{actor['name']} ({'https://image.tmdb.org/t/p/w500' + actor['profile_path'] if actor.get('profile_path') else 'N/A'})"
#             for actor in cast
#         ])
#     return "N/A"
#
#
# # ✅ Function to fetch content details
# def fetch_content_details(content, content_type):
#     content_id = content.get('id', 'N/A')
#     title = content.get('name' if content_type == 'tv' else 'title', 'N/A')
#     original_title = content.get('original_name' if content_type == 'tv' else 'original_title', 'N/A')
#
#     # ✅ Get additional details using multithreading
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         english_title_future = executor.submit(get_english_title, content_id, content_type)
#         genres_status_future = executor.submit(get_details, content_id, content_type)
#         cast_future = executor.submit(get_cast, content_id, content_type)
#         watch_platforms_future = executor.submit(get_watch_providers, content_id, content_type)
#
#         english_title = english_title_future.result()
#         genres, status = genres_status_future.result()
#         cast_data = cast_future.result()
#         watch_platforms = watch_platforms_future.result()
#
#     # ✅ Fetch release date
#     release_date = content.get('first_air_date' if content_type == 'tv' else 'release_date', 'N/A')
#
#     # ✅ Fetch poster image
#     poster_path = content.get('poster_path', '')
#     poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300"
#
#     return [
#         content_id, title, english_title, original_title, genres, status,
#         release_date, poster_url,  # ✅ Keep all fields
#         cast_data, watch_platforms, "Movie" if content_type == "movie" else "TV Series"
#     ]
#
#
# # ✅ Open CSV file for writing
# with open('thai_movies_and_tv_series.csv', mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#
#     # ✅ Restore full header row
#     writer.writerow([
#         'id', 'thai_title', 'english_title', 'original_title', 'genres', 'status',
#         'release_date', 'poster_path', 'cast', 'watch_platforms', 'content_type'
#     ])
#
#
#     def fetch_content(content_url, content_type):
#         params["page"] = 1
#         while True:
#             response = session.get(content_url, params=params)
#             if response.status_code == 200:
#                 data = response.json()
#                 contents = data.get('results', [])
#                 total_pages = data.get('total_pages', 1)
#
#                 with concurrent.futures.ThreadPoolExecutor() as executor:
#                     results = list(executor.map(lambda c: fetch_content_details(c, content_type), contents))
#
#                 writer.writerows(results)
#
#                 if params["page"] >= total_pages:
#                     break
#                 params["page"] += 1
#             else:
#                 print(f"Failed on page {params['page']} ({content_type}): {response.status_code}")
#                 break
#
#
#     fetch_content(MOVIE_URL, "movie")
#     fetch_content(TV_URL, "tv")
#
# print('✅ All movies & TV series saved to thai_movies_and_tv_series.csv')

import requests
import csv
import concurrent.futures  # ✅ Faster API calls

# API Key and Base URLs
API_KEY = '33b7e0a891dc3f77534d78102c3d1546'
MOVIE_URL = 'https://api.themoviedb.org/3/discover/movie'
TV_URL = 'https://api.themoviedb.org/3/discover/tv'

params = {
    'api_key': API_KEY,
    'region': 'TH',
    'language': 'th-TH',
    'sort_by': 'popularity.desc',
    'include_adult': 'false',
    'with_original_language': 'th',
    'page': 1
}

# ✅ ใช้ requests.Session() เพื่อเร่งความเร็ว
session = requests.Session()


# ✅ ฟังก์ชันดึงแพลตฟอร์มสตรีมมิ่ง
def get_watch_providers(content_id, content_type):
    url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers?api_key={API_KEY}"
    response = session.get(url)
    if response.status_code == 200:
        provider_data = response.json().get("results", {})
        platforms = set()

        for country, data in provider_data.items():
            providers = data.get("flatrate", [])  # Streaming platforms
            streaming = ', '.join([provider["provider_name"] for provider in providers]) if providers else "N/A"
            if streaming != "N/A":
                platforms.add(f"{country}: {streaming}")

        return "; ".join(sorted(platforms)) if platforms else "N/A"
    return "N/A"


# ✅ ฟังก์ชันดึงข้อมูล (แนวภาพยนตร์ + สถานะ + เรื่องย่อ)
def get_details(content_id, content_type):
    url = f"https://api.themoviedb.org/3/{content_type}/{content_id}?api_key={API_KEY}&language=th-TH"
    response = session.get(url)
    if response.status_code == 200:
        data = response.json()
        genres = ", ".join([genre["name"] for genre in data.get("genres", [])])
        status = data.get("status", "N/A")  # "Released", "In Production"
        overview = data.get("overview", "N/A")  # ✅ เอาเรื่องย่อมา
        return genres, status, overview
    return "N/A", "N/A", "N/A"


# ✅ ฟังก์ชันดึงชื่อภาษาอังกฤษที่ถูกต้อง
def get_english_title(content_id, content_type):
    url = f"https://api.themoviedb.org/3/{content_type}/{content_id}?api_key={API_KEY}&language=en-US"
    response = session.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("title" if content_type == "movie" else "name", "N/A")
    return "N/A"


# ✅ ฟังก์ชันดึงนักแสดงนำ 5 คน (พร้อมรูป)
def get_cast(content_id, content_type):
    url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/credits?api_key={API_KEY}"
    response = session.get(url)
    if response.status_code == 200:
        cast = response.json().get("cast", [])[:5]  # ดึงมาแค่ 5 คนแรก
        return ', '.join([
            f"{actor['name']} ({'https://image.tmdb.org/t/p/w500' + actor['profile_path'] if actor.get('profile_path') else 'N/A'})"
            for actor in cast
        ])
    return "N/A"


# ✅ ฟังก์ชันดึงรายละเอียดทั้งหมดของภาพยนตร์ / ซีรีส์
def fetch_content_details(content, content_type):
    content_id = content.get('id', 'N/A')
    title = content.get('name' if content_type == 'tv' else 'title', 'N/A')
    original_title = content.get('original_name' if content_type == 'tv' else 'original_title', 'N/A')

    # ✅ ดึงข้อมูลแบบ Multi-threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        english_title_future = executor.submit(get_english_title, content_id, content_type)
        genres_status_overview_future = executor.submit(get_details, content_id, content_type)
        cast_future = executor.submit(get_cast, content_id, content_type)
        watch_platforms_future = executor.submit(get_watch_providers, content_id, content_type)

        english_title = english_title_future.result()
        genres, status, overview = genres_status_overview_future.result()
        cast_data = cast_future.result()
        watch_platforms = watch_platforms_future.result()

    # ✅ ดึงวันที่ออกฉาย
    release_date = content.get('first_air_date' if content_type == 'tv' else 'release_date', 'N/A')

    # ✅ ดึงโปสเตอร์ภาพยนตร์
    poster_path = content.get('poster_path', '')
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300"

    return [
        content_id, title, english_title, original_title, genres, status,
        release_date, poster_url, overview,  # ✅ เก็บเฉพาะเรื่องย่อ ไม่มีรีวิว
        cast_data, watch_platforms, "Movie" if content_type == "movie" else "TV Series"
    ]


# ✅ สร้างไฟล์ CSV และเขียนข้อมูล
with open('thai_movies_and_tv_series_2.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # ✅ กำหนด Header ของ CSV (ไม่มีรีวิว)
    writer.writerow([
        'id', 'thai_title', 'english_title', 'original_title', 'genres', 'status',
        'release_date', 'poster_path', 'overview', 'cast', 'watch_platforms', 'content_type'
    ])


    def fetch_content(content_url, content_type):
        params["page"] = 1
        while True:
            response = session.get(content_url, params=params)
            if response.status_code == 200:
                data = response.json()
                contents = data.get('results', [])
                total_pages = data.get('total_pages', 1)

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = list(executor.map(lambda c: fetch_content_details(c, content_type), contents))

                writer.writerows(results)

                if params["page"] >= total_pages:
                    break
                params["page"] += 1
            else:
                print(f"Failed on page {params['page']} ({content_type}): {response.status_code}")
                break


    fetch_content(MOVIE_URL, "movie")
    fetch_content(TV_URL, "tv")

print('✅ All movies & TV series saved to thai_movies_and_tv_series.csv')
