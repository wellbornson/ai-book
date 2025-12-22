import React from 'react';
import styles from './styles.module.css';

const TeacherGreeting = () => {
  return (
    <div className={styles.greetingContainer}>
      <span className={styles.heart}>❤️</span>
      <div className={styles.textContainer}>
        <span className={styles.respect}>Respect to My Teachers:</span>
        <span className={styles.names}>SIR AMEEN ALAM & SIR ZIA KHAN</span>
        <span className={styles.thanks}>Thank you for your guidance!</span>
      </div>
    </div>
  );
};

export default TeacherGreeting;
