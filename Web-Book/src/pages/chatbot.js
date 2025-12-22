import React from 'react';
import Layout from '@theme/Layout';
import Chatbot from '../components/Chatbot';

function ChatbotPage() {
  return (
    <Layout title="RAG Chatbot" description="Chat with the RAG AI about book content">
      <main>
        <Chatbot />
      </main>
    </Layout>
  );
}

export default ChatbotPage;