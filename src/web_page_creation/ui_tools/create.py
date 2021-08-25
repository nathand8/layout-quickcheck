def ui_tools_js():
    js_string = ""
    with open('src/web_page_creation/ui_tools/template.js', 'r') as f:
        js_string = f.read()
    return js_string

def ui_tools_html():
    html_string = ""
    with open('src/web_page_creation/ui_tools/template.html', 'r') as f:
        html_string = f.read()
    return html_string