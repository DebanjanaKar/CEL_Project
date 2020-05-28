Event Extraction Module:

Step1: All the raw news documents are in folder:   ~/input_test_files/real_test_files/
       Run real_test_file_preprocessing.py and get proper format of the input so that it could be feed to the next module.
       The output files is stored in the folder: ~/input_test_files/test_file_normalized/

Step2:  Run bengali_trigger_identifier.py restoring the model stored in path: ~/bengali_trigger_model
	Use input data from folder ~/fixed_length_input/   
	Get the trigger identification output in the folder: ~/iit_kgp_event_extraction_model/output/test_trigger_output/

Step3:  Run bengali_argument_identifier.py restoring the model stored in path: ~/bengali_argument_model
	Use input data from folder ~/input_test_files/test_file_normalized/
	Get the trigger identification output in the folder: ~/output/test_argument_output/


Step4: Run merging_trigger_argument.py to link triggers and arguments and store the output in folder: ~/output/merge_output


Step5: Run csv_converter_of_event_frames.py to convert the output of step4 to csv file and store them in folder: ~/output/merge_output_tabular
	
 
