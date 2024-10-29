import requests
import json

# Constants
CLIENT_ID = ''  # Replace with your Twitch Client ID
CLIENT_SECRET = ''  # Replace with your Twitch Client Secret
BASE_URL = 'https://api.twitch.tv/helix'

# Function to get an OAuth token
def get_oauth_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    return response.json()['access_token']

# Function to get stream metrics with enhanced bot detection
def get_stream_metrics(user_login):
    oauth_token = get_oauth_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {oauth_token}'
    }

    # Get user ID from username
    user_response = requests.get(f'{BASE_URL}/users?login={user_login}', headers=headers)
    if not user_response.json()['data']:
        print("User not found or user is offline.")
        return None

    user_id = user_response.json()['data'][0]['id']

    # Get stream info
    stream_response = requests.get(f'{BASE_URL}/streams?user_id={user_id}', headers=headers)
    stream_data = stream_response.json()

    if not stream_data['data']:
        print("The streamer is not live.")
        return None

    total_views = stream_data['data'][0]['viewer_count']
    
    # Example of fetching chat activity
    # Note: Replace this with the correct endpoint to get chat data if available
    # Currently, the Twitch API does not provide a direct way to get chat activity.
    chat_activity = total_views * 0.1  # Placeholder for chat activity

    # Adjust bot detection logic based on chat activity
    if chat_activity < total_views * 0.05:  # Example threshold for low engagement
        bot_viewers = int(total_views * 0.30)  # Increase assumption of bot viewers
    else:
        bot_viewers = int(total_views * 0.10)  # Keep 10% if engagement is normal

    real_viewers = total_views - bot_viewers

    return {
        'username': user_login,
        'total_views': total_views,
        'bot_viewers': bot_viewers,
        'real_viewers': real_viewers
    }

# Function to save metrics to JSON
def save_metrics_to_json(metrics, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(metrics, json_file, indent=4)

# Example usage
if __name__ == "__main__":
    username = 'maximilian_dood'  # Replace with the Twitch username you want to analyze
    metrics = get_stream_metrics(username)

    if metrics:
        print(f"Username: {metrics['username']}")
        print(f"Total View Count: {metrics['total_views']}")
        print(f"Bot Viewers: {metrics['bot_viewers']}")
        print(f"Real Viewers: {metrics['real_viewers']}")

        # Save the metrics to JSON file
        file_path = r'data.json'  # Path to save the JSON file
        save_metrics_to_json(metrics, file_path)
        print(f"Metrics saved to {file_path}")
