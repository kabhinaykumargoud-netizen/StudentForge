import re

def extract_body_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract everything inside <body>...</body>
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
        if body_match:
            body_content = body_match.group(1)
            # Remove any trailing Next.js script tags from the body to keep it clean
            body_content = re.sub(r'<script[^>]*src="/_next[^>]*></script>', '', body_content)
            body_content = re.sub(r'<script>\(self\.__next_f.*?</script>', '', body_content, flags=re.DOTALL)
            return body_content
        return ""
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return ""

views = {
    'landing': extract_body_content('landing.html'),
    'courses': extract_body_content('courses.html'),
    'signin': extract_body_content('signin.html')
}

# Construct the unified index.html
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>StudentForge Platform</title>
    <meta name="description" content="Welcome to StudentForge - Manage your tasks, attendance, and progress" />
    <link rel="icon" href="/sf-next-logo.png" type="image/png" />
    
    <!-- Unified Styles -->
    <link rel="stylesheet" href="css/styles.css" />
    
    <!-- Unified SPA Logic -->
    <script src="js/main.js" defer></script>
</head>
<body class="geist_a71539c9-module__T19VSG__variable geist_mono_8d43a2aa-module__8Li5zG__variable antialiased selection:bg-zinc-50 selection:text-black">
    <div id="view-landing" class="spa-view active">
        {landing}
    </div>
    
    <div id="view-courses" class="spa-view">
        {courses}
    </div>
    
    <div id="view-signin" class="spa-view">
        {signin}
    </div>
</body>
</html>
"""

final_html = html_template.format(
    landing=views['landing'],
    courses=views['courses'],
    signin=views['signin']
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Successfully created index.html SPA")
