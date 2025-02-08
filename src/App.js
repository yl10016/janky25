import React, { useState } from "react";
import "./styles.css";

const newsArticles = [
  {
    title: "Tech Industry Booms in 2025",
    summary: "The technology sector continues to expand rapidly, with AI leading the way. Recent reports suggest a 20% increase in AI-driven job opportunities.",
    link: "https://example.com/tech-boom",
  },
  {
    title: "Climate Change Policies Strengthened Globally",
    summary: "Governments worldwide have pledged stronger climate action, with new laws targeting carbon emissions reductions by 40% over the next decade.",
    link: "https://example.com/climate-policy",
  },
  {
    title: "Breakthrough in Cancer Research Announced",
    summary: "Scientists have developed a new therapy that improves survival rates by 30%, marking a significant advancement in oncology.",
    link: "https://example.com/cancer-research",
  },
];

const hardcodedResponses = [
  "That's an interesting perspective!",
  "I see your point. What other solutions might work?",
  "This is a complex issue, isn't it?",
];

function App() {
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [agreement, setAgreement] = useState(50);

  const handleSend = () => {
    if (!userInput.trim()) return;
    
    const randomResponse =
      hardcodedResponses[Math.floor(Math.random() * hardcodedResponses.length)];
    
    setMessages([...messages, { text: userInput, sender: "user" }, { text: randomResponse, sender: "bot" }]);
    setUserInput("");
  };

  return (
    <div className="container">
      <h1>Today's News</h1>
      <div className="news-list">
        {newsArticles.map((article, index) => (
          <button key={index} onClick={() => setSelectedArticle(article)} className="news-item">
            {article.title}
          </button>
        ))}
      </div>
      {selectedArticle && (
        <div className="news-summary">
          <h2>{selectedArticle.title}</h2>
          <p>{selectedArticle.summary}</p>
          <a href={selectedArticle.link} target="_blank" rel="noopener noreferrer">
            Read more
          </a>
          <div className="engagement-box">
            <label>Agreement Level: {agreement}%</label>
            <input
              type="range"
              min="0"
              max="100"
              value={agreement}
              onChange={(e) => setAgreement(e.target.value)}
            />
            <div className="chat-thread">
              {messages.map((msg, index) => (
                <p key={index} className={msg.sender}>{msg.text}</p>
              ))}
            </div>
            <textarea
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Share your thoughts..."
            ></textarea>
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
