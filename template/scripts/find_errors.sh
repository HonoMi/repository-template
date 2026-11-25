#!/bin/bash

INPUT_DIR=${1}

if [ "${INPUT_DIR}" = "" ]; then
  echo "Specify input directory"
  exit 1
fi


find "$INPUT_DIR"/ -type f -print0 \
  | grep -zE 'log.*txt$|qsub\.err|qsub\.out|zlog$' \
  | sort -z \
  | while IFS= read -r -d '' file; do
      if tail -n 100 "$file" \
           | ack 'Traceback|Segmentation|Error' >/dev/null 2>&1; then
        echo "$file"
      fi
    done
