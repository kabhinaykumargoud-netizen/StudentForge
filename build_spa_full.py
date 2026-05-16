import os
import re
import urllib.request

# 1. Identify all HTML files
files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html' and not f.startswith('downloaded')]

# 2. Extract CSS links
css_links = set()
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        links = re.findall(r'href="(/_next/static/css/[a-z0-9]+\.css)"', content)
        css_links.update(links)

print('Found CSS:', css_links)

# 3. Download and merge CSS into css/styles.css
merged_css = ""
for css_path in css_links:
    url = f"https://studentforge.vercel.app{css_path}"
    print(f"Downloading {url}...")
    try:
        response = urllib.request.urlopen(url)
        merged_css += response.read().decode('utf-8') + "\n"
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Add SPA styles
merged_css += """
/* SPA Styles */
.spa-view { display: none; min-height: 100vh; }
.spa-view.active { display: block; }
"""

os.makedirs('css', exist_ok=True)
with open('css/styles.css', 'w', encoding='utf-8') as f:
    f.write(merged_css)

# 4. Build index.html
def extract_body_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
        if body_match:
            body_content = body_match.group(1)
            body_content = re.sub(r'<script[^>]*src="/_next[^>]*></script>', '', body_content)
            body_content = re.sub(r'<script>\(self\.__next_f.*?</script>', '', body_content, flags=re.DOTALL)
            return body_content
        return ""
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return ""

views_html = ""
for html_file in files:
    view_id = "view-" + html_file.replace('.html', '')
    if html_file == 'landing.html':
        active_class = " active"
    else:
        active_class = ""
    
    body = extract_body_content(html_file)
    views_html += f'<div id="{view_id}" class="spa-view{active_class}">\n{body}\n</div>\n'

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>StudentForge Platform</title>
    <meta name="description" content="Welcome to StudentForge" />
    <link rel="icon" href="/sf-next-logo.png" type="image/png" />
    <link rel="stylesheet" href="css/styles.css" />
    <script src="js/main.js" defer></script>
</head>
<body class="geist_a71539c9-module__T19VSG__variable geist_mono_8d43a2aa-module__8Li5zG__variable antialiased selection:bg-zinc-50 selection:text-black">
{views_html}
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Successfully built index.html and css/styles.css")
