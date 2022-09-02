import React, { Component } from 'react';
import styles from '../stylesheets/QuestionsView.module.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

const base_url = '/api/v0.1.0';

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: 0,
      onSearch: false,
      searchTerm: ''
    };
  }

  componentDidMount () {
    this.getQuestions();
  }

  getQuestions = (page = 1) => {
    $.ajax({
      url: `${base_url}/questions?page=${page}`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
          categories: result.categories,
          page: page
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  selectPage (num) {
    this.setState({ page: num }, () => {
      if (!this.state.onSearch) {
        if (!this.state.currentCategory) {
          this.getQuestions(this.state.page);
        } else {
          this.getByCategory(this.state.currentCategory, this.state.page);
        }
      }
      else {
        this.submitSearch(this.state.searchTerm, this.state.page);
      };
    });
  }

  createPagination () {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 3);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`${styles.pageNum} ${i === this.state.page ? styles.active : ''}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id, page = 1) => {
    $.ajax({
      url: `${base_url}/categories/${id}/questions?page=${page}`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
          onSearch: false,
          page: page
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  submitSearch = (searchTerm, page = 1) => {
    $.ajax({
      url: `${base_url}/questions?page=${page}`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ search_term: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
          onSearch: true,
          searchTerm: searchTerm,
          page: page
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `${base_url}/questions/${id}`, //TODO: update request URL
          type: 'DELETE',
          success: (result) => {
            this.setState({
              questions: this.state.questions.filter(question => question.id !== result.deleted_id)
            });
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again');
            return;
          },
        });
      }
    }
  };

  render () {
    return (
      <div className={styles.questionView}>
        <div className={styles.categoriesList}>
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            <li
              onClick={() => { this.getQuestions(1); }}
              className={`${this.state.currentCategory === 0 ? styles.selected : ''}`}
            >
              All
            </li>
            {Object.keys(this.state.categories).map((id) => (
              <li
                key={id}
                onClick={() => {
                  this.getByCategory(id);
                }}
                className={`${Number(this.state.currentCategory) === Number(id) ? styles.selected : ''}`}
              >
                <img
                  className={styles.category}
                  alt={`${this.state.categories[id].toLowerCase()}`}
                  src={`${id < 7 ? this.state.categories[id].toLowerCase() : 'new'}.svg`}
                />
                <span>{this.state.categories[id]}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className={styles.questionsList}>
          <h2>
            Questions
          </h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              id={q.id}
              rating={q.rating}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <Search submitSearch={this.submitSearch} />
          <div className={styles.paginationMenu}>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
