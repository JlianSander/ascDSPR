#!/usr/bin/bash
#set -x

# Created by Julian Sander, 2025/09/10


#/////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////---- PARAM ----////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////

#counter of instances with same general result [YES/NO]
num_same_result=0
#counter of instances with same extensions
num_same_extension=0
#counter of instances compared
num_instances_comp=0
#counter of instances total
num_instances_total=0
#counter of instances with invalid extension
num_instances_invalid_extension_solver1=0
num_instances_invalid_extension_solver2=0
#counter of instances with empty files
num_instances_empty=0 #instances with at least one solver having a empty file
num_instances_empty_1=0
num_instances_empty_2=0
#counter of instances with different soultions and solver 1 returned NO
num_instance_diff_solver1_NO=0
#counter of instances with empty certificate
num_instance_empty_certificate_solver_1=0
num_instance_empty_certificate_solver_2=0
num_instance_empty_certificate_both=0

#/////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////---- FUNC ----/////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////

function Check_Certificate () {
    file_cc=$1
    file_raw_cc=${1##*/}
    file_2_cc=$2
    file_2_raw_cc=${2##*/}
    #echo "Check_Certificate"
    #echo "File: $file_cc"
    #echo "File Raw: $file_raw_cc"

    #get result of files
    result_cc=$(sed {$num_line_result_solver_1"q;d"} < $file_cc)
    result_2_cc=$(sed {$num_line_result_solver_1"q;d"} < $file_2_cc)

    #get extension from solver 1 (special files)           
    raw_ext_cc=$(sed -n {$next_line_result_solver_1',${p;}'} < $file_cc)
    raw_ext_2_cc=$(sed -n {$next_line_result_solver_1',${p;}'} < $file_2_cc)
    ext_cc=$(echo $raw_ext_cc | sed -e s/'\r'/' '/g -e s/'\n'/' '/g) # parse extensions in several lines
    ext_2_cc=$(echo $raw_ext_2_cc | sed -e s/'\r'/' '/g -e s/'\n'/' '/g)

    #echo "Raw_ext = $raw_ext_cc"
    #echo "Ext = $ext_cc"

    # check if any of the files is empty, in that case comparison is meaningless
    if [ -z "$result_cc" ]; then
        return
    fi

    if [ -z "$result_2_cc" ]; then
        return
    fi
    
    #check if certificate in solver 1 is empty
    if [  $(expr length "$ext_cc") -lt 3 ]; then
        cert_1_empty=true
    else
        cert_1_empty=false
    fi

    #check if certificate in solver 2 is empty
    if [  $(expr length "$ext_2_cc") -lt 3 ]; then
        cert_2_empty=true
    else
        cert_2_empty=false
    fi

    if [ "$cert_1_empty" = true ]; then
        if [ "$cert_2_empty" = false ]; then
            if [ "$no_print" = false ]; then
                echo "Empty Certificate Solver 1: $file_raw_cc"
                echo "$result_cc $ext_cc"
            fi
            ((num_instance_empty_certificate_solver_1++))
        else
            if [ "$no_print" = false ]; then
                echo "Empty Certificate both Solver: $file_raw_cc"
                echo "$result_cc $ext_cc"
            fi
            ((num_instance_empty_certificate_both++))
        fi
    else
        if [ "$cert_2_empty" = true ]; then
            if [ "$no_print" = false ]; then
                echo "Empty Certificate Solver 2: $file_2_raw_cc"
                echo "$result_2_cc $ext_2_cc"
            fi
            ((num_instance_empty_certificate_solver_2++))
        fi
    fi
}


#/////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////---- MAIN ----/////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////

if [ -n "$6" ]
  then
    input_no_print=$6
else
    input_no_print="NO"
fi
if [[ ($input_no_print == 'Y') || ($input_no_print == 'YES')]]
  then
    no_print=true;
else
    no_print=false;
fi

if [ "$no_print" = false ]; then
    echo "Validate v4.2"
    echo "created by Julian Sander"
    echo "for no print use ./validate.sh [path_solver_1] [path_solver_2] 1 N N Y"
fi

if [ -z "$1" ]
  then
    echo "Path to the directory for the 1st solver: "
    read dir_1
    echo " "
else
    dir_1=$1
fi
# Check if the target is a directory
if [ ! -d "$dir_1" ]; then
    echo "$dir_1"
    echo "Path does not lead to a directory"
    exit 1
fi

if [ -z "$2" ]
  then
    echo -e "Path to the directory for the 2nd solver: "
    read dir_2
    echo " "
else
    dir_2=$2
fi
# Check if the target is a directory
if [ ! -d "$dir_2" ]; then
    echo "$dir_2"
    echo "Path does not lead to a directory"
    exit 1
fi

if [ -z "$3" ]
  then
    echo -e "In which line is the result written for files of solver 1: "
    read num_line_result_solver_1
    echo " "
else
    num_line_result_solver_1=$3
fi
next_line_result_solver_1=$((num_line_result_solver_1+1))

if [ -z "$4" ]
  then
    echo -e "Check for empty certificates in YES-result of solver 1 [Y/N]: "
    read input_check_cert_YES
    echo " "
else
    input_check_cert_YES=$4
fi
if [[ $input_check_cert_YES == 'Y' ]]
  then
    check_cert_YES=true;
else
    check_cert_YES=false;
fi

if [ -z "$5" ]
  then
    echo -e "\nCheck for empty certificates in NO-result of solver 1 [Y/N]: "
    read input_check_cert_NO
    echo " "
else
    input_check_cert_NO=$5
fi
if [[ $input_check_cert_NO == 'Y' ]]
  then
    check_cert_NO=true;
else
    check_cert_NO=false;
fi

if [ "$no_print" = false ]; then
    if [ "$check_cert_YES" = true ]; then
        echo "check_cert_YES: true"
    else
        echo "check_cert_YES: false"
    fi
    if [ "$check_cert_NO" = true ]; then
        echo "check_cert_NO: true"
    else
        echo "check_cert_NO: false"
    fi
fi

#iterate through files of solver_1
for FILE in "$dir_1"/*.out; do 
    #count instance
    ((num_instances_total++))

    #echo $FILE; 
    #echo "${FILE##*/}"

    FILE_2=$(find $dir_2 -name "${FILE##*/}")
    #echo $FILE_2

    #only compare for files that exist in both dir's
    if [ -z "$FILE_2" ]; then
        continue
    fi

    is_Empty=false

    #read result of solver 1 (special files)
    result_1=$(sed {$num_line_result_solver_1"q;d"} < $FILE)

    # don't count aborted(empty) cases
    if [ -z "$result_1" ]; then
        if [ "$no_print" = false ]; then
            echo "Empty File: $FILE"
        fi
        ((num_instances_empty_1++))
        is_Empty=true
    else
        if [ "$result_1" = "NO" ]; then
            if [ "$check_cert_NO" = true ]; then
                Check_Certificate $FILE $FILE_2
            fi
        fi

        if [ "$result_1" = "YES" ]; then
            if [ "$check_cert_YES" = true ]; then
                Check_Certificate $FILE $FILE_2
            fi
        fi
    fi

    #read result of solver 2
    result_2=$(sed '1q;d' < $FILE_2)
    # don't count aborted(empty) cases
    if [ -z "$result_2" ]; then
        if [ "$no_print" = false ]; then
            echo "Empty File: $FILE_2"
        fi
        ((num_instances_empty_2++))
        is_Empty=true
    fi

    if [ "$is_Empty" = true ]; then
        ((num_instances_empty++))
        continue
    fi

    #count compared instance
    ((num_instances_comp++))

    #compare result
    char_1=${result_1:0:1}
    char_2=${result_2:0:1}
    if [ "$char_1" = "$char_2" ]; then
        ((num_same_result++))
    else
        if [ "$result_1" = "NO" ]; then
            ((num_instance_diff_solver1_NO++))
            #solver 1 returned NO and extension
            #get extension from solver 1 (special files)           
            raw_ext=$(sed -n {$next_line_result_solver_1',${p;}'} < $FILE)
            ext=$(echo $raw_ext | sed -e s/'\r'/' '/g -e s/'\n'/' '/g) # parse extensions in several lines
            
            #check if extension in solver 1 is valid
            if [  $(expr length "$ext") -gt 3 ]; then
                # extension is not empty
                if [ "$no_print" = false ]; then
                    echo "Diff. result: ${FILE##*/} solver1: $ext"
                fi
#                Check_Extension $FILE $dir_prob
#                if [ "$is_Valid" != true ]; then
#                    ((num_instances_invalid_extension_solver1++))
#                fi
            else
#                ((num_instances_invalid_extension_solver1++))
                if [ "$no_print" = false ]; then
                    echo "Diff. result + empty ext: ${FILE}"
                fi
            fi
        else
            #solver 2 returned NO and extension
            #get extension from solver 2
            raw_ext_2=$(sed -n '2,${p;}' < $FILE_2) 
            ext_2=$(echo $raw_ext_2 | sed -e s/'\r'/' '/g -e s/'\n'/' '/g) # parse extensions in several lines
            
            #check if extension in solver 2 is valid
            if [  $(expr length "$ext_2") -gt 3 ]; then
                # extension is not empty
                if [ "$no_print" = false ]; then
                    echo "Diff. result: ${FILE##*/} solver2: $ext_2"
                fi
#                Check_Extension $FILE_2 $dir_prob
#                if [ "$is_Valid" != true ]; then
#                    ((num_instances_invalid_extension_solver2++))
#                fi
            else
#                ((num_instances_invalid_extension_solver2++))
                if [ "$no_print" = false ]; then
                    echo "Diff. result + empty ext: ${FILE_2}"
                fi
            fi
        fi
        continue
    fi
    # get extension from solver 1 (special files)
    raw_ext=$(sed -n {$next_line_result_solver_1',${p;}'} < $FILE)
    # if no extension given, nothing to compare
    if [ -z "$raw_ext" ]; then
        continue
    fi
    ext=$(echo $raw_ext | sed -e s/'\r'/' '/g -e s/'\n'/' '/g) # parse extensions in several lines

    #get extension from solver 2
    raw_ext_2=$(sed -n '2,${p;}' < $FILE_2)
    ext_2=$(echo $raw_ext_2 | sed -e s/'\r'/' '/g -e s/'\n'/' '/g) # parse extensions in several lines

    #compare extension
    if [ "$ext" = "$ext_2" ]; then
        ((num_same_extension++))
    #else
       #echo "Different extension: ${FILE##*/}"
    fi

done

#calculate number of instances with different results
num_diff_result=$((num_instances_comp-num_same_result))
#num_diff_solver2_NO=$((num_diff_result-num_instance_diff_solver1_NO))
#num_incorrect_NO_solver1=$((num_instances_invalid_extension_solver1))
#num_incorrect_NO_solver2=$((num_instances_invalid_extension_solver2))
#num_incorrect_YES_solver1=$((num_diff_solver2_NO-num_instances_invalid_extension_solver2))
#num_incorrect_YES_solver2=$((num_instance_diff_solver1_NO-num_instances_invalid_extension_solver1))
#num_incorrect_solver1=$((num_incorrect_NO_solver1+num_incorrect_YES_solver1))
#num_incorrect_solver2=$((num_incorrect_NO_solver2+num_incorrect_YES_solver2))

if [ "$no_print" = false ]; then
    echo "Same results                  [1/compared]:                   $num_same_result/$num_instances_comp" 
    echo "Same extensions               [1/same result]:                $num_same_extension/$num_same_result"
    echo "Empty files (min. one solver) [1/total]:                      $num_instances_empty/$num_instances_total"
    echo "Empty files of solver1        [1/total]:                      $num_instances_empty_1/$num_instances_total"
    echo "Empty files of solver2        [1/total]:                      $num_instances_empty_2/$num_instances_total"
    #echo "Solver 1 invalid extensions   [1/solver 1 NO]                 $num_instances_invalid_extension_solver1/$num_instance_diff_solver1_NO"
    #echo "Solver 2 invalid extensions   [1/solver 2 NO]                 $num_instances_invalid_extension_solver2/$num_diff_solver2_NO"
    #echo "incorrect solutions solver 1                                  $num_incorrect_solver1"
    #echo "incorrect solutions solver 2                                  $num_incorrect_solver2"
    echo "Empty certificates both solvers [1/total]:                    $num_instance_empty_certificate_both/$num_instances_total"
    echo "Empty certificates solver 1, solver 2 not:                    $num_instance_empty_certificate_solver_1"
    echo "Empty certificates solver 2, solver 1 not:                    $num_instance_empty_certificate_solver_2"
    echo "solver 1 NO solver 2 YES      [1/diff result]                 $num_instance_diff_solver1_NO/$num_diff_result"
else
    if [[ $num_diff_result == '0' ]]; then
        echo "VALID"
    else
        echo "INVALID"
    fi
fi