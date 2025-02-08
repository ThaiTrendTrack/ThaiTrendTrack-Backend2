# import requests
# import csv
#
# # API Key และ URL
# API_KEY = '33b7e0a891dc3f77534d78102c3d1546'
# BASE_URL = 'https://api.themoviedb.org/3/discover/movie'
#
# # Parameters สำหรับ API
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
# # ฟังก์ชันดึงข้อมูลนักแสดง
# def get_cast(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         cast = response.json().get("cast", [])
#         return ', '.join([actor["name"] for actor in cast[:5]])  # ดึงเฉพาะ 5 คนแรก
#     return "N/A"
#
# # ฟังก์ชันดึงข้อมูลแพลตฟอร์ม
# def get_watch_providers(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         providers = response.json().get("results", {}).get("TH", {}).get("flatrate", [])
#         return ', '.join([provider["provider_name"] for provider in providers]) if providers else "N/A"
#     return "N/A"
#
# # ฟังก์ชันเช็คว่ายังอยู่ในโรงไหม
# def is_now_playing(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json().get("status", "N/A")
#     return "N/A"
#
# # เปิดไฟล์ CSV เพื่อเขียนข้อมูล
# with open('thai_movies_with_details.csv', mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#
#     # เพิ่ม header row
#     writer.writerow([
#         'movie_id', 'thai_title', 'english_title', 'overview', 'release_date', 'popularity',
#         'vote_average', 'vote_count', 'genres', 'poster_path', 'cast', 'watch_platforms', 'status'
#     ])
#
#     # วนลูปเพื่อดึงข้อมูลจากทุกหน้า
#     while True:
#         response = requests.get(BASE_URL, params=params)
#         if response.status_code == 200:
#             data = response.json()
#             movies = data.get('results', [])
#             total_pages = data.get('total_pages', 1)
#
#             # เขียนข้อมูลของแต่ละหนังลงใน CSV
#             for movie in movies:
#                 movie_id = movie.get('id', 'N/A')
#                 title = movie.get('title', 'N/A')
#                 original_title = movie.get('original_title', 'N/A')
#                 overview = movie.get('overview', 'N/A')
#                 release_date = movie.get('release_date', 'N/A')
#                 popularity = movie.get('popularity', 'N/A')
#                 vote_average = movie.get('vote_average', 'N/A')
#                 vote_count = movie.get('vote_count', 'N/A')
#                 poster_path = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
#
#                 # ดึงข้อมูลเพิ่มเติม
#                 cast = get_cast(movie_id)
#                 watch_platforms = get_watch_providers(movie_id)
#                 status = is_now_playing(movie_id)
#
#                 # เพิ่มข้อมูลหนังลงในไฟล์
#                 writer.writerow([
#                     movie_id, title, original_title, overview, release_date, popularity,
#                     vote_average, vote_count, poster_path, cast, watch_platforms, status
#                 ])
#
#             # เช็คว่าถึงหน้าสุดท้ายหรือยัง
#             if params['page'] >= total_pages:
#                 break
#
#             # เพิ่มค่า page เพื่อดึงหน้าถัดไป
#             params['page'] += 1
#         else:
#             print(f"Failed to retrieve data on page {params['page']}: {response.status_code} - {response.text}")
#             break
#
# print('All Thai movies with details have been saved to thai_movies_with_details.csv')


import requests
import csv

# API Key และ URL
API_KEY = '33b7e0a891dc3f77534d78102c3d1546'
BASE_URL = 'https://api.themoviedb.org/3/discover/movie'

# Parameters สำหรับ API
params = {
    'api_key': API_KEY,
    'region': 'TH',
    'language': 'th-TH',
    'sort_by': 'popularity.desc',
    'include_adult': 'false',
    'with_original_language': 'th',
    'page': 1
}


# ฟังก์ชันดึงข้อมูลนักแสดง พร้อมรูปภาพ
def get_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        cast = response.json().get("cast", [])[:5]  # ดึงเฉพาะ 5 คนแรก
        return ', '.join([
            f"{actor['name']} ({'https://image.tmdb.org/t/p/w500' + actor['profile_path'] if actor.get('profile_path') else 'N/A'})"
            for actor in cast
        ])
    return "N/A"


# ฟังก์ชันดึงข้อมูลแพลตฟอร์ม
def get_watch_providers(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        providers = response.json().get("results", {}).get("TH", {}).get("flatrate", [])
        return ', '.join([provider["provider_name"] for provider in providers]) if providers else "N/A"
    return "N/A"


# ฟังก์ชันเช็คว่ายังอยู่ในโรงไหม
def is_now_playing(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("status", "N/A")
    return "N/A"


# เปิดไฟล์ CSV เพื่อเขียนข้อมูล
with open('thai_movies_with_details_and_picture.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # เพิ่ม header row
    writer.writerow([
        'movie_id', 'thai_title', 'english_title', 'overview', 'release_date', 'popularity',
        'vote_average', 'vote_count', 'genres', 'poster_path', 'cast', 'watch_platforms', 'status'
    ])

    # วนลูปเพื่อดึงข้อมูลจากทุกหน้า
    while True:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            movies = data.get('results', [])
            total_pages = data.get('total_pages', 1)

            # เขียนข้อมูลของแต่ละหนังลงใน CSV
            for movie in movies:
                movie_id = movie.get('id', 'N/A')
                title = movie.get('title', 'N/A')
                original_title = movie.get('original_title', 'N/A')
                overview = movie.get('overview', 'N/A')
                release_date = movie.get('release_date', 'N/A')
                popularity = movie.get('popularity', 'N/A')
                vote_average = movie.get('vote_average', 'N/A')
                vote_count = movie.get('vote_count', 'N/A')
                poster_path = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"

                # ดึงข้อมูลเพิ่มเติม
                cast_data = get_cast(movie_id)
                watch_platforms = get_watch_providers(movie_id)
                status = is_now_playing(movie_id)

                # เพิ่มข้อมูลหนังลงในไฟล์
                writer.writerow([
                    movie_id, title, original_title, overview, release_date, popularity,
                    vote_average, vote_count, poster_path, cast_data, watch_platforms, status
                ])

            # เช็คว่าถึงหน้าสุดท้ายหรือยัง
            if params['page'] >= total_pages:
                break

            # เพิ่มค่า page เพื่อดึงหน้าถัดไป
            params['page'] += 1
        else:
            print(f"Failed to retrieve data on page {params['page']}: {response.status_code} - {response.text}")
            break

print('All Thai movies with details have been saved to thai_movies_with_details.csv')
