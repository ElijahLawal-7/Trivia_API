import React, { Component } from 'react';
import $ from 'jquery';
import styling from '../stylesheets/QuizView.module.css';
import style from '../stylesheets/FormView.module.css';

const questionsPerPlay = 5;
const base_url = '/api/v0.1.0';

class QuizView extends Component {
  constructor(props) {
    super();
    this.state = {
      quizCategory: 0,
      previousQuestions: [],
      showAnswer: false,
      categories: {},
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false,
      users: [],
      user: 0,
      username: '',
      cumulativeScore: 0
    };
  }

  componentDidMount () {
    $.ajax({
      url: `${base_url}/categories?quiz=true`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({ categories: result.categories });
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again');
        return;
      },
    });

    this.getUsers();
  }

  getUsers () {
    $.ajax({
      url: `${base_url}/users`,
      type: 'GET',
      success: (result) => {
        this.setState({ users: result.users });
        return;
      },
      error: (error) => {
        alert('Unable to load Users');
        return;
      },
    });
  }

  selectUser (id) {
    this.setState({ user: id });
  }

  updateUserScore () {
    $.ajax({
      url: `${base_url}/users/${this.state.user}`,
      type: 'PATCH',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ score: this.state.numCorrect }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          cumulativeScore: result.score
        });
        return;
      },
      error: (error) => {
        alert(`Unable to update User's cumulative score: ` + error.message);
        return;
      },
    });
  }

  submitUser = (event) => {
    event.preventDefault();
    $.ajax({
      url: `${base_url}/users`,
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        username: this.state.username,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.getUsers();
        document.getElementById('add-user-form').reset();
        this.setState({ username: '' });
        return;
      },
      error: (error) => {
        alert('Unable to add User. Please try your request again');
        return;
      },
    });
  };

  handleUserChange = (event) => {
    event.preventDefault();
    this.setState({ username: event.target.value });
  };

  selectCategory = ({ type, id = 0 }) => {
    this.setState({ quizCategory: { type, id } }, this.getNextQuestion);
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  getNextQuestion = () => {
    const previousQuestions = [...this.state.previousQuestions];
    if (this.state.currentQuestion.id) {
      previousQuestions.push(this.state.currentQuestion.id);
    }

    $.ajax({
      url: `${base_url}/quizzes`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.quizCategory,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: ''
        });
        if (!Object.keys(result.question).length || result.question === null || this.state.previousQuestions.length === questionsPerPlay) {
          this.setState({
            forceEnd: true
          });
          this.state.forceEnd && this.updateUserScore();
        }

        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again');
        return;
      },
    });
  };

  submitGuess = (event) => {
    event.preventDefault();
    let evaluate = this.evaluateAnswer();
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    });
  };

  restartGame = () => {
    this.getUsers();
    this.setState({
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false,
      user: 0
    });
  };

  userForm () {
    return (
      <div id='add-form'>

        <form
          className={style.form}
          id='add-user-form'
          onSubmit={this.submitUser}
        >
          <h2>Create new profile</h2>
          <label>
            <span>Username</span>
            <input type='text' name='username' onChange={this.handleUserChange} />
          </label>
          <input type='submit' value='Submit' />
        </form>
      </div>
    );
  }

  renderUserSelect () {
    return (
      <div className={styling.quizPlayHolder}>
        <div className={styling.chooseHeader}>Play as</div>
        <div className={styling.categoryHolder}>
          {this.state.users.map(user => {
            return (
              <div key={user.id} onClick={() => this.selectUser(user.id)} className={styling.playCategory}>
                <p>{user.username} - Score: {user.score}</p>
              </div>
            );
          })}
        </div>
        {this.userForm()}
      </div>
    );
  }

  renderPrePlay () {
    return (
      <div className={styling.quizPlayHolder}>
        <div className={styling.chooseHeader}>Choose Category</div>
        <div className={styling.categoryHolder}>
          <div className={styling.playCategory} onClick={this.selectCategory}>
            ALL
          </div>
          {Object.keys(this.state.categories).map((id) => {
            return (
              <div
                key={id}
                value={id}
                className={styling.playCategory}
                onClick={() =>
                  this.selectCategory({ type: this.state.categories[id], id })
                }
              >
                {this.state.categories[id]}
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  renderFinalScore () {
    return (
      <div className={styling.quizPlayHolder}>
        <div>
          Your Final Score is {this.state.numCorrect}
        </div>
        <div className={styling.cumulative}>
          Your Cumulative Score is {this.state.cumulativeScore}!
        </div>
        <div className={styling.button} onClick={this.restartGame}>
          Play Again?
        </div>
      </div>
    );
  }

  evaluateAnswer = () => {
    const formatGuess = this.state.guess
      // eslint-disable-next-line
      .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '')
      .toLowerCase();
    const answerArray = this.state.currentQuestion.answer
      .toLowerCase()
      .split(' ');
    return answerArray.every((el) => formatGuess.includes(el));
  };

  renderCorrectAnswer () {
    let evaluate = this.evaluateAnswer();
    return (
      <div className={styling.quizPlayHolder}>
        <div className={styling.quizCategory}>
          {this.state.currentQuestion.question}
        </div>
        <div className={`${evaluate ? styling.correct : styling.wrong}`}>
          {evaluate ? 'You were correct!' : 'You were incorrect'}
        </div>
        <div className={styling.quizAnswer}>{this.state.currentQuestion.answer}</div>
        <div className={styling.button} onClick={this.getNextQuestion}>
          {' '}
          Next Question{' '}
        </div>
      </div>
    );
  }

  renderPlay () {
    return (this.state.previousQuestions.length === questionsPerPlay || this.state.forceEnd)
      ? (
        this.renderFinalScore()
      ) : this.state.showAnswer ? (
        this.renderCorrectAnswer()
      ) : (
        <div className={styling.quizPlayHolder}>
          <div className={styling.quizCategory}>
            {this.state.currentQuestion.question}
          </div>
          <form onSubmit={this.submitGuess} className={style.form}>
            <label>
              <input type='text' name='guess' onChange={this.handleChange} />
            </label>
            <input
              type='submit'
              value='Submit Answer'
            />
          </form>
        </div>
      );
  }

  render () {
    return this.state.user ? this.state.quizCategory ? this.renderPlay() : this.renderPrePlay() : this.renderUserSelect();
  }
}

export default QuizView;
