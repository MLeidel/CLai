
# md2html.md_render
# Reads and converts an input .md file to HTML, and saves the HTML file
# Example:
'''
import md2html
rc = md2html.md_render("./test.md", "./test.html")
print(rc)
'''

import markdown

def md_render(inpath_md: str, outpath_html: str) -> bool:
    try:
        in_md_text = open(inpath_md, "r", encoding='utf-8').read()
    except:
        return False

    # convert MD to HTML
    H = markdown.markdown(in_md_text,
                          extensions=['tables','fenced_code'])
    # write to file
    html_path = outpath_html
    try:
        open(html_path, 'w', encoding='utf-8').write(H)
    except:
        return False

    return True
