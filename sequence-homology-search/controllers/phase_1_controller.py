from models.HmmerOperator import *;

def execute_phase_1(hmm_file: str, job_name: str, iteration: int):
    # create hmm operator object
    operator: HmmerOperator = HmmerOperator(job_name);
    # operator.common_file_prefix = new_common_prefix;
    curr_iteration: int = 1;
    default_iteration: int = 5;
    if int(iteration) >= 1:
        default_iteration = iteration;
    elif int(iteration) <= 0 or int(iteration) not int:
        print("invalid iteration value, using default iteration of 5");
  
    common_file_prefix: str = f"./output/phase_1/{job_name}/iteration_{curr_iteration}";
    operator: HmmerOperator = HmmerOperator(common_file_prefix);
    for curr_iteration in range(7):
        # make_folder();
        operator.hmm_search(); 

        pass;

def __set_iteration_count():
    pass;
