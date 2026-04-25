from analysis import *
from pathlib import Path
import re

output_file = "./data/Room Occupancy Signal Dashboard.html"


# ---------------------------------------------------
# FUNCTION TO EXTRACT BODY CONTENT FROM HTML FILE
# ---------------------------------------------------
def extract_plotly_div(html_text):
    """
    Extract useful Plotly div/script content from saved Plotly HTML.
    """
    match = re.search(r"<body>(.*?)</body>", html_text, re.DOTALL)
    if match:
        return match.group(1)
    return html_text


# ---------------------------------------------------
# LOAD FIGURES
# ---------------------------------------------------
plots_html = []

for measurement in MEASUREMENTS_STRINGS:
    file = f'./data/{measurement}.html'
    title= f'{measurement} Data'
    html = Path(file).read_text(encoding="utf-8")
    content = extract_plotly_div(html)

    plots_html.append(f"""
    <div class="panel">
        <div class="title">{title}</div>
        {content}
    </div>
    """)


# ---------------------------------------------------
# BUILD FINAL HTML
# ---------------------------------------------------
final_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Scientific Plot Dashboard</title>

<style>
body {{
    margin: 0;
    padding: 30px;
    background: #f4f6f8;
    font-family: Arial, Helvetica, sans-serif;
}}

h1 {{
    text-align: center;
    color: #1c2833;
    margin-bottom: 35px;
    font-size: 34px;
    letter-spacing: 1px;
}}

.dashboard {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 22px;
}}

.panel {{
    background: white;
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    border: 1px solid #dfe6e9;
}}

.title {{
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid #dfe6e9;
}}

.plotly-graph-div {{
    width: 100% !important;
    height: 520px !important;
}}
</style>

</head>

<body>

<h1>📊 Room Occupancy Signal Dashboard</h1>

<div class="dashboard">
    {''.join(plots_html)}
</div>

</body>
</html>
"""


# ---------------------------------------------------
# SAVE
# ---------------------------------------------------
Path(output_file).write_text(final_html, encoding="utf-8")

print(f"Created: {output_file}")