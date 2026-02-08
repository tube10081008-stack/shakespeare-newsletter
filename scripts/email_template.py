def generate_email_html(data):
    theme_colors = {
        "Monday Motivation": "#2E0249", # Deep Purple
        "Tuesday Romance": "#D41F1F", # Passion Red
        "Witty Wednesday": "#D4AF37", # Gold
        "Thoughtful Thursday": "#0f0f11", # Charcoal
        "Furious Friday": "#550000", # Blood Red
        "Weekend Wit": "#D4AF37",    # Gold
        "Sunday Reflection": "#2E0249" # Deep Purple
    }
    
    # Extract Theme Color
    theme_name = data.get("title", "").split("(")[0].strip()
    primary_color = "#2E0249" # Default
    for key, color in theme_colors.items():
        if key in theme_name:
            primary_color = color
            break
            
    # Helper for preview list
    preview_html = ""
    if isinstance(data.get("weekly_preview"), list):
        for item in data["weekly_preview"]:
            preview_html += f"<li>{item}</li>"
    else:
        preview_html = f"<li>{data.get('weekly_preview', '')}</li>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.7; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }}
            .container {{ max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 2px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-top: 5px solid {primary_color}; }}
            
            .header {{ padding: 40px 30px 20px 30px; text-align: center; border-bottom: 1px solid #eee; }}
            .header-subtitle {{ font-size: 14px; color: {primary_color}; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; display: block; }}
            .header h1 {{ margin: 0; font-family: 'Georgia', serif; font-size: 26px; color: #111; letter-spacing: -0.5px; }}
            
            .intro {{ padding: 30px 40px; color: #555; font-size: 16px; border-bottom: 1px dashed #ddd; }}
            
            .section {{ padding: 30px 40px; }}
            .section-label {{ font-size: 13px; font-weight: bold; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; display: block; }}
            
            .quote-box {{ background-color: #fcfcfc; border-left: 4px solid {primary_color}; padding: 20px; margin: 10px 0; }}
            .quote-en {{ font-family: 'Georgia', serif; font-size: 19px; color: #222; font-style: italic; margin-bottom: 10px; display: block; }}
            .quote-kr {{ font-size: 15px; color: #555; display: block; margin-bottom: 10px; }}
            .quote-source {{ font-size: 13px; color: #999; text-align: right; display: block; }}
            
            .insight-box p {{ margin-bottom: 15px; }}
            .highlight {{ color: {primary_color}; font-weight: bold; }}
            
            .divider {{ height: 1px; background: #eee; margin: 0 40px; }}
            
            .perspective-box {{ background: #fafafa; padding: 25px; border-radius: 4px; }}
            .perspective-title {{ font-weight: bold; color: {primary_color}; display: block; margin-bottom: 10px; }}
            
            .preview-box ul {{ list-style: none; padding: 0; margin: 0; }}
            .preview-box li {{ padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 14px; color: #666; }}
            .preview-box li:last-child {{ border-bottom: none; }}
            
            .footer {{ background: #111; color: #666; text-align: center; padding: 30px; font-size: 12px; }}
            .footer p {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <span class="header-subtitle">The Daily Bard</span>
                <h1>{data.get("title", "Daily Wisdom")}</h1>
            </div>
            
            <div class="intro">
                {data.get("intro", "")}
            </div>
            
            <div class="section">
                <span class="section-label">🌟 Quote of the Day (오늘의 명대사)</span>
                <div class="quote-box">
                    <span class="quote-en">"{data.get("quote", {}).get("text", "")}"</span>
                    <span class="quote-kr">{data.get("quote", {}).get("translation", "")}</span>
                    <span class="quote-source">— {data.get("quote", {}).get("source", "")}</span>
                </div>
            </div>
            
            <div class="divider"></div>
            
            <div class="section">
                <span class="section-label">💡 The Insight (통찰)</span>
                <div class="insight-box">
                    <p>{data.get("insight", {}).get("context", "")}</p>
                    <p>{data.get("insight", {}).get("interpretation", "")}</p>
                    <p class="highlight">👉 적용하기: {data.get("insight", {}).get("action", "")}</p>
                </div>
            </div>
            
             <div class="divider"></div>

            <div class="section">
                <span class="section-label">🏛 Another Perspective (또 다른 시선)</span>
                <div class="perspective-box">
                    <span class="perspective-title">{data.get("second_perspective", {}).get("title", "Perspective")}</span>
                    <p style="margin:0; font-size: 15px; color: #444;">{data.get("second_perspective", {}).get("content", "")}</p>
                </div>
            </div>
            
            <div class="section">
                <span class="section-label">📅 Weekly Preview (이번 주 예고)</span>
                <div class="preview-box">
                    <ul>
                        {preview_html}
                    </ul>
                </div>
            </div>

            <div class="footer">
                <p>&copy; 2026 Shakespeare's Chronicle. All rights reserved.</p>
                <p>Designed for wisdom, delivered with grace.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    # Test
    import json
    import os
    
    data_path = os.path.join(os.path.dirname(__file__), "../src/data/latest_issue.json")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(generate_email_html(data))
    else:
        print("No data found to test.")
