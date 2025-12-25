#!/bin/bash
# Universal Metadata Extractor - exiftool wrapper with forensic output
exiftool -a -u -g1 -w json "$1" | jq '.[] | {Source: .SourceFile, Date: .DateTimeOriginal // .CreateDate, Software: .Software, GPS: .GPSLatitude // empty}' > metadata_$(basename "$1").json
echo "Metadata extracted: metadata_$(basename "$1").json"
