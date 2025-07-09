This is an end-to-end machine learning project to predict whether a website URL is malicious (phishing) or legitimate, aimed at enhancing
network security through automated threat detection.
A classification model is built using data extracted from a MongoDB database to identify phishing URLs. The project includes a full ML 
pipeline integrated into a FastAPI web application for real-time predictions.
This project's code is developed in a fully modular structure according to the ML lifecycle.
MLflow and Dagshub are used to track model performance
This project contains a github workflow to containerize the FastAPI based web application using docker  and deploy it on an AWS EC2 instance
