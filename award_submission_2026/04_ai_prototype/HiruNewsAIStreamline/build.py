"""
Build script: Combines index.html + app.jsx into a single working HTML file.
Run: python build.py
Output: frontend/index.html (with inlined JSX)
"""

import re
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"


def build():
    # Read the template HTML
    html_path = FRONTEND_DIR / "index_template.html"
    if not html_path.exists():
        html_path = FRONTEND_DIR / "index.html"

    html = html_path.read_text(encoding="utf-8")

    # Read app.jsx
    jsx_path = FRONTEND_DIR / "app.jsx"
    jsx_content = jsx_path.read_text(encoding="utf-8")

    # Replace the external script reference with inline content
    # Look for: <script type="text/babel" src="app.jsx"></script>
    old_tag = '<script type="text/babel" src="app.jsx"></script>'
    new_tag = f'<script type="text/babel">\n{jsx_content}\n</script>'

    if old_tag in html:
        html = html.replace(old_tag, new_tag)
        print("Replaced external app.jsx reference with inline content.")
    else:
        # Append before </body>
        html = html.replace("</body>", f"{new_tag}\n</body>")
        print("Appended inline JSX before </body>.")

    # Write output
    output_path = FRONTEND_DIR / "index.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Built: {output_path} ({len(html)} bytes)")


if __name__ == "__main__":
    build()
