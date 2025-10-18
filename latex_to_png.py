import os
import sys
import subprocess
import tempfile
import shutil

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Command failed: {cmd}", file=sys.stderr)
        print(result.stderr.decode(), file=sys.stderr)
        sys.exit(result.returncode)
    return result
def read_input(source_path):
    if source_path == "-":
        return sys.stdin.read()
    with open(source_path,"r",encoding="utf-8") as f:
        return f.read()
def contains_begin_document(tex):
    return "\\begin{document}" in tex
def wrap_if_needed(tex):
    if contains_begin_document(tex):
        return tex
    return r"""\documentclass[varwidth=true,border=8pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{courier}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{amsmath}
\usepackage{amssymb}
\lstset{
  basicstyle=\ttfamily\footnotesize,
  breaklines=true,
  numbers=left,
  numberstyle=\tiny,
  frame=single
}
\begin{document}
""" + tex + "\n\\end{document}\n"

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 latex_to_png.py <input.tex | -> <output.png>", file=sys.stderr)
        sys.exit(1)
    input_path,output_path=sys.argv[1],sys.argv[2]
    tex_code = read_input(input_path)

    tmpdir = tempfile.mkdtemp(prefix="latex2png_")
    tex_file = os.path.join(tmpdir,"input.tex")
    pdf_file = os.path.join(tmpdir,"input.pdf")
    png_file = os.path.join(tmpdir,"output.png")

    with open(tex_file,"w",encoding="utf-8") as f:
        f.write(wrap_if_needed(tex_code))
    cmd_pdflatex = "pdflatex -interaction=nonstopmode -halt-on-error input.tex"
    run_cmd(cmd_pdflatex, cwd=tmpdir)
    cmd_pdftocairo = "pdftocairo -png -singlefile -transp input.pdf output"
    try:
        run_cmd(cmd_pdftocairo,cwd=tmpdir)
    except SystemExit:
        cmd_convert = "convert -density 300 input.pdf -quality 100 -background none -alpha remove -alpha off output.png"
        run_cmd(cmd_convert, cwd=tmpdir)
    shutil.copy2(png_file,output_path)
    print(f"[OK] Image written to {output_path}")
    shutil.rmtree(tmpdir)
if __name__ == "__main__":
    main()
