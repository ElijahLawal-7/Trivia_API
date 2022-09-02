import React, { Component } from 'react';
import styles from '../stylesheets/QuestionsView.module.css';
import $ from 'jquery';

const base_url = '/api/v0.1.0';

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
      originalCategories: [
        'Science',
        'Art',
        'Geography',
        'History',
        'Entertainment',
        'Sports'
      ],
      id: 0,
      rating: 0
    };
  }

  componentDidMount () {
    const { id, rating } = this.props;
    this.setState({
      id: id,
      rating: rating
    });
  }

  createRating () {
    const ratings = [];
    for (let index = 1; index <= 5; index++) {
      ratings.push(
        <span className={styles.rate} key={index} onClick={() => this.updateRating(index)}>{this.state.rating >= (index) ? '💛' : '🖤'}</span>
      );
    }
    return ratings;
  }

  updateRating (rating) {
    $.ajax({
      url: `${base_url}/questions/${this.state.id}`,
      type: 'PATCH',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ rating: rating }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          rating: rating
        });
        return;
      },
      error: (error) => {
        alert('Unable to update rating: ' + error.message);
        return;
      },
    });
  }

  flipVisibility () {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render () {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className={styles.questionHolder}>
        <div className='Question'>{question}</div>

        <div
          className={`${styles.showAnswer} ${this.state.visibleAnswer ? styles.shown : ''}`}
          onClick={() => this.flipVisibility()}
        >
          <span>{this.state.visibleAnswer ? 'Hide' : 'Show'} Answer </span>
        </div>
        <div className={styles.answerHolder}>
          <span
            style={{
              visibility: this.state.visibleAnswer ? 'visible' : 'hidden',
            }}
          >
            Answer: {answer}
          </span>
        </div>
        <div className={styles.questionStatus}>
          <img
            className={styles.category}
            alt={`${category.toLowerCase()}`}
            src={`${this.state.originalCategories.some(el => el === category) ? category.toLowerCase() : 'new'}.svg`}
          />
          <div className={styles.rating}>
            Rating: {this.createRating()}
          </div>
          <div className={styles.difficulty}>Difficulty: {difficulty}</div>
          <div className='deleteContainer'>
            <img
              src='delete.png'
              alt='delete'
              className={styles.delete}
              onClick={() => this.props.questionAction('DELETE')}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default Question;
