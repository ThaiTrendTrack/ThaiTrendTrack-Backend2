# # import requests
# # import csv
# #
# # # API Key และ URL
# # API_KEY = '33b7e0a891dc3f77534d78102c3d1546'
# # BASE_URL = 'https://api.themoviedb.org/3/discover/movie'
# #
# # # Parameters สำหรับ API
# # params = {
# #     'api_key': API_KEY,
# #     'region': 'TH',
# #     'language': 'th-TH',
# #     'sort_by': 'popularity.desc',
# #     'include_adult': 'false',
# #     'with_original_language': 'th',
# #     'page': 1
# # }
# #
# # # ฟังก์ชันดึงข้อมูลนักแสดง
# # def get_cast(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         cast = response.json().get("cast", [])
# #         return ', '.join([actor["name"] for actor in cast[:5]])  # ดึงเฉพาะ 5 คนแรก
# #     return "N/A"
# #
# # # ฟังก์ชันดึงข้อมูลแพลตฟอร์ม
# # def get_watch_providers(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         providers = response.json().get("results", {}).get("TH", {}).get("flatrate", [])
# #         return ', '.join([provider["provider_name"] for provider in providers]) if providers else "N/A"
# #     return "N/A"
# #
# # # ฟังก์ชันเช็คว่ายังอยู่ในโรงไหม
# # def is_now_playing(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         return response.json().get("status", "N/A")
# #     return "N/A"
# #
# # # เปิดไฟล์ CSV เพื่อเขียนข้อมูล
# # with open('thai_movies_with_details.csv', mode='w', newline='', encoding='utf-8') as file:
# #     writer = csv.writer(file)
# #
# #     # เพิ่ม header row
# #     writer.writerow([
# #         'movie_id', 'thai_title', 'english_title', 'overview', 'release_date', 'popularity',
# #         'vote_average', 'vote_count', 'genres', 'poster_path', 'cast', 'watch_platforms', 'status'
# #     ])
# #
# #     # วนลูปเพื่อดึงข้อมูลจากทุกหน้า
# #     while True:
# #         response = requests.get(BASE_URL, params=params)
# #         if response.status_code == 200:
# #             data = response.json()
# #             movies = data.get('results', [])
# #             total_pages = data.get('total_pages', 1)
# #
# #             # เขียนข้อมูลของแต่ละหนังลงใน CSV
# #             for movie in movies:
# #                 movie_id = movie.get('id', 'N/A')
# #                 title = movie.get('title', 'N/A')
# #                 original_title = movie.get('original_title', 'N/A')
# #                 overview = movie.get('overview', 'N/A')
# #                 release_date = movie.get('release_date', 'N/A')
# #                 popularity = movie.get('popularity', 'N/A')
# #                 vote_average = movie.get('vote_average', 'N/A')
# #                 vote_count = movie.get('vote_count', 'N/A')
# #                 poster_path = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
# #
# #                 # ดึงข้อมูลเพิ่มเติม
# #                 cast = get_cast(movie_id)
# #                 watch_platforms = get_watch_providers(movie_id)
# #                 status = is_now_playing(movie_id)
# #
# #                 # เพิ่มข้อมูลหนังลงในไฟล์
# #                 writer.writerow([
# #                     movie_id, title, original_title, overview, release_date, popularity,
# #                     vote_average, vote_count, poster_path, cast, watch_platforms, status
# #                 ])
# #
# #             # เช็คว่าถึงหน้าสุดท้ายหรือยัง
# #             if params['page'] >= total_pages:
# #                 break
# #
# #             # เพิ่มค่า page เพื่อดึงหน้าถัดไป
# #             params['page'] += 1
# #         else:
# #             print(f"Failed to retrieve data on page {params['page']}: {response.status_code} - {response.text}")
# #             break
# #
# # print('All Thai movies with details have been saved to thai_movies_with_details.csv')
#
#
# # import requests
# # import csv
# #
# # # API Key และ URL
# # API_KEY = '33b7e0a891dc3f77534d78102c3d1546'
# # BASE_URL = 'https://api.themoviedb.org/3/discover/movie'
# #
# # # Parameters สำหรับ API
# # params = {
# #     'api_key': API_KEY,
# #     'region': 'TH',
# #     'language': 'th-TH',
# #     'sort_by': 'popularity.desc',
# #     'include_adult': 'false',
# #     'with_original_language': 'th',
# #     'page': 1
# # }
# #
# #
# # # ฟังก์ชันดึงข้อมูลนักแสดง พร้อมรูปภาพ
# # def get_cast(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         cast = response.json().get("cast", [])[:5]  # ดึงเฉพาะ 5 คนแรก
# #         return ', '.join([
# #             f"{actor['name']} ({'https://image.tmdb.org/t/p/w500' + actor['profile_path'] if actor.get('profile_path') else 'N/A'})"
# #             for actor in cast
# #         ])
# #     return "N/A"
# #
# #
# # # ฟังก์ชันดึงข้อมูลแพลตฟอร์ม
# # def get_watch_providers(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         providers = response.json().get("results", {}).get("TH", {}).get("flatrate", [])
# #         return ', '.join([provider["provider_name"] for provider in providers]) if providers else "N/A"
# #     return "N/A"
# #
# #
# # # ฟังก์ชันเช็คว่ายังอยู่ในโรงไหม
# # def is_now_playing(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         return response.json().get("status", "N/A")
# #     return "N/A"
# #
# #
# # # เปิดไฟล์ CSV เพื่อเขียนข้อมูล
# # with open('thai_movies_with_details_and_picture.csv', mode='w', newline='', encoding='utf-8') as file:
# #     writer = csv.writer(file)
# #
# #     # เพิ่ม header row
# #     writer.writerow([
# #         'movie_id', 'thai_title', 'english_title', 'overview', 'release_date', 'popularity',
# #         'vote_average', 'vote_count', 'genres', 'poster_path', 'cast', 'watch_platforms', 'status'
# #     ])
# #
# #     # วนลูปเพื่อดึงข้อมูลจากทุกหน้า
# #     while True:
# #         response = requests.get(BASE_URL, params=params)
# #         if response.status_code == 200:
# #             data = response.json()
# #             movies = data.get('results', [])
# #             total_pages = data.get('total_pages', 1)
# #
# #             # เขียนข้อมูลของแต่ละหนังลงใน CSV
# #             for movie in movies:
# #                 movie_id = movie.get('id', 'N/A')
# #                 title = movie.get('title', 'N/A')
# #                 original_title = movie.get('original_title', 'N/A')
# #                 overview = movie.get('overview', 'N/A')
# #                 release_date = movie.get('release_date', 'N/A')
# #                 popularity = movie.get('popularity', 'N/A')
# #                 vote_average = movie.get('vote_average', 'N/A')
# #                 vote_count = movie.get('vote_count', 'N/A')
# #                 poster_path = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
# #
# #                 # ดึงข้อมูลเพิ่มเติม
# #                 cast_data = get_cast(movie_id)
# #                 watch_platforms = get_watch_providers(movie_id)
# #                 status = is_now_playing(movie_id)
# #
# #                 # เพิ่มข้อมูลหนังลงในไฟล์
# #                 writer.writerow([
# #                     movie_id, title, original_title, overview, release_date, popularity,
# #                     vote_average, vote_count, poster_path, cast_data, watch_platforms, status
# #                 ])
# #
# #             # เช็คว่าถึงหน้าสุดท้ายหรือยัง
# #             if params['page'] >= total_pages:
# #                 break
# #
# #             # เพิ่มค่า page เพื่อดึงหน้าถัดไป
# #             params['page'] += 1
# #         else:
# #             print(f"Failed to retrieve data on page {params['page']}: {response.status_code} - {response.text}")
# #             break
# #
# # print('All Thai movies with details have been saved to thai_movies_with_details.csv')
#
#
# # import requests
# # import csv
# # import json
# #
# # # API Key and Base URL
# # API_KEY = '33b7e0a891dc3f77534d78102c3d1546'
# # BASE_URL = 'https://api.themoviedb.org/3/discover/movie'
# #
# # params = {
# #     'api_key': API_KEY,
# #     'region': 'TH',
# #     'language': 'th-TH',
# #     'sort_by': 'popularity.desc',
# #     'include_adult': 'false',
# #     'with_original_language': 'th',
# #     'page': 1
# # }
# #
# #
# # # Function to get genres and theatrical status
# # def get_movie_details(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=th-TH"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         movie_data = response.json()
# #         genres = ", ".join([genre["name"] for genre in movie_data.get("genres", [])])
# #         status = movie_data.get("status", "N/A")  # Theatrical status
# #         return genres, status
# #     return "N/A", "N/A"
# #
# #
# # # Function to get cast with images
# # def get_cast(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         cast = response.json().get("cast", [])[:5]  # Only top 5 actors
# #         return ', '.join([
# #             f"{actor['name']} ({'https://image.tmdb.org/t/p/w500' + actor['profile_path'] if actor.get('profile_path') else 'N/A'})"
# #             for actor in cast
# #         ])
# #     return "N/A"
# #
# #
# # # Function to get streaming platforms for all countries
# # def get_watch_providers(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         provider_data = response.json().get("results", {})
# #         platforms_by_country = {}
# #
# #         for country, data in provider_data.items():
# #             providers = data.get("flatrate", [])  # Streaming platforms
# #             buy_providers = data.get("buy", [])  # Purchase options
# #             rental_providers = data.get("rent", [])  # Rental options
# #
# #             streaming = ', '.join([provider["provider_name"] for provider in providers]) if providers else "N/A"
# #             buy = ', '.join([provider["provider_name"] for provider in buy_providers]) if buy_providers else "N/A"
# #             rent = ', '.join(
# #                 [provider["provider_name"] for provider in rental_providers]) if rental_providers else "N/A"
# #
# #             platforms_by_country[country] = {
# #                 "streaming": streaming,
# #                 "buy": buy,
# #                 "rent": rent
# #             }
# #
# #         return json.dumps(platforms_by_country, ensure_ascii=False)
# #     return "N/A"
# #
# #
# # # Function to check if it's a movie or TV series
# # def get_movie_type(movie_id):
# #     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         return "Movie"
# #
# #     url = f"https://api.themoviedb.org/3/tv/{movie_id}?api_key={API_KEY}"
# #     response = requests.get(url)
# #     if response.status_code == 200:
# #         return "TV Series"
# #
# #     return "Unknown"
# #
# #
# # # Open CSV file for writing
# # with open('thai_movies_with_full_details.csv', mode='w', newline='', encoding='utf-8') as file:
# #     writer = csv.writer(file)
# #
# #     # New header row
# #     writer.writerow([
# #         'movie_id', 'thai_title', 'english_title', 'overview', 'release_date', 'popularity',
# #         'vote_average', 'vote_count', 'genres', 'poster_path', 'cast', 'watch_platforms',
# #         'status', 'movie_type'
# #     ])
# #
# #     while True:
# #         response = requests.get(BASE_URL, params=params)
# #         if response.status_code == 200:
# #             data = response.json()
# #             movies = data.get('results', [])
# #             total_pages = data.get('total_pages', 1)
# #
# #             for movie in movies:
# #                 movie_id = movie.get('id', 'N/A')
# #                 title = movie.get('title', 'N/A')
# #                 original_title = movie.get('original_title', 'N/A')
# #                 overview = movie.get('overview', 'N/A')
# #                 release_date = movie.get('release_date', 'N/A')
# #                 popularity = movie.get('popularity', 'N/A')
# #                 vote_average = movie.get('vote_average', 'N/A')
# #                 vote_count = movie.get('vote_count', 'N/A')
# #                 poster_path = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
# #
# #                 # Fetch additional data
# #                 genres, status = get_movie_details(movie_id)
# #                 cast_data = get_cast(movie_id)
# #                 watch_platforms = get_watch_providers(movie_id)
# #                 movie_type = get_movie_type(movie_id)
# #
# #                 # Write row to CSV
# #                 writer.writerow([
# #                     movie_id, title, original_title, overview, release_date, popularity,
# #                     vote_average, vote_count, genres, poster_path, cast_data, watch_platforms,
# #                     status, movie_type
# #                 ])
# #
# #             # Stop at last page
# #             if params['page'] >= total_pages:
# #                 break
# #
# #             params['page'] += 1  # Next page
# #         else:
# #             print(f"Failed on page {params['page']}: {response.status_code} - {response.text}")
# #             break
# #
# # print('✅ All movies saved to thai_movies_with_full_details.csv')
#
#
# import requests
# import csv
# import json
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
# # ✅ Function to get cast (with images)
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
# # ✅ Function to get streaming platforms (only for Thailand)
# def get_watch_providers(content_id, content_type):
#     url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers?api_key={API_KEY}"
#     response = session.get(url)
#     if response.status_code == 200:
#         providers = response.json().get("results", {}).get("TH", {}).get("flatrate", [])
#         return ', '.join([provider["provider_name"] for provider in providers]) if providers else "N/A"
#     return "N/A"
#
# # ✅ Function to fetch details using multithreading (parallel execution)
# def fetch_content_details(content, content_type):
#     content_id = content.get('id', 'N/A')
#     title = content.get('name' if content_type == 'tv' else 'title', 'N/A')  # Name for TV series
#     original_title = content.get('original_name' if content_type == 'tv' else 'original_title', 'N/A')
#     overview = content.get('overview', 'N/A')
#     release_date = content.get('first_air_date' if content_type == 'tv' else 'release_date', 'N/A')
#     popularity = content.get('popularity', 'N/A')
#     vote_average = content.get('vote_average', 'N/A')
#     vote_count = content.get('vote_count', 'N/A')
#     poster_path = f"https://image.tmdb.org/t/p/w500{content.get('poster_path', '')}"
#
#     # ✅ Run API calls in parallel (much faster!)
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         genres_status_future = executor.submit(get_details, content_id, content_type)
#         cast_future = executor.submit(get_cast, content_id, content_type)
#         watch_platforms_future = executor.submit(get_watch_providers, content_id, content_type)
#
#         genres, status = genres_status_future.result()
#         cast_data = cast_future.result()
#         watch_platforms = watch_platforms_future.result()
#
#     return [
#         content_id, title, original_title, overview, release_date, popularity,
#         vote_average, vote_count, genres, poster_path, cast_data, watch_platforms,
#         status, "Movie" if content_type == "movie" else "TV Series"
#     ]
#
# # ✅ Open CSV file for writing
# with open('thai_movies_and_tv.csv', mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#
#     # New header row
#     writer.writerow([
#         'id', 'thai_title', 'english_title', 'overview', 'release_date', 'popularity',
#         'vote_average', 'vote_count', 'genres', 'poster_path', 'cast', 'watch_platforms',
#         'status', 'content_type'
#     ])
#
#     # ✅ Function to fetch both movies and TV series
#     def fetch_content(content_url, content_type):
#         params["page"] = 1
#         while True:
#             response = session.get(content_url, params=params)
#             if response.status_code == 200:
#                 data = response.json()
#                 contents = data.get('results', [])
#                 total_pages = data.get('total_pages', 1)
#
#                 # ✅ Use multithreading to process content faster
#                 with concurrent.futures.ThreadPoolExecutor() as executor:
#                     results = list(executor.map(lambda c: fetch_content_details(c, content_type), contents))
#
#                 # ✅ Write all results to CSV in one go (faster)
#                 writer.writerows(results)
#
#                 # Stop at last page
#                 if params["page"] >= total_pages:
#                     break
#
#                 params["page"] += 1  # Next page
#             else:
#                 print(f"Failed on page {params['page']} ({content_type}): {response.status_code}")
#                 break
#
#     # ✅ Fetch both movies and TV series
#     fetch_content(MOVIE_URL, "movie")
#     fetch_content(TV_URL, "tv")
#
# print('✅ All movies & TV series saved to thai_movies_and_tv.csv')
