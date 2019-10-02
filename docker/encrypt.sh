#!/bin/bash

if [ $# -eq 0 ]
then
  echo "Usage: $0 <in-file>"
  exit 1
fi

FILE=$1

if [ ! -f $FILE ]
then
  echo "File ${FILE} not found."
  exit 1
fi

gpg --cipher-algo=AES256 --armor -o ${FILE}.enc -c ${FILE}
