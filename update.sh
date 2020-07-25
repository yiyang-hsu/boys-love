#! /usr/bin/env bash
find static/txt -maxdepth 1 -name "*.txt" -exec bash -c 'sed -i "s/“/「/g" "$1" && sed -i "s/”/」/g" "$1" ' - '{}' \;
python3 run.py;
find content/ -name "*.zht.md" -exec bash -c 'rm "$1"' - '{}' \;
find content/ -name "*.md" -exec bash -c 'opencc -i "$1" -o "${1%.md}".zht.md -c s2twp.json' - '{}' \;
cd static/txt/
find . -maxdepth 1 -name "*.txt" -exec bash -c 'opencc -i "$1" -o zht/`echo ${1%.txt} | opencc -c s2twp.json`.txt -c s2twp.json' - '{}' \;
cd ../../
/usr/bin/env hugo -D -d shota