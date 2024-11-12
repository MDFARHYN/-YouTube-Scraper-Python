from googleapiclient.discovery import build
import re, csv

# Define your API Key here
API_KEY = 'AIzaSyDL1uNtSQ2h62JiHrpCCMGQehkDMGgeaIs'  # Replace with your actual API key

# Build the YouTube API service
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Function to extract video ID from a YouTube URL
def extract_video_id(url):
    # Regular expression to match YouTube video ID
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# Function to get video details
def get_video_details(url):
    video_id = extract_video_id(url)
    if not video_id:
        print("Invalid video URL")
        return

    # Call the videos.list method to retrieve video details
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
 
    # Check if the video exists
    if "items" not in response or not response["items"]:
        print("Video not found.")
        return
    
    # Extract video details
    # Parsing and displaying important video details
    video = response["items"][0]

    details = {
        "Title": video["snippet"]["title"],
        "Channel Name": video["snippet"]["channelTitle"],
        "Published At": video["snippet"]["publishedAt"],
        "Description": video["snippet"]["description"],
        "Views": video["statistics"].get("viewCount", "N/A"),
        "Likes": video["statistics"].get("likeCount", "N/A"),
        "Comments": video["statistics"].get("commentCount", "N/A"),
        "Duration": video["contentDetails"]["duration"],
        "Tags": ', '.join(video["snippet"].get("tags", [])),
        "Category ID": video["snippet"]["categoryId"],
        "Default Language": video["snippet"].get("defaultLanguage", "N/A"),
        "Dimension": video["contentDetails"]["dimension"],
        "Definition": video["contentDetails"]["definition"],
        "Captions Available": video["contentDetails"]["caption"],
        "Licensed Content": video["contentDetails"]["licensedContent"]
    }

    # Displaying the details
    print(details)
    
    # Save details to CSV
    with open('video_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=details.keys())
        writer.writeheader()
        writer.writerow(details)
 
    print("Video details saved to video_details.csv")

 
# Example usage
get_video_details("https://www.youtube.com/watch?v=_uQrJ0TkZlc")
