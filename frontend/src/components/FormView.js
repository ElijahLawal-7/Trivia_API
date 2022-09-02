import React, { Component } from 'react';
import $ from 'jquery';
import styles from '../stylesheets/FormView.module.css';

const base_url = '/api/v0.1.0';

class FormView extends Component {
  constructor(props) {
    super();
    this.state = {
      question: '',
      answer: '',
      difficulty: 1,
      category: 1,
      categories: {},
      rating: 1
    };
  }

  componentDidMount () {
    $.ajax({
      url: `${base_url}/categories`, //TODO: update request URL
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
  }

  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: `${base_url}/questions`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category,
        rating: this.state.rating
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById('add-question-form').reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again');
        return;
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render () {
    return (
      <div id='add-form'>
        <form
          className={styles.form}
          id='add-question-form'
          onSubmit={this.submitQuestion}
        >
          <h2>Add a New Trivia Question</h2>
          <label>
            <span>Question</span>
            <textarea rows='3' name='question' onChange={this.handleChange} />
          </label>
          <label>
            <span>Answer</span>
            <input type='text' name='answer' onChange={this.handleChange} />
          </label>
          <label>
            <span>Difficulty</span>
            <select name='difficulty' onChange={this.handleChange}>
              <option value='1'>1</option>
              <option value='2'>2</option>
              <option value='3'>3</option>
              <option value='4'>4</option>
              <option value='5'>5</option>
            </select>
          </label>
          <label>
            <span>Category</span>
            <select name='category' onChange={this.handleChange}>
              {Object.keys(this.state.categories).map((id) => {
                return (
                  <option key={id} value={id}>
                    {this.state.categories[id]}
                  </option>
                );
              })}
            </select>
          </label>
          <label>
            <span>Rating</span>
            <select name='rating' onChange={this.handleChange}>
              <option value='1'>1</option>
              <option value='2'>2</option>
              <option value='3'>3</option>
              <option value='4'>4</option>
              <option value='5'>5</option>
            </select>
          </label>
          <input type='submit' value='Submit' />
        </form>
      </div>
    );
  }
}

export default FormView;
