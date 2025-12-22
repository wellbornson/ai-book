import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './auth.module.css';

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulate Login Logic
    // In a real app, you would send this to your backend
    console.log("Logging in...", email);
    
    // Store the token that the Chatbot needs
    localStorage.setItem('auth_token', 'test-token');
    
    // Redirect to Chatbot
    window.location.href = '/chatbot';
  };

  return (
    <Layout title="Sign In" description="Login to your AI Account">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <h2>Welcome Back! 🤖</h2>
          <p>Login to access your AI Brain.</p>
          
          <form onSubmit={handleSubmit}>
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

            <button type="submit" className={styles.authButton}>Sign In</button>
          </form>

          <div className={styles.authFooter}>
            <p>Don't have an account? <Link to="/signup">Sign Up</Link></p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
