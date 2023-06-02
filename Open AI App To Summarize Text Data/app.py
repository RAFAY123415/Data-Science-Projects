import os
from dotenv import load_dotenv
import zipfile
import requests
from flask import Flask, render_template, request
import shutil
import openai


# Load environment variables from .env file
#load_dotenv()

# Get API key from environment variable
openai.api_key ='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'

#'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'

#'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'

# Create Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# The request will be sent from javascript to this route to execute the function
@app.route('/submit', methods=['POST'])
def analyze():
    try:
        # Retrieve the uploaded ZIP file from the request
        zip_file = request.files['code_zip']
        

        # Extract the contents of the ZIP file to a temporary directory
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall('tmp/')

        # Combine the code from all extracted files into a single string
        code = ''
        for filename in os.listdir('tmp'):
            with open(os.path.join('tmp', filename), 'r') as f:
                code += f.read()
        
        # Delete the temporary directory and its contents
        shutil.rmtree('tmp/')
        code = ' '.join(code.split())
        

        # Make a request to the OpenAI API for code completion
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f'Summarize the main points and key arguments presented in the essay: {code}',
            temperature=0.6,
            max_tokens=1000,
            )
        
        # If the request successfully completed then it will return the response successfully
        if response['choices'][0]['finish_reason'] == 'completed':
            return response['choices'][0]['text']
        
        # If the request is successfully completed and the text we have given as input
        #  summerize before the the token limit complete successfully
        elif response['choices'][0]['finish_reason'] == 'stop':
            return response['choices'][0]['text']
        
        # If the API request failed 
        else:
            return "Error: API request failed"
    # If there is an error in Try it will give an exception
    except Exception as e:
        return "Error: An unexpected error occurred"

if __name__ == "__main__":
    # Run the Flask application in debug mode on port 5000 by default
    app.run(debug=True)

