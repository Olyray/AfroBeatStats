#!/usr/bin/python3
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    token_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(token_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    if auth_response.status_code == 200:
        token_info = auth_response.json()
        access_token = token_info['access_token']
        return access_token
    else:
        print(f"Error: {auth_response.status_code} - {auth_response.text}")
        return None


if __name__ == "__main__":
    # Get the access token
    access_token = get_token()

    if access_token:
        # Set the headers with the access token
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Set the search parameters
        search_query = 'genre:afrobeats'
        search_type = 'artist'
        limit = 50  # Adjust the limit as per your requirements
        offset = 0
        total_results = 0
        artists = []

        # Perform the initial search request to retrieve the total number of results
        search_url = 'https://api.spotify.com/v1/search'
        search_params = {
            'q': search_query,
            'type': search_type,
            'limit': limit,
            'offset': offset
        }
        response = requests.get(search_url, headers=headers, params=search_params)

        if response.status_code == 200:
            data = response.json()
            total_results = data['artists']['total']

            # Collect all artists from subsequent pages
            while offset < total_results:
                response = requests.get(search_url, headers=headers, params=search_params)
                if response.status_code == 200:
                    data = response.json()
                    artists += data['artists']['items']
                    offset += limit
                    search_params['offset'] = offset
                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    break

            # Sort artists by popularity
            artists = sorted(artists, key=lambda x: x['popularity'], reverse=True)

            # Select the top ten artists
            top_ten_artists = artists[:10]

            # Prepare the data to write to the JSON file
            data_to_write = []
            for artist in top_ten_artists:
                artist_data = {
                    'name': artist['name'],
                    'popularity': artist['popularity']
                }
                data_to_write.append(artist_data)

            # Write the data to the JSON file
            file_path = 'file_storage.json'
            with open(file_path, 'w') as file:
                json.dump(data_to_write, file, indent=4)

            print(f"Top ten Afrobeats artists saved to {file_path}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
