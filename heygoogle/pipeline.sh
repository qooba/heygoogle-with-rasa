#!/bin/bash

lang=$1
echo "Processing $lang"

if (($(git diff-tree --no-commit-id --name-only -r $CI_COMMIT_SHA | grep ^$lang/ | wc -l) > 0)); then
   echo "Training $lang"
   cd $lang
   rasa train
   rasa test
   cd ..
   python3 pipeline.py --language $lang
else
   echo "Nothing changed for $lang"
fi
