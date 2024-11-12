import json
import time
import re
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv 


# Function to create proxy authentication extension
def create_proxy_auth_extension(proxy_host, proxy_user, proxy_pass):
    import zipfile
    import os

    # Separate the host and port
    host = proxy_host.split(':')[0]  # Extract the host part (e.g., "la.residential.rayobyte.com")
    port = proxy_host.split(':')[1]  # Extract the port part (e.g., "8000")

    # Define proxy extension files
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    
    background_js = f"""
    var config = {{
            mode: "fixed_servers",
            rules: {{
              singleProxy: {{
                scheme: "http",
                host: "{host}",
                port: parseInt({port})
              }},
              bypassList: ["localhost"]
            }}
          }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy_user}",
                    password: "{proxy_pass}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """

    # Create the extension
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return pluginfile
 

# Proxy configuration
proxy_server = "server_name:port"  # Replace with your proxy server and port
proxy_username = "username"  # Replace with your proxy username
proxy_password = "password"  # Replace with your proxy password


# Initialize Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument(f'--proxy-server={proxy_server}')
# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Add proxy authentication if necessary (for proxies that require username/password)
if proxy_username and proxy_password:
        # Chrome does not support proxy authentication directly; use an extension for proxy authentication
        options.add_extension(create_proxy_auth_extension(proxy_server, proxy_username, proxy_password))

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
         
    }

    # Print the extracted details
    for key, value in details.items():
        print(f"{key}: {value}")

 

    # Save details to CSV
    with open('video_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=details.keys())
        writer.writeheader()
        writer.writerow(details)

# Example usage
get_video_details("https://www.youtube.com/watch?v=_uQrJ0TkZlc")
 


