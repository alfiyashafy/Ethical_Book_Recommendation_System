# Ethical_Book_Recommendation_System

## Overview
The Ethical Book Recommendation System is designed to provide users with personalized book recommendations while prioritizing ethical considerations such as user privacy, data security, and unbiased suggestions. This project focuses on delivering a trustworthy and user-friendly recommendation experience.

## Ethical Challenges and considerations 
Developing a book recommendation system involves several ethical challenges and considerations to ensure fairness, transparency, and respect for user privacy. Addressing these challenges is crucial for building a system that users can trust and rely on. Below are some of the key ethical considerations taken into account in this project:
### Fairness and Bias
### Transparency and Explainability
### User Privacy and Data Security
### User Control and Feedback
### Ethical Use of Algorithms

## Features
User Authentication: Users can log in with their unique user ID to receive personalized recommendations.
Top 50 Books: Displays a list of the top 50 books based on average ratings and number of ratings.
Author-Based Recommendations: Users can select an author to receive recommendations for books by that author.
User Feedback Mechanism: Users can provide feedback on recommendations with options like "Read Again" or "Recommend New."
Transparency: The system provides clear explanations for recommendations based on author popularity and book ratings.

## Dataset
The dataset used in this project is sourced from Kaggle's "Book-Crossing Dataset," containing comprehensive information on books, user ratings, and demographics. It comprises three main tables:

Books Table (Books.csv): Includes details such as title, author, publication year, and publisher.
Users Table (Users.csv): Contains demographic information about users, including location and age.
Ratings Table (Ratings.csv): Records user ratings for various books on a scale from 1 to 10.

## Data Processing
Merging Datasets: The Books, Users, and Ratings tables are merged to create a comprehensive DataFrame.
Calculating Aggregate Statistics: Number of ratings per book and average rating per book are calculated.
Filtering Popular Books: Books with more than 250 ratings are selected to ensure a reliable recommendation base.
User-Specific Data: Unique authors are extracted to enable author-based recommendations.

## Streamlit API Logic and UI
The system is built using Streamlit, providing an interactive and responsive user interface. Key components include:

User Authentication: Users enter their user ID for personalized recommendations.
Sidebar Navigation: Users can navigate between "Top 50 Books" and "Recommendation Based" options.
Top 50 Books: Displays the top 50 books based on popularity.
Author-Based Recommendations: Users select an author to receive book recommendations from that author.
User Feedback: Options for "Read Again" or "Recommend New" allow users to refine future recommendations.

## Technology Used
Development Environment: PyCharm for coding and project management.
Database Management: PostgreSQL for storing and managing data related to users, books, and ratings.
Web Framework: Streamlit for creating interactive user interfaces.
API Integration: Google Books API to retrieve detailed book information.
Programming Language: Python, leveraging libraries like Pandas and Scikit-learn.

## Limitations
While the system effectively provides top-rated books by the selected author, it faces limitations in the "Recommend New" feature. This feature, intended to suggest books similar to the user's initial author selection, currently relies on popularity-based algorithms instead of leveraging author-specific attributes. Additionally, there are challenges in storing user data, particularly read books, due to database connection errors, impacting the completeness of user interactions within the system.

## Installation and Setup
Clone the repository:
bash
Copy code
git clone <repository-url>
Navigate to the project directory:
bash
Copy code
cd ethical-book-recommendation-system
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Run the Streamlit app:
bash
Copy code
streamlit run app.py

# License
This project is licensed under the MIT License. See the LICENSE file for more details.

# Acknowledgements
Kaggle for providing the Book-Crossing Dataset.
Streamlit for the interactive web framework.
Google Books API for detailed book information.
