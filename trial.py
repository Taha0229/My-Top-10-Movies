import requests

api_key = "761b9764dc14fad26bb0bf065c584a09"
#
# base_image_url = "http://image.tmdb.org/t/p/original/"
#
# search_path = "https://api.themoviedb.org/3/search/movie?api_key=761b9764dc14fad26bb0bf065c584a09"
# movie_name = input("enter a movie name")
# params = {
#     'query': movie_name
# }
# headers = {
#     'api_key': api_key
# }
#
# response = requests.get(url=search_path, params=params)
# data = response.json()
# image_path = []
# for i in data['results']:
#     poster_path = f"{base_image_url}{i['poster_path']}"
#     image_path.append(poster_path)
# print(data)
# print(image_path)

movie_id = "603"

resp = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US")
data = resp.json()
print(data)
print(data['release_date'][:4])