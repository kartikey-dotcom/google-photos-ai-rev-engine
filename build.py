import re
import os

def build_single_file():
    print("Building single-file Streamlit bundle...")
    
    # 1. Read CSS files
    with open("css/tokens.css", "r", encoding="utf-8") as f:
        tokens_css = f.read()
    with open("css/main.css", "r", encoding="utf-8") as f:
        main_css = f.read()
        
    combined_css = f"<style>\n{tokens_css}\n{main_css}\n</style>"
    
    # 2. Ordered list of JS files to concatenate
    js_files = [
        "js/config/constants.js",
        "js/data/schema.js",
        "js/data/seedCorpus.js",
        "js/data/corpusStore.js",
        "js/services/BigDataConnector.js",
        "js/services/clipboardService.js",
        "js/services/geminiClient.js",
        "js/services/markdownRenderer.js",
        "js/services/promptBuilder.js",
        "js/state/canvasState.js",
        "js/components/IdleState.js",
        "js/components/LoadingSkeleton.js",
        "js/components/ErrorBanner.js",
        "js/components/Canvas.js",
        "js/components/ApiKeyCard.js",
        "js/components/SourceSelector.js",
        "js/components/WorkflowButtons.js",
        "js/components/Sidebar.js",
        "js/app.js"
    ]
    
    combined_js = ""
    for file_path in js_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Strip import statements
            content = re.sub(r'^import\s+.*?;?\s*$', '', content, flags=re.MULTILINE)
            # Strip export keywords
            content = re.sub(r'^export\s+default\s+', '', content, flags=re.MULTILINE)
            content = re.sub(r'^export\s+', '', content, flags=re.MULTILINE)
            combined_js += f"\n/* --- {file_path} --- */\n" + content + "\n"
            
    combined_js_tag = f"<script type=\"module\">\n{combined_js}\n</script>"
    
    # 3. Read index.html and inject
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    # Remove old link tags
    html = re.sub(r'<link rel="stylesheet" href="./css/tokens.css">', '', html)
    html = re.sub(r'<link rel="stylesheet" href="./css/main.css">', '', html)
    
    # Remove old script tag
    html = re.sub(r'<script type="module" src="./js/app\.js"></script>', '', html)
    
    # Inject combined CSS into <head>
    html = html.replace('</head>', f'{combined_css}\n</head>')
    
    # Inject combined JS before </body>
    html = html.replace('</body>', f'{combined_js_tag}\n</body>')
    
    with open("streamlit_index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Successfully created streamlit_index.html")

if __name__ == "__main__":
    build_single_file()
