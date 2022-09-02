# Frontend - Trivia API

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **stand up the backend first**, reference the [backend documentation](./../backend/README.md) for detailed guidance.

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i` is shorthand for `npm install``

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

```bash
npm start
```

And that should do it, open [http://localhost:3000](http://localhost:3000) to view the Trivia app in the browser.

## Interaction

### List Page

The app opens a view that list all the questions by default and gives you the ability to view questions by their category by clicking on the desired category on the side bar.

The questions are loaded three (3) at a time on a page on this project and set to switch pages based on the category selected.

### Add Question page

This page gives you the ability to add a question to the trivia.

### Add Category page

This page allows you to add a category to the trivia.
If the category provided already exists, you will get a conflict alert and would have to provide something different.

### Play Quiz page

Here you play the quiz

- In this page you would have to choose the user profile to play the quiz as. You could also create your own user profile if you want.
- After which you will be prompted to choose a category before you can start the quiz.
- Upon choosing a category, you will be taken to the game, where you will be provided with a question to answer.
- You have 5 turns to play the game if the category selected has up to 5 questions assigned to it, but if not, you will only get the available questions in the category after which a final score is displayed and result is added to your cumulative score.
