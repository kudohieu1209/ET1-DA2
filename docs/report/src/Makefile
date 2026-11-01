# Makefile to compile LaTeX report with XeLaTeX

all:
	xelatex -interaction=nonstopmode main.tex
	xelatex -interaction=nonstopmode main.tex
	cp main.pdf ../Bao_cao_DATK2_ATmega16_DHT11.pdf

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.synctex.gz

.PHONY: all clean
