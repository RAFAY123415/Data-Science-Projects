
-------------------------------------Instructions (How To Run My Gradio App) ----------------------------

------------------------------------- Setup Process And Usage -------------------------------------------

---------------------------------------RAG App Setup Guide : --------------------------------------------

This guide will show you how to run the RAG (Retrieval-Augmented Generation) application using Docker. 
This method makes it easy to run the application without worrying about installing dependencies manually. Follow the instructions below to get the app running on your system.

Prerequisites:

Docker must be installed on your system. If you don't have Docker installed, download it from website.


1. Build the Docker Image

To get started, make sure your Dockerfile is ready with all necessary configurations. Then, build 
the Docker image by running the following command in your terminal (from the directory containing 
the Dockerfile) :

docker build -t gradio-app .

This command will create a Docker image named gradio-app. I am providing Docker file with all 
dependencies.

2. Verify the Image Works Locally

After building the Docker image, run the following command to test the application locally and make 
sure everything works as expected:

docker run -p 8000:8000 gradio-app

Once the command runs successfully, open your web browser and visit http://localhost:8000. 
You should see the application running. If the page loads, everything is set up correctly.

3. Save the Docker Image as a File

To share the Docker image with others, you can save it as a .tar file. This can be done by running 
the following command:

docker save -o gradio-app.tar gradio-app

This command will create a file named gradio-app.tar containing your Docker image.

4. Share the Docker Image File

Now you can send the gradio-app.tar file to others through file-sharing services like Google Drive, 
Dropbox, or via email (if the file size is manageable).

5. Load the Docker Image on Another System

Once someone receives the gradio-app.tar file, they need to load the image into Docker on their own 
system. They can do this by running the following command:

docker load -i gradio-app.tar

This will load the Docker image onto their system and make it available for use.

6. Run the Docker Image

After loading the image, they can run the Docker container with the following command:

docker run -p 8000:8000 gradio-app

This will start the application and expose it on port 8000. They can then access the application in 
their browser by visiting http://localhost:8000.


------------------------------------------- Important Instructions : ------------------------------------

1) To upload more documents, simply run the commands in RAG_Application_Development.ipynb and provide 
the directory path. All documents must be stored in that directory, and currently, all documents 
are loaded into the Chroma_Storage database already.

2) In the .env file, I have provided my API key, so you can run the application easily.

3) To run the application locally, simply use the command python Gradio_App.py and access 
it at http://127.0.0.1:8000.

4) If you want to build the Docker container, simply use the command provided above to build it, 
and then run it at http://127.0.0.1:8000. I have already set up the container and will send 
you a .tar file so you can load it and run the app directly.

5) All the required packages are listed in the requirements.txt file. To install them, run the 
following command: pip install -r requirements.txt.

6) I am using Python version 3.10.12, so you can create a virtual environment with this version.



