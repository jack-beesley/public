,#!/usr/bin/python3

import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import os
import openai
from dotenv import load_dotenv

# Setup the .env
load_dotenv()

# --- Fetch the page ---
# Ask the user for the URL
inputurl = input("Enter the URL to check links: ")
print("Fetching page...")

# Headers for the requests
headers = {
    "User-Agent": "curl/8.11.1",
    "Accept": "*/*"
    }

# Do a HTTP GET request to get the status code
page = requests.get(inputurl, headers=headers)
print ("Status code is:", page.status_code)

# Define status codes
validcode = [200, 301, 302, 304]
invalidcode = [500, 404, 403]

# Check the status code is valid
if page.status_code in validcode:
    print(page, "is valid")
    # If it is, fetch the full page
    print("Retrieving page", inputurl, "...")
    html = page.text
elif page.status_code in invalidcode:
    # if it is a correct invalid code, exit with an error
    print(page, " is invalid, exiting...")
    sys.exit(1)
else:
    # If it is a code I haven't put in the list above, exit
    print("Unhandled error, you broke it somehow, exiting...")
    sys.exit(2)


# --- Extract all the links ---
print("Length of the HTML document is: ", len(html))
formattedhtml = BeautifulSoup(html, 'html.parser')
linkslist = [a['href'] for a in formattedhtml.find_all('a', href=True)]
for link in linkslist:
    print(link)


# --- Cleanup internal links ---
cleaned_links = set()
for link in linkslist:
    if link and not link.startswith('#'):
        cleaned_links.add(link)


# --- Seperate External from Internal Links ---
parsed_url = urlparse(inputurl)
base_domain = parsed_url.netloc

internal_links = []
external_links = []

for link in cleaned_links:
    parsed_link = urlparse(link)

    # Handle relative URLs (like /about)
    if not parsed_link.netloc:
        internal_links.append(link)
        continue

    # Check if domain matches
    if base_domain in parsed_link.netloc:
        internal_links.append(link)
    else:
        external_links.append(link)

print("Internal Links:")
print("\n".join(internal_links))

print("\nExternal Links:")
print("\n".join(external_links))


# --- Parse the links ---
valid_links = {}
invalid_links = {}

for url in external_links:
    try:
        response = requests.head(url, allow_redirects=True, timeout=5, headers=headers)
        status = response.status_code

        if status == 200:
            valid_links[url] = status
        else:
            invalid_links[url] = status

    except requests.exceptions.RequestException as e:
        # Could not reach the server or other error
        invalid_links[url] = f"Error: {str(e)}"

print("\n✅ VALID LINKS (200):")
for link, status in valid_links.items():
    print(f"{status} - {link}")

print("\n❌ INVALID LINKS:")
for link, status in invalid_links.items():
    print(f"{status} - {link}")


# --- Output Report ---
now = datetime.now()
filename = now.strftime("external-links-%Y%m%d-%H%M%S.md")

valid_section = "## ✅ Valid Links (200 OK)\n"
for link, code in valid_links.items():
    valid_section += f"- [{code}]({link}) {link}\n"

invalid_section = "## ❌ Invalid Links\n"
for link, code in invalid_links.items():
    invalid_section += f"- [{code}]({link}) {link}\n"

markdown_output = f"# External Link Check Report\n\nGenerated: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
markdown_output += valid_section + "\n" + invalid_section

with open(filename, "w", encoding="utf-8") as f:
    f.write(markdown_output)

print("\n📝 Markdown report saved as:", filename)


# --- ChatGPT ---
# client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
#
# print("Your OpenAPI Key is: ", os.environ["OPENAI_API_KEY"])
#
# broken_links_list = "\n".join(f"[{code}] {link}" for link, code in invalid_links.items())
#
# prompt = f"""
# You're a helpful web assistant. I have a list of broken external links from a blog post or article. For each one, suggest a high-quality, trustworthy, and up-to-date replacement link with similar content or value. Return your suggestions in markdown format with a short description.
#
# Broken links:
# {broken_links_list}
#
# Return format:
# - [Replacement Title](https://replacement.url) — short description of what this link offers.
# """
#
# # Step 1: Send the prompt to GPT
# response = client.chat.completions.create(
#     model="gpt-4",
#     messages=[{"role": "user", "content": prompt}]
# )
#
# # Step 2: Extract content
# suggestions = response.choices[0].message.content.strip()
#
# # Step 3: Print to stdout
# print("\n🔁 Suggested Replacements:\n")
# print(suggestions)
#
# # Step 4: Append to the markdown file
# with open(filename, "a", encoding="utf-8") as f:
#     f.write("\n\n## 🔁 Suggested Replacements\n")
#     f.write(suggestions)
