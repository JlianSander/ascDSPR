#!/usr/bin/bash
#set -x

# Created by Julian Sander, 2025/09/10

echo "countResults v1.0"
echo "created by Julian Sander"

if [ "$#" -ne 2 ]
  then
    echo "countResults [INPUT path asc folders] [OUTPUT path csv-file]"
    exit 1    
fi

dir_1=$1
output_file=$2

echo "solver_name,task,dataset,number_files,number_empty,number_yes,number_no" > $output_file

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
                result_1=$(sed {1"q;d"} < $FILE)
                if [ -z "$result_1" ]; then
                    #echo "Empty File: $FILE"
                    ((num_instances_empty++))
                else
                    #echo "Not Empty: $FILE"
                    if [ "$result_1" = "YES" ]; then
                        ((num_instances_yes++))
                    fi
                    if [ "$result_1" = "NO" ]; then
                        ((num_instances_no++))
                    fi
                fi
            done

            echo "$solverName,$probName,$dataSetName,$num_instances,$num_instances_empty,$num_instances_yes,$num_instances_no" >> $output_file
        done
    done
done