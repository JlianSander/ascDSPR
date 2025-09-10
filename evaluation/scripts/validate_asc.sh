#!/usr/bin/bash
#set -x

# Created by Julian Sander, 2025/09/10

echo "validate_asc v1.0"
echo "created by Julian Sander"

if [ -z "$1" ]
  then
    echo "Path to the directory containing the asc_x folders: "
    read dir_1_asc
    echo " "
else
    dir_1_asc=$1
fi
# Check if the target is a directory
if [ ! -d "$dir_1_asc" ]; then
    echo "$dir_1_asc"
    echo "Path does not lead to a directory"
    exit 1
fi

if [ -z "$2" ]
  then
    echo -e "Path to the directory of the benchmark solver, containing the different iccma folders: "
    read dir_2_asc
    echo " "
else
    dir_2_asc=$2
fi
# Check if the target is a directory
if [ ! -d "$dir_2_asc" ]; then
    echo "$dir_2_asc"
    echo "Path does not lead to a directory"
    exit 1
fi


# create Output directory
dirOut_asc="$dir_1_asc"/Validation/
mkdir -p -- "$dirOut_asc"
# create overview file
fileAll_asc="$dirOut_asc"overview.log
> $fileAll_asc cat <<< " "

#iterate through files of solver_1
for folderAsc in "$dir_1_asc"/*/; do
    #echo "$folderAsc"
    ascVersion="$(basename -- $folderAsc)"
    for folderProb_asc in "$folderAsc"*/; do
        #echo "$folderProb_asc"
        probVersion_asc="$(basename -- $folderProb_asc)"
        for folderIccma_asc in "$folderProb_asc"*/; do
            echo "$folderIccma_asc"
            iccmaVersion_asc="$(basename -- $folderIccma_asc)"
            #echo $iccmaVersion_asc
            folderBenchmark_asc="$dir_2_asc"/"$iccmaVersion_asc"/
            echo $folderBenchmark_asc
            file_log_asc="$dirOut_asc""$ascVersion"_"$probVersion_asc"_"$iccmaVersion_asc".log
            > $file_log_asc cat <<< " "
            isValid_asc=$(source ./validate.sh $folderIccma_asc $folderBenchmark_asc 1 N N Y)
            echo "$ascVersion"_"$probVersion_asc"_"$iccmaVersion_asc"       $isValid_asc  >> $fileAll_asc
            source ./validate.sh $folderIccma_asc $folderBenchmark_asc 1 N N N > $file_log_asc
        done
    done
done
