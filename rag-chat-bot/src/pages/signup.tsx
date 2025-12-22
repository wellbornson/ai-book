import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './auth.module.css';

export default function SignUp() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Account created successfully! Welcome to the future. 🚀");
    window.location.href = '/signin';
  };

  return (
    <Layout title="Sign Up" description="Create your AI Account">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <h2>Join the Squad ⚡</h2>
          <p>Create an account to start learning.</p>
          
          <form onSubmit={handleSubmit}>
            <div className={styles.inputGroup}>
              <label>Full Name</label>
              <input 
                type="text" 
                placeholder="Zahid Imam" 
                value={name}
                onChange={(e) => setName(e.target.value)}
                required 
              />
            </div>

            <div className={styles.inputGroup}>
              <label>Email</label>
              <input 
                type="email" 
                placeholder="human@example.com" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required 
              />
            </div>
            
            <div className={styles.inputGroup}>
              <label>Password</label>
              <input 
                type="password" 
                placeholder="••••••••" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required 
              />
            </div>

            <button type="submit" className={styles.authButton}>Create Account</button>
          </form>

          <div className={styles.authFooter}>
            <p>Already have an account? <Link to="/signin">Sign In</Link></p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
