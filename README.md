# External Link Checker for Blog Posts & Articles

A script to **check for broken external links** on any public web page and **generate a Markdown report** of valid and invalid links. Ideal for bloggers, content editors, and developers maintaining evergreen content.

---

## 📚 Learning Journey

This script was created as part of my learning process with:

- **Web scraping** using `requests` and `BeautifulSoup`
- **URL parsing** with `urllib.parse`
- **Validating HTTP response codes**
- **Markdown report generation**
- Planning future integration with **OpenAI GPT** for automated link replacement suggestions

It started as a hands-on exercise in cleaning up blog posts, but it evolved into a modular tool with reusable logic for any link-checking context.

---

## 🧠 How It Works

This script is designed to be **terminal-based** and follows these main stages:

### 1. Fetch the Page

- Prompt the user for a URL.
- Use `requests.get` to fetch the full page contents with custom headers (mimicking `curl`).
- Validate the page using known HTTP status codes.

You can edit the header as needed:
```python
headers = {
    "User-Agent": "curl/8.11.1",
    "Accept": "*/*"
}
```

---

### 2. Extract Links

- Parse HTML using `BeautifulSoup`.
- Find all `<a>` tags and extract `href` attributes.
- Filter out empty or hash-only (`#`) anchors.

```python
linkslist = [a['href'] for a in formattedhtml.find_all('a', href=True)]
```

---

### 3. Clean and Classify Links

- Clean duplicates using `set`.
- Parse the domain with `urlparse` and classify:
  - **Internal links** → same domain
  - **External links** → different domain

```python
if base_domain in parsed_link.netloc:
    internal_links.append(link)
else:
    external_links.append(link)
```

---

### 4. Check External Link Status

- Use `requests.head()` to check status codes of external links.
- Valid codes: `200 OK`
- Invalid: other codes or exceptions (e.g., timeout, DNS errors)

```python
response = requests.head(url, allow_redirects=True, timeout=5)
```

---

### 5. Generate Markdown Report

- Save output as `external-links-YYYYMMDD-HHMMSS.md`
- Sections include:
  - ✅ Valid Links
  - ❌ Invalid Links

```python
markdown_output = f"# External Link Check Report\n\nGenerated: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
```

---

## File Structure

```bash
.
├── check_links.py         # Main script
├── .env                   # Environment file (for GPT API key)
├── external-links-*.md    # Generated output reports
```

---

## 🛠️ Requirements

- Python 3
- `requests`
- `beautifulsoup4`
- `python-dotenv`
- Optional (planned): `openai`

Install with:

```bash
pip install -r requirements.txt
```

```txt
# requirements.txt
requests
beautifulsoup4
python-dotenv
openai
```

---

## Planned Improvements

### Functionality Goals

- [ ] **Add functions**
- [ ] **GPT Suggestions**: Automatically recommend alternative working links using ChatGPT.
- [ ] **WordPress Terminal Mode**: Allow execution inside a WordPress editor session (CLI or headless browser).
- [ ] **Pretty Titles & Output**: Enhance visual formatting for terminal and markdown report:
  - Fetch and display `<title>` of the input page
  - Format valid/invalid sections with emojis and colors
- [ ] **Handle relative internal links** more thoroughly (convert to absolute if needed)
- [ ] **Add retry logic** for flaky servers
- [ ] **Optional output to JSON**, for integration into CI pipelines or dashboards
- [ ] **Ignore-list support**: Let user skip known broken links (e.g., tracking URLs)
- [ ] **Batch processing**: Accept a list of URLs instead of one at a time
- [ ] **Ability to input full site**, not just one URL, crawl the whole site, then check every link on the site.
  - Two modes: page mode, site mode.

---

## Usage Example

```bash
$ python3 check_links.py
Enter the URL to check links: https://example.com/blog-post
```

**Output:**

- Internal and external link listing
- ✅ Valid and ❌ Invalid link classification
- Markdown report saved to file

---

## Environment Configuration

Use a `.env` file for your OpenAI key (for future GPT integration):

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

---

## Author Notes

This tool is a **work-in-progress**, but it already serves as a valuable utility for auditing blog posts, newsletters, and knowledge bases.

It also taught me a lot about:

- Error handling in real-world HTTP
- Respecting timeouts and performance in scraping
- Structuring code into logical stages
- Thinking about future integration with AI

---

## 🤝 Contributions

Feel free to fork this and adapt it to your own CMS or workflow! Pull requests, issue reports, and ideas are welcome.

---

## 📄 License

MIT License
