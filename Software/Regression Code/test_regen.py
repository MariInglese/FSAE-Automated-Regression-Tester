import math 
import time 
import cantools
import cantools.database
import os 
import helper_functions
from CANBase import CANInterface 
from data.message_data import MessageData


#pytest -s "C:\Users\snowb\Documents\GitHub\FSAE-Automated-Regression-Tester\Software\Regression Code\test_regen.py::test_regen_state_det_1"

def test_regen_state_det_1():  
    hfi_dbc = os.path.join(os.getcwd(), r'Software\DBC Tools\HardwareInjector.dbc')
    hfi_db = cantools.database.load_file(hfi_dbc)
    vcu_torque_dbc = os.path.join(os.getcwd(), r'Software\DBC Tools\M150_VCU_TORQUE.dbc')
    vcu_torque_db = cantools.database.load_file(vcu_torque_dbc)

    ############################### Part 1 #############################

    # Create the HFI messages
    hfi_command_mux0 = MessageData(message=hfi_db.get_message_by_name("HARDINJ_command"), 
                                   data={
                                    'HARDINJ_mux': 0,
                                    'HARDINJ_output1Control': 0, # unknown pin
                                    'HARDINJ_output2Control': 0, # unknown pin 
                                    'HARDINJ_output3Control': 0, # APPS main (AV3)
                                    'HARDINJ_output4Control': 0, # APPS tracking (AV4)
                                    'HARDINJ_output5Control': 0, # INJ_LS1
                                    'HARDINJ_output6Control': 127, # Brake pressure front (AV6)
                                   })
    
    hfi_command_mux1 = MessageData(message=hfi_db.get_message_by_name("HARDINJ_command"),
                                data={    
                                    'HARDINJ_mux': 1,
                                    'HARDINJ_output7Control': 127, # Brake pressure rear (AV7)
                                    'HARDINJ_output8Control': 0,
                                    'HARDINJ_output9Control': 0,
                                    'HARDINJ_output10Control': 0,
                                    'HARDINJ_output11Control': 0,
                                    'HARDINJ_output12Control': 0, 
                                })
    
    # Create and start CAN interface 
    can_interface = CANInterface()
    can_interface.start_send_and_update_100Hz()
    
    # Add and send HFI messages
    can_interface.add_message_100Hz(hfi_command_mux0)
    can_interface.add_message_100Hz(hfi_command_mux1)
    print(hfi_command_mux0)
    print(hfi_command_mux1)

    # Wait for a period of time for the system to catch up 
    time.sleep(1)

    # Test and compare 
    can_interface.start_receive_and_sort(can_db=vcu_torque_db, timeout=2)
    time.sleep(1)
    value = can_interface.get_signal_from_dictionary('vcu_regenState')
    time.sleep(1)
    print(value) 
    try: 
        assert(value == 1)
    except AssertionError: 
        print("-----------------Part 1 failed, continuing to Part 2-------------------")

    ############################### Part 2 #############################

    # Update HFI messages
    helper_functions.update_hfi_message(hfi_command_mux0, 3, 200) 
    helper_functions.update_hfi_message(hfi_command_mux0, 4, 200)

    # Add and send HIF messages 
    can_interface.add_message_100Hz(hfi_command_mux0)
    can_interface.add_message_100Hz(hfi_command_mux1)
    print(hfi_command_mux0)
    print(hfi_command_mux1)

    # Wait 
    time.sleep(1)

    # Test and compare
    can_interface.start_receive_and_sort(can_db=vcu_torque_db, timeout=2)
    time.sleep(1)
    value = can_interface.get_signal_from_dictionary('vcu_regenState')
    time.sleep(1)
    print(value) 
        
    try: 
            assert (value == 0)
    finally: 
            can_interface.stop_receive_and_sort()
            can_interface.stop_send_and_update_100hz()
            del can_interface
