from googleapiclient.discovery import build
import csv

# Define your API Key here
API_KEY = 'AIzaSyDL1uNtSQ2h62JiHrpCCMGQehkDMGgeaIs'  # Replace with your actual API key
# Build the YouTube API service
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Define the search function with location and language
def youtube_search(keyword, max_results=5, latitude=None, longitude=None, radius="50km", language="en"):
    # Prepare parameters for location search if latitude and longitude are provided
    search_params = {
        "part": "snippet",
        "q": keyword,
        "maxResults": max_results,
        "type": "video",
        "relevanceLanguage": language  # Specify the relevance language
    }
    # Add location parameters if latitude and longitude are provided
    if latitude is not None and longitude is not None:
        search_params["location"] = f"{latitude},{longitude}"
        search_params["locationRadius"] = radius

    # Call the search.list method to retrieve results matching the keyword, location, and language
    request = youtube.search().list(**search_params)
    response = request.execute()
    
    # List to store video details for CSV
    video_data = []


    # Print important video details
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        snippet = item['snippet']
        
        # Extract 20 important data points
        details = {
            "Title": snippet.get("title", "N/A"),
            "Channel Name": snippet.get("channelTitle", "N/A"),
            "Video URL": f"https://www.youtube.com/watch?v={video_id}",
            "Description": snippet.get("description", "N/A"),
            "Publish Date": snippet.get("publishedAt", "N/A"),
            "Channel ID": snippet.get("channelId", "N/A"),
            "Video ID": video_id,
            "Thumbnail URL": snippet.get("thumbnails", {}).get("high", {}).get("url", "N/A"),
            "Location Radius": radius,
            "Relevance Language": language,
            "Latitude": latitude if latitude else "N/A",
            "Longitude": longitude if longitude else "N/A",
        
        }

        # Append details to video_data for saving to CSV
        video_data.append(details)

        # Print the extracted details
        print("\nVideo Details:")
        for key, value in details.items():
            print(f"{key}: {value}")
    
    # Save video details to a CSV file
    with open('youtube_videos.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = video_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(video_data)

    print("Video details saved to youtube_videos.csv")

# Example usage: Search for videos by keyword, location, and language
# Location: San Francisco (latitude: 37.7749, longitude: -122.4194), Language: English
youtube_search("Python tutorial", max_results=50, latitude=37.7749, longitude=-122.4194, radius="50km", language="en")
