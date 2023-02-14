import random
from string import ascii_lowercase
import requests
import json
import time
import logging

def run_bot() -> None:
    with open("config.json", 'r') as config_file:
        bot = json.load(config_file)
        number_of_users = bot['number_of_users']
        max_posts_per_user = bot['max_posts_per_user']
        max_likes_per_user = bot['max_likes_per_user']

    def generate_user_data() -> str:
        return {"username": f'bot-{str(time.time())}',
                "password": "123qweQWE",
                "email": f'bot-{time.time()}@gmail.com',
                "first_name": f"bot-name-{str(random.randrange(1000, 9999))}",
                "last_name": f"bot-last-name-{str(random.randrange(1000, 9999))}",
            }
    
    def generate_text(n: int) -> str:
        chars = ascii_lowercase + " " * 10
        return "".join(random.choice(chars) for _ in range(n))


    def create_user() -> None:
        url_create_user = "http://localhost:8000/auth/users/"
        try:
            response = requests.post(url_create_user, data=user_data)
        except Exception as e:
            print(f"Error was due to following exception: {e}")
            raise 
           
        if response.status_code == 201:
            print(f"Username {user_data['username']} was created.")
        else:
            print(response.status_code)
            
    def get_access_token() -> str:
        url = "http://localhost:8000/auth/jwt/create"
        data = {
            'username': user_data['username'],
            'password': user_data['password']
        }
        try:
            response = requests.post(url, data=data)
        except Exception as e:
            print(f"Error was due to following exception: {e}")
            raise 
        
        data = response.json()
        access_token = data['access']
        return access_token

    def create_post() -> None: 
        url_create_post = "http://localhost:8000/api/posts/"
        post_data = {
            'title': generate_text(4),
            'body': generate_text(300)
        }
        
        try:
            response = requests.post(url_create_post, headers=headers, data=post_data)
        except Exception as e:
            print(f"Error was due to following exception: {e}")
            raise
        
        if response.status_code == 201:
             print(f"Post with title {post_data['title']} created.")
        else:
            print(f"Status code: {response.status_code}")
        
    def like_posts() -> None:
        url = "http://localhost:8000/api/posts/"
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print(f"Error was due to following exception: {e}")
            raise
        
        data = response.json()
        post_ids = [str(post['id']) for post in data]
        post_id = random.choice(post_ids)

        url_like = f"http://localhost:8000/api/posts/{post_id}/like/"
        try:
            response = requests.post(url_like, headers=headers)
        except Exception as e:
            print(f"Error was due to following exception: {e}")
            raise
        
        if response.status_code == 201:
            print(f"Post with id {post_id} was liked by {user_data['username']}")
        else:
            print(f"Status code: {response.status_code}")
                    
     
    for _ in range(number_of_users):
        user_data = generate_user_data()
        create_user()
        access_token = get_access_token()
        headers = {'Authorization': 'JWT {}'.format(access_token)}
        for _ in range(max_posts_per_user):
            create_post()
        for _ in range(max_likes_per_user):
            like_posts()


if __name__ == "__main__":
    run_bot()