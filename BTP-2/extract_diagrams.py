import re
import os
import subprocess
import shutil

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def extract_diagrams():
    report_path = 'final_report.tex'
    if not os.path.exists(report_path):
        print(f"Error: {report_path} not found.")
        return

    # Clear existing directory
    out_dir = 'diagrams_extracted'
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    with open(report_path, 'r') as f:
        content = f.read()

    # Extract preamble
    preamble_match = re.search(r'(\\documentclass.*?\\begin\{document\})', content, re.DOTALL)
    if not preamble_match:
        print("Preamble not found")
        return
    preamble = preamble_match.group(1)
    
    # Change documentclass to standalone for tight crops
    preamble = re.sub(r'\\documentclass\[.*?\]\{article\}', r'\\documentclass[preview,border=40pt]{standalone}', preamble)
    # Remove things that break standalone or are unnecessary
    preamble = re.sub(r'\\geometry\{.*?\}', '', preamble)
    preamble = re.sub(r'\\pagenumbering\{.*?\}', '', preamble)
    preamble = re.sub(r'\\titleformat.*?\n', '', preamble)
    
    # Find all figure environments to get captions
    figures = re.findall(r'(\\begin\{figure\}.*?\\end\{figure\})', content, re.DOTALL)
    
    for i, fig in enumerate(figures):
        # Extract tikzpicture
        tikz_match = re.search(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', fig, re.DOTALL)
        if not tikz_match:
            continue
        tikz_code = tikz_match.group(1)
        
        # Extract caption for naming
        caption_match = re.search(r'\\caption\{([^}]*)\}', fig)
        if caption_match:
            caption_text = caption_match.group(1)
            # Remove LaTeX commands from caption for filename
            clean_caption = re.sub(r'\\[a-zA-Z]+', '', caption_text)
            name = slugify(clean_caption)[:50]
        else:
            name = f'diagram_{i+1}'
            
        tex_filename = f'{name}.tex'
        with open(tex_filename, 'w') as f:
            f.write(preamble + '\n' + tikz_code + '\n' + '\\end{document}')
        
        print(f"Compiling {name}...")
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Convert to PNG (300 DPI)
            print(f"Converting {name} to PNG...")
            subprocess.run(['pdftoppm', '-png', '-r', '300', '-singlefile', f'{name}.pdf', f'{out_dir}/{name}'], capture_output=True)
            print(f"Saved: {out_dir}/{name}.png")
        else:
            print(f"Error compiling {name}")
            
        # Clean up all temp files
        for ext in ['.tex', '.aux', '.log', '.pdf']:
            if os.path.exists(name + ext):
                os.remove(name + ext)

if __name__ == "__main__":
    extract_diagrams()
