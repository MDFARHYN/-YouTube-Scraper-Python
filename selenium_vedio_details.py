import json
import time
import re
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv 


# Initialize Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Specify the Chrome user data directory up to "User Data" only
options.add_argument(r"user-data-dir=C:\Users\farhan\AppData\Local\Google\Chrome\User Data")

# Specify the profile directory (e.g., "Profile 17")
options.add_argument("profile-directory=Profile 17")

driver = webdriver.Chrome(options=options)

# Function to extract video details using JSON-LD data with regex
def get_video_details(url):
    # Apply Selenium Stealth to avoid detection
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    driver.get(url)
    time.sleep(5) 

    # Extract the page source
    page_source = driver.page_source

    # Use regex to find the JSON-LD data for VideoObject
    match = re.search(r'({[^}]+\"@type\":\"VideoObject\"[^}]+})', page_source)
    if not match:
        print("No JSON-LD data found.")
        return

    # Parse JSON-LD data
    json_data = json.loads(match.group(1))

    # Extract the top 20 most important video details
    details = {
        "Title": json_data.get("name", "N/A"),
        "Description": json_data.get("description", "N/A"),
        "Duration": json_data.get("duration", "N/A"),
        "Embed URL": json_data.get("embedUrl", "N/A"),
        "Views": json_data.get("interactionCount", "N/A"),
        "Thumbnail URL": json_data.get("thumbnailUrl", ["N/A"])[0],
        "Upload Date": json_data.get("uploadDate", "N/A"),
        "Genre": json_data.get("genre", "N/A"),
        "Channel Name": json_data.get("author", "N/A"),
        "Context": json_data.get("@context", "N/A"),
        "Type": json_data.get("@type", "N/A"),
        "Related URLs": []  # Initialize as an empty list
    }

    # Print the extracted details
    for key, value in details.items():
        print(f"{key}: {value}")

    try:
        while True:
            time.sleep(3)
            # Loop to click the "Next" arrow until the "Related" button is visible
            # Click the "Next" arrow if the "Related" button isn't found
            next_arrow = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@id='right-arrow-button']//button"))
                    )
            next_arrow.click()
            time.sleep(3)  # Short delay to allow elements to load
    
            # Try to locate the "Related" button
            related_button = driver.find_element(By.XPATH, "//yt-chip-cloud-chip-renderer[.//yt-formatted-string[@title='Related']]")
            if related_button.is_displayed():
                    related_button.click()
                    print("Clicked on the 'Related' button.")
                    time.sleep(3)
                    all_related_vedio_url = r'yt-simple-[^>]+video-renderer[^>]+href="([^"]+)'
                    urls = re.findall(all_related_vedio_url,page_source)
                    # Add the related URLs to the list in `details`
                    details["Related URLs"].extend([f"https://www.youtube.com{url}" for url in urls])
                    for url in urls:
                        print(f"https://www.youtube.com{url}") 
                    break

    except Exception as e:
        print("Could not find or click the 'Related' button:", e)
    
    # Join related URLs as a single string separated by commas
    details["Related URLs"] = ", ".join(details["Related URLs"])

    # Save details to CSV
    with open('video_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=details.keys())
        writer.writeheader()
        writer.writerow(details)

# Example usage
get_video_details("https://www.youtube.com/watch?v=_uQrJ0TkZlc")
 

 