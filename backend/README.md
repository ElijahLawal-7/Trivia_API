# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.10** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

For Windows Users

```bash
$>> ./${path_to_your_virtual_environment}/Scripts/python.exe -m pip install -r ./${path_to_your_requirements_file}/requirements.txt
```

For Unix Users

```bash
$>> ./${path_to_your_virtual_environment}/bin/python -m pip install -r ./${path_to_your_requirements_file}requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM is used to handle the lightweight SQL database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross-origin requests from the frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

For Unix Users

```bash
$>> createdb trivia
```

For Windows Users
Enter your psql tool environment as root user and run the following command

```shell
root_database=# CREATE DATABASE  trivia;
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

For Unix Users

```bash
$>> psql trivia < trivia.psql
```

For Windows Users
Enter your psql tool environment as root user and enter your trivia database then run the following command

```shell
trivia=# \i trivia.psql;
```

### Environment Variables

This API uses environment variables for the database connection information.  
To setup your database connection, simply:
Create a `.env` file in the `/backend` directory with the following content

```text
DATABASE_NAME = '<Your database name>'
DATABASE_PORT = '<Your database connection port>'
DATABASE_OWNER = '<The database owner>'
DATABASE_PASSWORD = '<Password for the database>'
```

> _Note_: All values must be in valid string format.

### Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute the following commands:

```bash
$>> export FLASK_APP=flaskr
$>> export FLASK_ENV=development
$>> flask run
```

Once you have your server running, you can go start up your frontend to work with the backend server.

## API EndPoints

### Get Categories

`GET '/api/v0.1.0/categories'`

Fetches a dictionary of categories in which the keys are the IDs and the value is the corresponding string of the category. If the request argument `quiz` is set to `true`, then only categories that have questions assigned to them are returned, else by default all categories are returned.

- Request Arguments: quiz- type boolean, default false
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `categories`: An object of `id: category_string` key: value pairs

Example Response:

```json
{
  "success": true,
  "categories": {}
}
```

### Create a new Category

`POST '/api/v0.1.0/categories'`

Creates a new category with the name specified in the category property of the body request

- Request Arguments: None
- Request Body Properties: category- type string
- Returns: An object with the following properties:
  - `status_code`: HTTP status code
  - `success`: A boolean representing the status of the result of the request.
  - `message`: A message describing the result of the request

Example Response:

```json
{
  "status_code": 201,
  "success": true,
  "message": "created"
}
```

### Get Questions

`GET '/api/v0.1.0/questions'`

Fetches a list of dictionaries with the questions information, including the list of categories, a count of all the questions returned, and the current category.

- Request Arguments: page- type int
- Returns: An object with five keys:
  - `success`: A boolean representing the status of the result of the request.
  - `questions`: An array of objects with the following properties:
    - `id`: The ID of the question
    - `question`: The question
    - `answer`: The answer
    - `category`: The ID of category of the question
    - `difficulty`: An integer indicating the difficulty of the question
    - `rating`: An integer indicating the rating of the question
  - `total_questions`: An integer of the total number of questions
  - `categories`: An object of `id: category_string` key: value pairs
  - `current_category`: Zero

Example Response:

```json
{
  "success": true,
  "questions": [],
  "total_questions": 0,
  "categories": {},
  "current_category": 0
}
```

### Delete Question

`DELETE '/api/v0.1.0/questions/<int:id>'`

Deletes a question

- Request Arguments: None
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `deleted_id`: A integer representing the ID of the deleted question

Example Response:

```json
{
  "success": true,
  "deleted_id": 0,
}
```

### Search Questions

`POST '/api/v0.1.0/questions'`

Fetches a list of dictionaries with the questions information that match the search value, a count of all the questions returned, and the current category.

- Request Arguments: page- type int
- Request Body Properties: search_term- type string
- Returns: An object with five keys:
  - `success` A boolean representing the status of the result of the request.
  - `questions`: An array of objects with the following properties:
    - `id`: The ID of the question
    - `question`: The question
    - `answer`: The answer
    - `category`: The ID of category of the question
    - `difficulty`: An integer indicating the difficulty of the question
    - `rating`: An integer indicating the rating of the question
  - `total_questions`: An integer of the total number of questions
  - `current_category`: Zero

Example Response:

```json
{
  "success": true,
  "questions": [],
  "total_questions": 0,
  "current_category": 0
}
```

### Update Question Rating

`PATCH '/api/v0.1.0/questions/<int:id>'`

Update a question's rating

- Request Arguments: None
- Request Body Properties: rating- type int
- Returns: An object with the following property:
  - `success`: A boolean representing the status of the result of the request.

Example Response:

```json
{
  "success": true,
}
```

### Create a new Question

`POST '/api/v0.1.0/questions'`

Creates a new question

