#! /bin/sh

for fullname in $(find $1 -name '*.xml.gz'); do
    filename=$(basename "$fullname")
    filename="${filename%.xml.gz}"
    gzcat $fullname | python xml2text.py /dev/stdin | python clean_text.py > $2/$filename.clean.txt
done
