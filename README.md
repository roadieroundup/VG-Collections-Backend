![banner](readme_files/rmbanner.png?raw=true "banner")

## Overview
Video Game Collections is a web application that allows users to create and manage their own video game lists. Users can create personalized lists, add games to their lists, and provide ratings and reviews for each game. This is only the backend API project.\
\
The backend of the application is developed using Django and Django Rest Framework (DRF), it handles data persistence, user authentication, and API endpoints to perform CRUD operations on game lists, games, ratings, and reviews.

You can see the [React frontend project here.](https://github.com/roadieroundup/VG-Collections-Frontend)\
\
![demo](readme_files/demo.gif?raw=true "Demo")

## Motivation

Web platforms like *letterboxd* provide users with the ability to create movie lists, add reviews, ratings, and other social media features. As an avid video game enjoyer, I noticed the absence of a similar platform dedicated to one of my favorite hobbies. To address this gap, I created Video Game Collections to offer a dedicated space to curate and share their gaming experiences.

## Tech Stack

The project utilizes the following relevant technologies and dependencies:
- Python 3.11.2: The programming language used to build the backend.
- Django 4.1.7: A powerful web framework.
- Django Rest Framework 3.14: A powerful toolkit for building Web APIs.
- Django CORS Headers 3.14: A package that allow handling Cross-Origin Resource Sharing.
- DRF Simple JWT 4.8.0: A package that provides a JSON Web Token authentication backend for the Django REST Framework.
- Psycopg2-binary 2.9.3: A PostgreSQL database adapter for Python.
- Boto3 1.26 and Botocore 1.29: Libraries for interacting with AWS S3, used for user profile pictures.

## Database Schema

![user_flow](readme_files/ERD.png?raw=true "UserFlow")

The above diagram showcases the database schema for the Video Game Collections project. It illustrates the relationships between the main entities in the application

## Live site

Check out the live version of the application at https://roadieroundup.github.io/VG-Collections-Frontend/

## Possible future updates

- [ ]  Add more social media features (follows, discovers, etc) 

Feel free to explore the project and provide any feedback or suggestions for further improvements.