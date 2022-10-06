#!/usr/bin/env bash
# This script prepares the data folders for the CommonVoice.

set -e
set -o pipefail

stage=0
prefix=commonvoice
version="cv-corpus-9.0-2022-04-27"
nj=80

. ./path.sh || exit 1;
. ./cmd.sh || exit 1;
. ./utils/parse_options.sh || exit 1;

which python3
if [ $# -ne 2 ]; then
  echo "Usage: $0 [options] <commonvoice-root> <data-dir>"
  echo " e.g.: $0 /data/commonvoice data/"
  echo "Options:"
  echo "  --stage <stage>    # Script stage."
  exit 1
fi

commonvoice_root=`realpath $1`
data_dir=$2
commonvoice_train=$data_dir/train
commonvoice_dev=$data_dir/dev
commonvoice_test=$data_dir/test

if [ $stage -le 0 ]; then
  echo "$0: Preparing CommonVoice"
  # Processes all data.
  mkdir -p $commonvoice_{train,dev,test} || exit 1;
  python3 ./prepare_commonvoice.py --prefix=commonvoice --version=$version \
    --input_dir=$commonvoice_root --train_dir=$commonvoice_train \
    --dev_dir=$commonvoice_dev --test_dir=$commonvoice_test || exit 1;
  utils/fix_data_dir.sh $commonvoice_train || exit 1;
  utils/fix_data_dir.sh $commonvoice_dev || exit 1;
  utils/fix_data_dir.sh $commonvoice_test || exit 1;
fi

if [ $stage -le 1 ]; then
  # Generate segments, utt2dur, reco2dur for training set
  utils/data/get_utt2dur.sh --nj $nj --cmd "$train_cmd" $commonvoice_train
  utils/data/get_reco2dur.sh --nj $nj --cmd "$train_cmd" $commonvoice_train
  awk '{ print $1, $1, 0, $2 }' $commonvoice_train/utt2dur >$commonvoice_train/segments
  utils/fix_data_dir.sh $commonvoice_train || exit 1;
  utils/validate_data_dir.sh --no-feats $commonvoice_train || exit 1;
  utils/validate_data_dir.sh --no-feats $commonvoice_dev || exit 1;
  utils/validate_data_dir.sh --no-feats $commonvoice_test || exit 1;
fi
