# Code Analysis Website
This website allows a user to upload a .zip file containing code, extracts the code, sends it to the OpenAI ChatGPT API for analysis, and displays the response.
## Requirements
- Python 3
- Flask
- OpenAI API key
- Heroku Hosting
## How it works
1. The user uploads a .zip file containing code through an HTML form.
2. The /analyze route handles the file upload. It uses the zipfile library to extract the .zip file into a temporary directory.
3. The code reads all the files in the temporary directory and concatenates the text into a single string.
4. A request is made to the OpenAI /completions endpoint with the ChatGPT engine using the concatenated code string as the prompt. The OpenAI API key is passed in the Authorization header.
5. The response from the OpenAI API is returned and displayed on the web page.