- Request Arguments: None
- Request Body Properties:
  - `question`: The question
  - `answer`: The answer
  - `category`: The ID of category of the question
  - `difficulty`: An integer indicating the difficulty of the question
  - `rating`: An integer indicating the rating of the question
- Returns: An object with the following properties:
  - `status_code`: HTTP status code
  - `success`: A boolean representing the status of the result of the request.
  - `message`: A message describing the result of the request
  
Example Response:

```json
{
  "status_code": 201,
  "success": true,
  "message": "created"
}
```

### Get Questions by Category

`POST '/api/v0.1.0/categories/<int:category_id>/questions'`

Fetches a list of dictionaries with the questions information with a category ID that matches what the one being requested for, a count of all the questions returned, and the current category.

- Request Arguments: page- type int
- Request Body Properties: search_term- type string
- Returns: An object with the following properties:
  - `success` A boolean representing the status of the result of the request.
  - `questions`: An array of objects with keys:
    - `id`: The ID of the question
    - `question`: The question
    - `answer`: The answer
    - `category`: The ID of category of the question
    - `difficulty`: An integer indicating the difficulty of the question
    - `rating`: An integer indicating the rating of the question
  - `total_questions`: An integer of the total number of questions
  - `current_category`: An integer indicating the ID of category of the questions returned

Example Response:

```json
{
  "success": true,
  "questions": [],
  "total_questions": 0,
  "current_category": 0
}
```

### Load Quiz Question

`POST '/api/v0.1.0/quizzes'`

Fetches a single question for the quiz on the condition that the question's ID does not already exist among the previous questions' IDs coming from the client.

- Request Arguments: None
- Request Body Properties:
  - `quiz_category`: An object with an `id` key that contains an integer indicating the category of the question to be returned
  - `previous_questions`: A list IDs of the previous questions accepted by the client
- Returns: An object with the following property:
  - `success`: A boolean representing the status of the result of the request.
  - `question`: An object with the following properties:
    - `id`: The ID of the question
    - `question`: The question
    - `answer`: The answer
    - `category`: The ID of category of the question
    - `difficulty`: An integer indicating the difficulty of the question
    - `rating`: An integer indicating the rating of the question

Example Response:

```json
{
  "success": true,
  "question": {},
}
```

### Get Users

`GET '/api/v0.1.0/users'`

Fetches a list of dictionaries of containing the information of the users.

- Request Arguments: None
- Returns: An object with the following property:
  - `users`: An array of object with the following properties:
    - `id`: The ID of the user
    - `username`: The username of the user
    - `score`: The score of the user

Example Response:

```json
{
  "users": [
    {
      "id": 1,
      "username": "Anonymous",
      "score": 0
    },
  ]
}
```

### Update User Score

`PATCH '/api/v0.1.0/users/<int:id>'`

Update a user's score

- Request Arguments: None
- Request Body Properties: score- type int
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `score`: An integer representing the updated score

Example Response:

```json
{
  "success": true,
  "score": 0
}
```

### Create a new User

`POST '/api/v0.1.0/users'`

Creates a new user with the username specified in the username property of the body request. Optionally a score property can be provided to provide an initial score for the user to be created.

- Request Arguments: None
- Request Body Properties: username- type string, (optionally) score- type integer
- Returns: An object with the following properties:
  - `status_code`: HTTP status code
  - `success`: A boolean representing the status of the result of the request.
  - `message`: A message describing the result of the request

Example Response:

```json
{
  "status_code": 201,
  "success": true,
  "message": "created"
}
```

## Errors

The following are the mostly likely errors that can occur when making requests:

### Bad Request

This could be as a result of passing:

- Empty or incomplete body parameters
- Invalid type of data

```json
{
  "success": false,
  "error": 400,
  "message": "bad request",
}
```

### Resource not Found

This means that no result could be found for the requested resource.

```json
{
  "success": false,
  "error": 404,
  "message": "resource not found",
}
```

### Method not Allowed

This is because no endpoint is specified for the specified method of request

```json
{
  "success": false,
  "error": 405,
  "message": "method not allowed"
}
```

### Conflict

This indicates that data requested to be created, already exists and as such would cause a conflict if created.

```json
{
  "success": false,
  "error": 409,
  "message": "conflict",
}
```

### Unprocessable Entity

This indicates that a request passed an empty value.

Example Request Body:

```json
{
  "username": ""
}
```

Example Response:

```json
{
  "success": false,
  "error": 422,
  "message": "unprocessable",
}
```

### Internal Server error

This indicates that the server encountered an error on attempt to process the request.
> _Notice_: If this is encountered, please create an issue on this repo and give a detailed description of events leading up to the error.

Example Response:

```json
{
  "success": false,
  "error": 500,
  "message": "internal server error"
}
```
