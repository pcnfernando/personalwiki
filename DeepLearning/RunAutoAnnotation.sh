#!/usr/bin/env bash

source ~/tensorflow/bin/activate

echo "Running Auto-annotation Generator"
echo Total Number of Argument Passed: "$#"
CHECKPOINT_PATH="${HOME}/tensorflow/models/im2txt/im2txt/model/train/model.ckpt-2000000"
VOCAB_FILE="${HOME}/tensorflow/models/im2txt/im2txt/data/word_counts.txt"
IMAGE_FILE=$1
echo "Checkpoint Path: "$CHECKPOINT_PATH
echo "Vocabulary Path: "$VOCAB_FILE

cd ~/tensorflow/models/im2txt

# Run inference to generate captions.
bazel-bin/im2txt/run_inference \
  --checkpoint_path=${CHECKPOINT_PATH} \
  --vocab_file=${VOCAB_FILE} \
  --input_files=${IMAGE_FILE}

