//#ifdef ASC_PARALLEL_ALL
    #include "../../include/logic/AlgorithmicShortcut_ParallelAll.h"


    //===========================================================================================================================================================
    //===========================================================================================================================================================



/* 
    static bool start_checking_rejection(uint32_t query_argument, AF &framework, ArrayBitSet &active_args, list<uint32_t> &certificate_extension,
	uint16_t numCores, ConeOfInfluence &coi)
    {
        if (numCores > 0)
        {
            omp_set_num_threads(numCores);
        }
        IPrioHeuristic *heuristic = NULL;
        heuristic = new Heuristic5();
        PriorityStackManager prio_stack;
        bool is_terminated = false;
        bool is_finished = false;
        bool is_rejected = false;
        omp_set_lock(prio_stack.lock_has_entry);
    #pragma omp parallel shared(is_rejected, is_terminated, is_finished, certificate_extension, prio_stack) \
    firstprivate(query_argument, framework, active_args, heuristic, coi)
        {
    #pragma omp single nowait
            {
                search_for_rejecting_sets_in_origin_state(framework, active_args, query_argument, is_rejected, is_terminated, certificate_extension,
                        prio_stack, heuristic, is_finished, coi);
                tools::ToolsOMP::update_is_finished(is_terminated, is_finished, prio_stack);
            }

            while (true) {
                omp_set_lock(prio_stack.lock_has_entry);
                if (tools::ToolsOMP::check_finished(is_finished, prio_stack)) {
                    omp_unset_lock(prio_stack.lock_has_entry);
                    break;
                }

                if (prio_stack.check_number_unprocessed_elements() > 0) {
                    list<uint32_t> extension = prio_stack.pop_prio_extension();

                    if (prio_stack.check_number_unprocessed_elements() > 0) {
                        omp_unset_lock(prio_stack.lock_has_entry);
                    }

                    search_for_rejecting_sets_in_reduct(query_argument, framework, active_args, is_rejected, is_terminated, extension, certificate_extension,
                        heuristic, prio_stack, coi);
                    tools::ToolsOMP::update_is_finished(is_terminated, is_finished, prio_stack);
                }
                else {
                    cout << "start_checking_rejection::exception queue empty but not finished" << endl;
                    throw new exception();
                }
            }
        }

        delete heuristic;
        return is_rejected;
    } */


    //===========================================================================================================================================================
    //===========================================================================================================================================================


    
     acceptance_result AlgorithmicShortcut_ParallelAll::try_solve(AF &framework, uint32_t query_argument)
    {

        //set 1 thread for each algorithmic shortcut
        omp_set_num_threads(10);
        bool is_terminated = false;
        vector<AlgorithmicShortcut> shortcuts;
        shortcuts.push_back(AlgorithmicShortcut_1());
    }

//#endif