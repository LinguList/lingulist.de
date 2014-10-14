PUBLIC_ADDRESS = pirxru@pirx.ru:obraz/public_html

default: build

build:
	cd _scripts; python update_bib.py; cd ..
	obraz build
	cd cv; xelatex cv_german.tex; cd ..;
	sh copy_stuff.sh
publish:
	rsync -avz --delete _site/ $(PUBLIC_ADDRESS)

clean:
	rm -fr _site

