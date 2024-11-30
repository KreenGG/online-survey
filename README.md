# Online Surveys

Survey managing application, there you can make surveys with different questions, and get statistics.

## Features

- CRUD surveys
- Survey statistics in Excel

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/KreenGG/online-survey.git
   cd online-survey
   ```
2. Create and configure `.env` file from `.env.example`(test section can be skipped)
3. Make migrations to your database.
   
   ```bash
   python manage.py migrate
   ```

## Running the Application

   ```bash
   python manage.py runserver
   ```
