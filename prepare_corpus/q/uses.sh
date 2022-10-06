#!/bin/bash
cd /home/nate/seasalt_indonesian_capstone
. ./path.sh
( echo '#' Running on `hostname`
  echo '#' Started at `date`
  echo -n '# '; cat <<EOF
qsub. The options to it are 
EOF
) >uses
time1=`date +"%s"`
 ( qsub. The options to it are  ) 2>>uses >>uses
ret=$?
time2=`date +"%s"`
echo '#' Accounting: time=$(($time2-$time1)) threads=1 >>uses
echo '#' Finished at `date` with status $ret >>uses
[ $ret -eq 137 ] && exit 100;
touch ./q/sync/done.1456779
exit $[$ret ? 1 : 0]
## submitted with:
# qsub -v PATH -cwd -S /bin/bash -j y -l arch=*64* -o ./q/uses    /home/nate/seasalt_indonesian_capstone/./q/uses.sh >>./q/uses 2>&1
