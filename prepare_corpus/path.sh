export MAMMOTH_ROOT=/seasalt-t4gpu-01/cjaik/mammoth
export KALDI_ROOT=$MAMMOTH_ROOT/kaldi
[ -f $KALDI_ROOT/tools/env.sh ] && . $KALDI_ROOT/tools/env.sh
export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$PWD:$PATH
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh
export LC_ALL=C

# # We use Python 2.7
# VIRTUAL_ENV_DISABLE_PROMPT=true && source `pwd`/../../../venv/mammoth/bin/activate

# Add to PYTHONPATH
if [ -d "$MAMMOTH_ROOT" ] && [[ ":$PYTHONPATH:" != *":$MAMMOTH_ROOT:"* ]]; then
  export PYTHONPATH=$MAMMOTH_ROOT:$MAMMOTH_ROOT/seasalt_g2p:$PYTHONPATH
fi

# Use python3 from conda env
export python3=/seasalt-t4gpu-03/cjaik/fr_asr/venv/asr/bin/python3

# storage config
STORAGE_HOSTNAME=seasalt-t4gpu*
TASK=`echo ${PWD##*examples/} | sed 's:/:_:'`
STORAGE_PREFIX=/seasalt-t4gpu-0{1,2,3,4}/$USER/kaldi-data/egs/$TASK
