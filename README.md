# PlacementEligibilityapp
PlacementEligibilityapp using streamlit application that helps the user to query student information database and display eligible candidate details

## Overview

The PlacementEligibilityApp simplifies the process of identifying suitable candidates for placements by allowing users to:
1.Query student data: Filter students based on various criteria dynamically (e.g., problems_solved, softskills, placement-mock_interview_score, final_project_score).
2.Display eligible candidates: View a table of students who meet the specified eligibility criteria.
3.Download results: Export the filtered student data as CSV file.

## Features

1.Interactive Filtering: Use Streamlit's widgets(like slider, dropdown(selectbox)) to easily filter student data.
2.Clear Data Visualization: Display eligible candidates in a tabular format.
3.User-Friendly Interface: Simple design for easy navigation and use.
4.Record the findings: Download/Export the results in CSV format.

## Technologies Used

1.Python: The core programming language.
2.Streamlit: For creating the interactive web application.
3.Pandas: For data manipulation, final result and analysis.
4.SQL (MySQL): For database storage and interaction.
5.NumPy: To handle numeric values
6.Faker: Generates the fake data on student details.

## Setup

1.  Install the libraries using pip install <library_name> in VSCode(VisualStudioCode).
2.  Develop the code using OOPs concepts(Class, Methods) to generate the data and store the data to database (Projectfinal.ipynb)
3.  Develop the streamlit application and queries to extract the data(eligible students for placements) from database by connecting to mysql connector server(PlacementEligibilityapp.py).
4.  Run the Streamlit application in the VScode terminal:
    ```bash
    streamlit run PlacementEligibilityapp.py
    ```

## Usage

1.  Run the application and the application will be opened in your web browser.
2.  Use the filter options to specify your eligibility criteria.
3.  The table will display the list of eligible candidates.
4.  Click the "Download" button to export the results as CSV file.
