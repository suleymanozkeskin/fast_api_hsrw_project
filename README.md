# What is this project?

This is a website project for a university in Germany.Only enrolled students and university staff will be able to use the platform. Platform will serve as a forum where students and professors can publicy create discussions , make criticism on topics relevant to university.

Another form of service will be employing and advertising tutors. Students can create a profile as a tutor and at the same time look and employ tutors according to their needs.An online payment system as a microservice will be implemented for those who wants to handle payments through this website.

And last but not least , members will be able to organize/share a wide scope of events and make it known to every student.An invitation only type of event modes will be added too.Depending on the event , website will serve as a ticket selling point too.

# Stage of project

This project is not completed at the moment. For backend; automated testing and payment systems will be added. Frontend will be builded simultaneously.

# What has been done so far ?

Authentication , encryption of passwords, crud operations for users, posts, events, employers, tutors. Initialization for database migration. Manual testing of endpoints has been done via Postman.

# About the tech stack

FastAPI , PostgreSQL, Alembic

# Commands

-   Virtual environment
    -   Create virtual enviromnent
        ```bash
        virtualenv venv
        ```
    -   Activate virtual environment on MacOs/Linux
        ```bash
        source ./venv/bin/activate
        ```
    -   Install dependencies in requirements.txt
        ```bash
        pip install -r requirements.txt
        ```
-   Run the application
    -   type it to terminal
        ```bash
        uvicorn app.main:app --reload
        ```
        
-   Alembic
    -   Alembic Initialisation
        ```bash
        alembic init alembic
        ```
