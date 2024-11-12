# 📹 YouTube Scraper in Python - Extract Video Data Efficiently 🎉

Welcome to the **YouTube Scraper** project! This repository guides you through building a Python-powered YouTube scraper that can extract detailed data from YouTube videos using two powerful methods: **YouTube API** and **Selenium Stealth** (for when you want to bypass YouTube’s bot detection). This project is ideal for anyone looking to gather insights from YouTube for analysis, trend tracking, or even market research. 

> **Check out our YouTube tutorial 📺**  
> [![YouTube](https://img.shields.io/badge/YouTube-Tutorial-red)](https://www.youtube.com/your-tutorial-link)
>
> **Read the Full Blog Post 📄**  
> [![Blog](https://img.shields.io/badge/Blog-Read%20Now-blue)](https://your-blog-link.com)
>
> **Visit the Project Website 🌐**  
> [![Website](https://img.shields.io/badge/Website-Learn%20More-green)](https://your-website-link.com)

---

## ✨ Features
- **Keyword-Based Video Search 🔍** - Extract video metadata based on keywords, location, and language.
- **Detailed Video Stats 🎥** - Retrieve views, likes, tags, description, and more for specific videos.
- **JSON-LD Data Extraction 🌐** - Bypass YouTube API limitations and scrape video details directly from page source.
- **Related Videos Collection 🔗** - Automatically gather related videos without needing to log in.
- **Bot Detection Bypass 🛡️** - Use Selenium Stealth and Proxies to navigate YouTube smoothly.

## 📜 Table of Contents
1. [Introduction](#-introduction)
2. [Setup YouTube API](#-setup-youtube-api)
3. [Keyword-Based Video Scraper](#-keyword-based-video-scraper)
4. [Detailed Video Stats with YouTube API](#-detailed-video-stats-with-youtube-api)
5. [Selenium Stealth Scraper](#-selenium-stealth-scraper)
6. [Related Videos Scraper](#-related-videos-scraper)
7. [Bot Detection Bypass with Proxies](#-bot-detection-bypass-with-proxies)

---

## 📖 Introduction
YouTube offers a wealth of data that can drive powerful insights, from understanding audience interests to tracking popular trends. This project provides **two key methods** to scrape YouTube data:

1. **Official YouTube API** - Fetch structured data directly from YouTube, including video titles, descriptions, views, likes, and more.
2. **Selenium Stealth Mode** - A no-API solution to directly extract data from YouTube while evading bot detection.

Choose the method that best suits your needs for efficient and comprehensive data collection.

---

## 🔑 Setup YouTube API

To start, create a project on Google Cloud and enable the **YouTube Data API v3**. Generate API credentials and install the required Python libraries.

### Installation Command:
```bash
pip install google-api-python-client
```

### Setting up the YouTube API:
With your API key ready, the code initializes the YouTube API service and allows you to make requests easily. 

---

## 🔍 Keyword-Based Video Scraper

Our keyword-based scraper searches YouTube for videos matching specific keywords. Set **language**, **location**, and other parameters to narrow down your search results. This is perfect for topic-specific data analysis!

```python
def youtube_search(keyword, max_results=5, latitude=None, longitude=None, radius="50km", language="en"):
    search_params = {
        "part": "snippet",
        "q": keyword,
        "maxResults": max_results,
        "type": "video",
        "relevanceLanguage": language
    }
    if latitude and longitude:
        search_params["location"] = f"{latitude},{longitude}"
        search_params["locationRadius"] = radius
    
    request = youtube.search().list(**search_params)
    response = request.execute()
    
    video_data = []
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        snippet = item['snippet']
        details = {
            "Title": snippet.get("title", "N/A"),
            "Channel Name": snippet.get("channelTitle", "N/A"),
            "Video URL": f"https://www.youtube.com/watch?v={video_id}",
            "Description": snippet.get("description", "N/A"),
            "Publish Date": snippet.get("publishedAt", "N/A"),
            "Channel ID": snippet.get("channelId", "N/A"),
            "Video ID": video_id,
            "Thumbnail URL": snippet.get("thumbnails", {}).get("high", {}).get("url", "N/A"),
        }
        video_data.append(details)
    
    with open('youtube_videos.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=video_data[0].keys())
        writer.writeheader()
        writer.writerows(video_data)
    print("Video details saved to youtube_videos.csv")

youtube_search("Python tutorial", max_results=50, latitude=37.7749, longitude=-122.4194, radius="50km", language="en")
```

---

## 📊 Detailed Video Stats with YouTube API

This module lets you gather **detailed stats** about each video, such as views, likes, comments, and tags. It's a powerful way to gain in-depth insights about specific YouTube videos.

```python
def get_video_details(url):
    video_id = extract_video_id(url)
    request = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
    response = request.execute()
    
    if "items" not in response or not response["items"]:
        print("Video not found.")
        return
    
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
    }
    with open('video_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=details.keys())
        writer.writeheader()
        writer.writerow(details)
    print("Video details saved to video_details.csv")

get_video_details("https://www.youtube.com/watch?v=_uQrJ0TkZlc")
```

---

## 🌐 Selenium Stealth Scraper

Using Selenium with Stealth, you can avoid bot detection and scrape YouTube directly. This method doesn’t rely on the API, making it ideal for cases where the API is limited or not sufficient.

### Installation:
```bash
pip install selenium selenium-stealth
```

```python
def get_video_details(url):
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    driver.get(url)
    time.sleep(5)
    
    page_source = driver.page_source
    match = re.search(r'({[^}]+"@type":"VideoObject"[^}]+})', page_source)
    if not match:
        print("No JSON-LD data found.")
        return
    json_data = json.loads(match.group(1))
    details = {
        "Title": json_data.get("name", "N/A"),
        "Description": json_data.get("description", "N/A"),
        "Duration": json_data.get("duration", "N/A"),
        "Embed URL": json_data.get("embedUrl", "N/A"),
        "Views": json_data.get("interactionCount", "N/A"),
    }
    print(details)

get_video_details("https://www.youtube.com/watch?v=_uQrJ0TkZlc")
```

---

## 🔗 Related Videos Scraper

The Related Videos module allows you to **gather videos similar to a target video** by simulating user interaction on YouTube’s interface. Great for tracking trends and discovering relevant content!

---

## 🛡️ Bot Detection Bypass with Proxies

For large-scale scraping, proxies help distribute requests and prevent IP bans. We recommend using a reliable proxy service for efficient bot detection avoidance.

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

Happy Scraping! 🎉
