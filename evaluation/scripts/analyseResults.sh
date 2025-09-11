#!/usr/bin/bash
#set -x

# Created by Julian Sander, 2025/09/10

echo "analyseResults v1.1"
echo "created by Julian Sander"

if [ "$#" -ne 3 ]
  then
    echo "analyseResults.sh [INPUT path asc folders] [OUTPUT summary csv-file] [OUTPUT details csv-file]"
    exit 1    
fi

dir_1=$1
output_file=$2
output_details_file=$3

echo "solver_name,task,dataset,number_files,number_empty,number_yes,number_no" > $output_file
echo "solver_name,task,dataset,instance,result" > $output_details_file

for folderSolver in "$dir_1"/*/; do
    #echo "$folderSolver"
    solverName="$(basename -- $folderSolver)"
    for folderProb in "$folderSolver"*/; do
        #echo "$folderProb"
        probName="$(basename -- $folderProb)"
        for folderDataSet in "$folderProb"*/; do
            #echo "$folderDataSet"
            dataSetName="$(basename -- $folderDataSet)"
            #echo $dataSetName
            # init variables to count files
            num_instances=0
            num_instances_empty=0
            num_instances_yes=0
            num_instances_no=0
            #iterate through .out files
            for FILE in "$folderDataSet"/*.out; do 
                ((num_instances++))
                FILE_BASENAME=$(basename -- "$FILE")
                FILE_BASENAME="${FILE_BASENAME%_1.*}"
                result_1=$(sed {1"q;d"} < $FILE)
                if [ -z "$result_1" ]; then
                    #echo "Empty File: $FILE"
                    ((num_instances_empty++))
                    echo "$solverName,$probName,$dataSetName,$FILE_BASENAME,NA" >> $output_details_file
                else
                    #echo "Not Empty: $FILE"
                    if [ "$result_1" = "YES" ]; then
                        ((num_instances_yes++))
                        echo "$solverName,$probName,$dataSetName,$FILE_BASENAME,YES" >> $output_details_file
                    fi
                    if [ "$result_1" = "NO" ]; then
                        ((num_instances_no++))
                        echo "$solverName,$probName,$dataSetName,$FILE_BASENAME,NO" >> $output_details_file
                    fi
                fi
            done

            echo "$solverName,$probName,$dataSetName,$num_instances,$num_instances_empty,$num_instances_yes,$num_instances_no" >> $output_file
        done
    done
done