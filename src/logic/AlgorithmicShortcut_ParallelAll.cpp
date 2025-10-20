
    #include "../../include/logic/AlgorithmicShortcut_ParallelAll.h"


//===========================================================================================================================================================
//===========================================================================================================================================================
    
acceptance_result AlgorithmicShortcut_ParallelAll::try_solve(AF &framework, uint32_t query_argument)
{

    //set 1 thread for each algorithmic shortcut
    omp_set_num_threads(10);
    vector<AlgorithmicShortcut> shortcuts;
    shortcuts.push_back(AlgorithmicShortcut_1());
    shortcuts.push_back(AlgorithmicShortcut_2());
    shortcuts.push_back(AlgorithmicShortcut_3());
    shortcuts.push_back(AlgorithmicShortcut_4());
    shortcuts.push_back(AlgorithmicShortcut_5());
    shortcuts.push_back(AlgorithmicShortcut_6());
    shortcuts.push_back(AlgorithmicShortcut_7());
    shortcuts.push_back(AlgorithmicShortcut_8());
    shortcuts.push_back(AlgorithmicShortcut_9());
    shortcuts.push_back(AlgorithmicShortcut_10());

    // Parallelize the loop using OpenMP
    acceptance_result result_global;
#pragma omp parallel for
    for (size_t i = 0; i < shortcuts.size(); ++i) {
        acceptance_result result_local = shortcuts[i].try_solve(framework, query_argument);
        if(result_local == acceptance_result::accepted || result_local == acceptance_result::rejected){
            #pragma omp atomic write
            result_global = result_local;
            break;
        }
    }

    return result_global;
}

