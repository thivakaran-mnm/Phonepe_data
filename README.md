#PhonePe Data Visualization and Exploration

This project is a Streamlit web application designed for visualizing and exploring data related to PhonePe transactions, users, and insurance. It provides interactive charts and maps to analyze various aspects of PhonePe usage.

##Table of Contents
Introduction
Installation
Usage
Features
Conclusion

##Introduction
The PhonePe Data Visualization and Exploration app is built using the Streamlit framework in Python. It connects to a MySQL database to fetch data related to PhonePe transactions, users, and insurance. The application offers multiple analysis methods, including aggregated analysis, map analysis, and top charts. Users can select specific years, quarters, states, or districts to visualize relevant data.

##Installation
To run this application locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the required Python packages.
3. Ensure that you have a MySQL server running locally with the appropriate database and credentials configured.
4. Update the MySQL connection details in the Phone_pulse.py file to match your local setup.
5. Run the Streamlit application using the following command:
   streamlit run Phonepe_pulse.py
   
##Usage
Once the application is running, you can access it through your web browser. The main menu allows you to choose between different analysis methods, including aggregated analysis, map analysis, and top charts. Select the desired method and follow the prompts to explore the PhonePe data interactively.

##Features
1. Aggregated analysis of PhonePe transactions, users, and insurance.
2. Interactive maps for visualizing transaction and user data by state and district.
3. Top charts highlighting key insights such as top mobile brands, states with highest transaction amounts, and more.
4. User-friendly interface with dropdowns, sliders, and radio buttons for selecting analysis parameters.

Conclusion
The PhonePe Data Visualization and Exploration app simplifies the analysis of PhonePe transaction, user, and insurance data. Whether you're a beginner or an expert, this tool makes it easy to uncover insights and trends. We're open to feedback and contributions to make this tool even better!
