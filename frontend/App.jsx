import React, { useState } from 'react';

/**
 * App Component - NBA Ref Chatbot
 *
 * This React component renders a simple chatbot interface for asking NBA rules questions.
 * Features:
 * - Chatbox UI with styled user and bot messages
 * - Input form to send user messages
 * - Loading indicator ("Scott Foster is typing...")
 * - Fetches bot responses from backend API (`http://localhost:8000/chat`)
 * - Right-side image (decorative)
 */
function App() {

  // State to hold all chat messages (array of { sender, text })
  const [messages, setMessages] = useState([]);

  // State to hold the user's current input
  const [input, setInput] = useState('');

  // State to manage "loading" indicator when awaiting bot reply
  const [loading, setLoading] = useState(false);

  /**
   * sendMessage - Handles form submission (sending a user message).
   * - Prevents page refresh
   * - Adds user message to chat
   * - Sends request to backend API
   * - Appends bot's response (or error message) to chat
   */
  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return; // ignore empty messages

    // Add user's message to state
    const userMessage = { sender: 'user', text: input };
    setMessages((msgs) => [...msgs, userMessage]);
    setLoading(true);
    setInput('');

    try {
      // Send message to backend API
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      // Parse bot's reply
      const data = await res.json();
      setMessages((msgs) => [...msgs, { sender: 'bot', text: data.reply }]);
    } catch (err) {
      // Fallback error message if API call fails
      setMessages((msgs) => [
        ...msgs,
        { sender: 'bot', text: 'Error: Could not get response.' }
      ]);
    }

    setLoading(false);
  };

  // Fixed height for chat input bar
  const chatboxHeight = 120;

  return (
    <div
      style={{
        minHeight: '100vh',
        width: '100vw',
        background: '#181A20',
        fontFamily: 'Inter, Segoe UI, sans-serif',
        display: 'flex',
        flexDirection: 'row'
      }}
    >
      {/* Main Chat Section */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <h2
          style={{
            color: '#E9B949',
            textAlign: 'center',
            fontWeight: 700,
            fontSize: 54,
            margin: 0,
            padding: '40px 0 20px 0'
          }}
        >
          NBA Ref Chatbot
        </h2>

        {/* Messages container */}
        <div
          style={{
            maxWidth: 900,
            margin: '0 auto',
            paddingBottom: chatboxHeight + 40, // add space for typing indicator
            flex: 1,
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          {/* Render all messages */}
          {messages.map((msg, i) => (
            <div
              key={i}
              style={{
                display: 'flex',
                justifyContent:
                  msg.sender === 'user' ? 'flex-end' : 'flex-start',
                margin: '28px 0'
              }}
            >
              {msg.sender === 'bot' ? (
                // Bot message (yellow text bubble)
                <pre
                  style={{
                    background: '#232946',
                    color: '#E9B949',
                    padding: '28px 36px',
                    borderRadius: 22,
                    whiteSpace: 'pre-wrap',
                    fontSize: 32,
                    fontFamily: 'inherit',
                    maxWidth: '85%'
                  }}
                >
                  {msg.text}
                </pre>
              ) : (
                // User message (yellow background bubble)
                <span
                  style={{
                    background: '#E9B949',
                    color: '#232946',
                    padding: '28px 36px',
                    borderRadius: 22,
                    fontSize: 32,
                    fontFamily: 'inherit',
                    maxWidth: '85%',
                    fontWeight: 600
                  }}
                >
                  {msg.text}
                </span>
              )}
            </div>
          ))}

          {/* Typing indicator */}
          <div style={{ minHeight: 40 }}>
            {loading && (
              <div
                style={{
                  color: '#E9B949',
                  fontWeight: 600,
                  fontSize: 32
                }}
              >
                Scott Foster is typing...
              </div>
            )}
          </div>
        </div>

        {/* Chat input form */}
        <form
          onSubmit={sendMessage}
          style={{
            position: 'fixed',
            left: 0,
            right: 0,
            bottom: 0,
            height: chatboxHeight,
            background: '#232946',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderTop: '2px solid #E9B949'
          }}
        >
          <div style={{ width: 900, display: 'flex', gap: 28 }}>
            {/* User input field */}
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              style={{
                flex: 1,
                padding: 32,
                borderRadius: 16,
                border: '1.5px solid #E9B949',
                fontSize: 32,
                background: '#181A20',
                color: '#fff'
              }}
            />
            {/* Send button */}
            <button
              type="submit"
              style={{
                padding: '0 56px',
                borderRadius: 16,
                border: 'none',
                background: '#E9B949',
                color: '#232946',
                fontWeight: 700,
                fontSize: 32,
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
              disabled={loading}
            >
              Send
            </button>
          </div>
        </form>
      </div>

      {/* Side image (stops above chatbox) */}
      <div
        style={{
          width: '30vw',
          minWidth: 320,
          position: 'fixed',
          right: 0,
          top: 0,
          bottom: chatboxHeight, // stops image above input bar
          pointerEvents: 'none',
          overflow: 'hidden',
          background: '#181A20'
        }}
      >
        <img
          src="/fbade587dbc577a77b0c9eb8a0debd80.png"
          alt="Chatbot Visual"
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover'
          }}
        />
      </div>
    </div>
  );
}

export default App;
