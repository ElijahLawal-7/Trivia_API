import React, { Component } from "react";
import styles from "../stylesheets/Header.module.css";

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className={styles.appHeader}>
        <h1
          className={styles.mainHeader}
          onClick={() => {
            this.navTo("");
          }}
        >
          Udacitrivia
        </h1>
        <h2
          className={`${styles.headers} ${
            window.location.href === window.location.origin + "/"
              ? styles.selected
              : ""
          }`}
          onClick={() => {
            this.navTo("");
          }}
        >
          List
        </h2>
        <h3
          className={`${styles.headers} ${
            window.location.href === window.location.origin + "/add-question"
              ? styles.selected
              : ""
          }`}
          onClick={() => {
            this.navTo("/add-question");
          }}
        >
          Add Question
        </h3>
        <h3
          className={`${styles.headers} ${
            window.location.href === window.location.origin + "/add-category"
              ? styles.selected
              : ""
          }`}
          onClick={() => {
            this.navTo("/add-category");
          }}
        >
          Add Category
        </h3>
        <h2
          className={`${styles.headers} ${
            window.location.href === window.location.origin + "/play"
              ? styles.selected
              : ""
          }`}
          onClick={() => {
            this.navTo("/play");
          }}
        >
          Play
        </h2>
      </div>
    );
  }
}

export default Header;
