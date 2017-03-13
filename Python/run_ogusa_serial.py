import ogusa
import os
import sys
from multiprocessing import Process
import time
import numpy as np

#OGUSA_PATH = os.environ.get("OGUSA_PATH", "../../ospc-dynamic/dynamic/Python")

#sys.path.append(OGUSA_PATH)

import postprocess
from execute import runner


def run_micro_macro(user_params):

    # reform = {
    # 2015: {
    #     '_II_rt1': [.09],
    #     '_II_rt2': [.135],
    #     '_II_rt3': [.225],
    #     '_II_rt4': [.252],
    #     '_II_rt5': [.297],
    #     '_II_rt6': [.315],
    #     '_II_rt7': [0.3564],
    # }, }

    # reform = {
    # 2015: {
    #     '_II_rt1': [0.045]
    # }, }

    reform = {
    2017: {
       # '_II_rt5': [.3],
       # '_II_rt6': [.3],
       # '_II_rt7': [0.3],
    }, }


    start_time = time.time()

    REFORM_DIR = "./OUTPUT_REFORM"
    BASELINE_DIR = "./OUTPUT_BASELINE"


    user_params = {'start_year':2016, 'debt_ratio_ss':1.0}

    '''
    ------------------------------------------------------------------------
        Run SS for Baseline first - so can run baseline and reform in parallel if want
    ------------------------------------------------------------------------
    '''
#    
#    output_base = BASELINE_DIR
#    input_dir = BASELINE_DIR
#    kwargs={'output_base':output_base, 'baseline_dir':BASELINE_DIR,
#            'baseline':True, 'analytical_mtrs':False, 'age_specific':True,
#            'user_params':user_params,'guid':'test',
#            'run_micro':False, 'small_open':True, 'budget_balance':False}
#    #p1 = Process(target=runner, kwargs=kwargs)
#    #p1.start()
#    runner_SS(**kwargs)
#    quit()


    '''
    ------------------------------------------------------------------------
        Run baseline
    ------------------------------------------------------------------------
    '''

    output_base = BASELINE_DIR
    input_dir = BASELINE_DIR
    kwargs={'output_base':output_base, 'baseline_dir':BASELINE_DIR,
            'test':True, 'time_path':True, 'baseline':True, 'analytical_mtrs':False, 'age_specific':True,
            'user_params':user_params,'guid':'',
            'run_micro':False, 'small_open': True, 'budget_balance':False}
    #p1 = Process(target=runner, kwargs=kwargs)
    #p1.start()
    runner(**kwargs)
    #quit()

    '''
    ------------------------------------------------------------------------
        Run reform
    ------------------------------------------------------------------------
    '''
    
    S = int(40)
    T = int(4 * S)

    tpi_firm_r_reform = np.ones(T+S)*(0.0515)
    tpi_firm_r_reform[0] = 0.0525
    tpi_firm_r_reform[1] = 0.0523
    tpi_firm_r_reform[2] = 0.0520
    tpi_firm_r_reform[3] = 0.0517

    user_params = {'start_year':2016, 'debt_ratio_ss':1.0, 'tpi_firm_r': tpi_firm_r_reform}

    output_base = REFORM_DIR
    input_dir = REFORM_DIR
    guid_iter = 'reform_' + str(0)
    kwargs={'output_base':output_base, 'baseline_dir':BASELINE_DIR,
            'test':True, 'time_path':True, 'baseline':False, 'analytical_mtrs':False, 'age_specific':True,
            'user_params':user_params,'guid':'_alt', 'reform':reform ,
            'run_micro':False, 'small_open': False, 'budget_balance':False}
    #p2 = Process(target=runner, kwargs=kwargs)
    #p2.start()
    runner(**kwargs)



    #p1.join()
    # print "just joined"
    #p2.join()

    # time.sleep(0.5)

#    ans = postprocess.create_diff(baseline_dir=BASELINE_DIR, policy_dir=REFORM_DIR)

    print "total time was ", (time.time() - start_time)
    # print ans

    # return ans

if __name__ == "__main__":
    run_micro_macro(user_params={})
