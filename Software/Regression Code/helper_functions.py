import math 
import time 
import cantools
import cantools.database
import os 
from CANBase import CANInterface 
from data.message_data import MessageData

def update_hfi_message(original_message, output_to_change, updated_value): 
      original_message.data[f"HARDINJ_output{output_to_change}Control"] = updated_value

#####################  Test for update_hfi_message ########################

#def test_update_hfi_message(): 
    #hfi_dbc = os.path.join(os.getcwd(), r'Software\DBC Tools\HardwareInjector.dbc')
    #hfi_db = cantools.database.load_file(hfi_dbc)
    #hfi_command_mux0 = MessageData(message=hfi_db.get_message_by_name("HARDINJ_command"), 
                                   #data={
                                    #'HARDINJ_mux': 0,
                                    #'HARDINJ_output1Control': 0, # unknown pin
                                    #'HARDINJ_output2Control': 0, # unknown pin 
                                    #'HARDINJ_output3Control': 0, # APPS main (AV3)
                                    #'HARDINJ_output4Control': 0, # APPS tracking (AV4)
                                    #'HARDINJ_output5Control': 0, # INJ_LS1
                                    #'HARDINJ_output6Control': 127, # Brake pressure front (AV6)
                                   #})
    #print(hfi_command_mux0)
    #update_hfi_message(hfi_command_mux0, 1, 200)
    #print(hfi_command_mux0)
