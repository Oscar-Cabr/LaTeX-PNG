# LaTeX code to PNG images!

This repo handle a python script that takes from a .tex file whatever you want to make in latex, and convert it into an image.

So you can take latex wherever you want!

## How to use it?

Just execute the file giving it as argument the .tex file you want to convert, then the route to the file you want as result.
For example:

<pre>
python3 latex_to_png.py texcode/example.tex images/example.png
</pre>

## Prerequisites

* <pre>python</pre> Python interpreter, to execute the main script.
* <pre>texlive-core  texlive-latexextra</pre> The base TeX Live distribution, to compiles .tex files into .pdf, also additional LaTeX packages to ensure that minimal and standalone documents can compile succesfully.
* <pre>poppler</pre> PDF rendering utilities, including pdftocairo, so it converts the pdf generated file into a .png image, as preferred method.
* <pre>imagemagick</pre> A suite of image manipulation tools, it provides the convert command as a fallback in case pdftocairo fails.
* <pre>ghostscript</pre> A PostScript and PDF rendering engine, it improves PDF conversion and transparency handling.

You can install them all in ArchLinux by the following sentence:

<pre>
sudo pacman -S --needed python texlive-core texlive-latexextra poppler imagemagick ghostscript
</pre>

## How it works

In general, the flow of the script can be summarized into the next following steps:

1. Reads LaTeX input from a .tex file. The file must include only the fragment of text you want to convert. It can be a math mode with $, something in between a scope align, or whatever preferred. All the policy for document type, begin document, importing packages and so its handled on the script. So the input is pasated into a fully prepared latex file that'll be compiled.
2. Compiles the input source into a PDF using pdflatex, for this it creates a temporal scope.
3. Converts the resulting PDF into a PNG image.
