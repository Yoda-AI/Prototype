# Yoda Prototype

This is a Dash app that allows for uni-variable, bi-variables and multi-variable exploration of data using plotly.express library. The app takes in a dataframe, an explored variable and a target column and generates box plots, histograms, and violin plots of the explored variable against all other columns in the dataframe.

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

# Prerequisites
You will need the following packages to run this app:

dash==1.21.1
dash-bootstrap-components==0.11.1
dash-core-components==1.11.1
dash-html-components==1.1.1
dash-renderer==1.5.1
dash-table==4.12.0
plotly==4.13.0
pandas==1.2.5
requests==2.25.0
You can install these packages by running pip install -r requirements.txt

# Running the app
To run the app, you will need to execute the code in the command line.
python <your_file_name>.py
Then, open your web browser and go to http://127.0.0.1:8050/

# Built With
Dash - The web framework used
Plotly - Data visualization library
Pandas - Data manipulation library
requests - HTTP library
Author
Your name - Your Github profile
Acknowledgments
Thanks to the Dash and Plotly communities for their support and tutorials.
Inspiration from Bi-variables Exploration Dashboard

# Feedback
The app includes buttons for sending feedback on the usefulness of the generated plots. These buttons send a GET request to http://Yoda-AI/feedback/ along with the id of the button clicked. You can use this endpoint to record the feedback in a database or log file.
