import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css'; // Assuming we'll add some CSS later

const API_BASE_URL = 'http://localhost:8000/api/v1'; // FastAPI backend URL
const DUMMY_TOKEN = 'your-dummy-auth-token'; // Replace with a real token mechanism if available

function Chatbot() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    // Create a new session when the component mounts
    const createSession = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/sessions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${DUMMY_TOKEN}`,
          },
          body: JSON.stringify({
            book_id: 'example-book-id', // Placeholder for now, can be dynamic
            initial_context: 'full-book',
          }),
        });
        const data = await response.json();
        if (response.ok) {
          setSessionId(data.session_id);
          setMessages([{ type: 'bot', text: "Hello! I'm your RAG Chatbot. Ask me anything about the book!" }]);
        } else {
          console.error('Failed to create session:', data);
          setMessages([{ type: 'bot', text: "Error: Could not start chat session. Please try again later." }]);
        }
      } catch (error) {
        console.error('Network error creating session:', error);
        setMessages([{ type: 'bot', text: "Error: Network issue. Could not start chat session." }]);
      }
    };

    createSession();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || !sessionId || isLoading) return;

    const userMessage = { type: 'user', text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${DUMMY_TOKEN}`,
        },
        body: JSON.stringify({
          session_id: sessionId,
          query_text: userMessage.text,
          query_mode: 'full-book',
        }),
      });
      const data = await response.json();

      if (response.ok) {
        const botMessage = {
          type: 'bot',
          text: data.response_text,
          citations: data.citations.map(c => ({
            source_location: c.source_location,
            content: c.content
          }))
        };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } else {
        console.error('Failed to get response:', data);
        setMessages((prevMessages) => [...prevMessages, { type: 'bot', text: `Error: ${data.detail?.error?.message || 'Failed to get response.'}` }]);
      }
    } catch (error) {
      console.error('Network error sending message:', error);
      setMessages((prevMessages) => [...prevMessages, { type: 'bot', text: 'Error: Network issue. Please check your connection.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <h2>RAG Chatbot</h2>
      {!sessionId && <p>Loading chat session...</p>}
      <div className={styles.messagesContainer}>
        {messages.map((msg, index) => (
          <div key={index} className={`${styles.message} ${styles[msg.type]}`}>
            <p>{msg.text}</p>
            {msg.type === 'bot' && msg.citations && msg.citations.length > 0 && (
              <div className={styles.citations}>
                <strong>Citations:</strong>
                <ul>
                  {msg.citations.map((citation, idx) => (
                    <li key={idx}>
                      <a href={`#${citation.source_location}`}>{citation.source_location}</a>: {citation.content}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
        {isLoading && <div className={`${styles.message} ${styles.bot}`}>Loading...</div>}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSendMessage} className={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={sessionId ? "Ask me a question..." : "Waiting for session..."}
          disabled={!sessionId || isLoading}
        />
        <button type="submit" disabled={!sessionId || isLoading}>Send</button>
      </form>
    </div>
  );
}

export default Chatbot;