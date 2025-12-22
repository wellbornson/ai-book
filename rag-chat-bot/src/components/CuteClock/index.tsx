import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

const CuteClock = () => {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  return (
    <div className={styles.clockContainer}>
      <span className={styles.icon}>⚡</span>
      <span className={styles.time}>{formatTime(time)}</span>
    </div>
  );
};

export default CuteClock;
