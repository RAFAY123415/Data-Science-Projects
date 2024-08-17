'''import os
from cleaningreviews import assign_reviews_data_and_convert_into_json

def convert_txt_to_json(main_directory):
    file_counter = 1
    """
    Walk through the main directory and its subdirectories to find 'Extracted_info_reviews' directories,
    process their JSON files, and save them with the directory name as the filename.

    Parameters:
    main_directory (str): The main directory to start searching for 'Extracted_info_reviews' directories.
    """
    # Walk through the main directory and its subdirectories
    for root, dirs, files in os.walk(main_directory):
        if 'Extracted_info_reviews' in dirs:
            extracted_info_reviews_path = os.path.join(root, 'Extracted_info_reviews')
            output_dir = os.path.join(root, 'Output_JSONs')

            # Create the output directory if it does not exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            # List files in the 'Extracted_info_reviews' directory
            extracted_files = os.listdir(extracted_info_reviews_path)
            for file in extracted_files:
                if file == 'unknown_ean.json':
                    continue
                if file.endswith('.json'):
                    file_input_path = os.path.join(extracted_info_reviews_path, file)
                    output_file_name = f'json_object_{file_counter}.json'
                    output_file_path = os.path.join(output_dir, output_file_name)
                    assign_reviews_data_and_convert_into_json(file_input_path, output_file_path)
                    # Increment the file counter
                    file_counter += 1


if __name__ == "__main__":
    # Get the current directory of the script
    main_directory = os.path.dirname(os.path.abspath(__file__))
    # Convert all 'data.txt' files in the directory tree to JSON
    convert_txt_to_json(main_directory)
'''
import os
from cleaningreviews import assign_reviews_data_and_convert_into_json

def convert_txt_to_json(main_directory):
    """
    Walk through the main directory and its subdirectories to find 'Extracted_info_reviews' directories,
    process their JSON files, and save them with the same name in the 'Output_JSONs' directory.

    Parameters:
    main_directory (str): The main directory to start searching for 'Extracted_info_reviews' directories.
    """
    # Walk through the main directory and its subdirectories
    for root, dirs, files in os.walk(main_directory):
        if 'Extracted_info_reviews' in dirs:
            extracted_info_reviews_path = os.path.join(root, 'Extracted_info_reviews')
            output_dir = os.path.join(root, 'Output_JSONs')

            # Create the output directory if it does not exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            # List files in the 'Extracted_info_reviews' directory
            extracted_files = os.listdir(extracted_info_reviews_path)
            for file in extracted_files:
                if file == 'unknown_ean.json' or not file.endswith('.json'):
                    continue
                
                file_input_path = os.path.join(extracted_info_reviews_path, file)
                output_file_path = os.path.join(output_dir, file)
                assign_reviews_data_and_convert_into_json(file_input_path, output_file_path)


if __name__ == "__main__":
    # Get the current directory of the script
    main_directory = os.path.dirname(os.path.abspath(__file__))
    # Convert all 'data.txt' files in the directory tree to JSON
    convert_txt_to_json(main_directory)
