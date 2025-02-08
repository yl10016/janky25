import React, { useState } from "react";
import "./styles.css";

const newsTopic = {
  title: "Trade and Tariffs",
  description: "Description blah blah blah"
};

const newsArticles = [
  {
    title: "It's not over: Donald Trump could still blow up global trade",
    summary: "Ideology, complacent markets and a need for revenue may still lead to big tariffs",
    link: "https://www.economist.com/leaders/2025/02/06/its-not-over-donald-trump-could-still-blow-up-global-trade",
    image: "https://www.economist.com/cdn-cgi/image/width=1424,quality=80,format=auto/content-assets/images/20250208_LDD002.jpg"
  },
  {
    title: "Japanese leader tries flattering Trump in bid to avert tariffs\n",
    summary: "Trump's meeting with Japan's prime minister ended with a tariff warning, but praise from the Japanese side eased tensions",
    link: "https://www.washingtonpost.com/politics/2025/02/07/trump-japan-prime-minister-meeting/",
    image: "https://www.washingtonpost.com/wp-apps/imrs.php?src=https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/72ULYKJYQO7HSKLUFQX3KPQ2PM_size-normalized.jpg"
  },
  {
    title: "Trump racks up wins on tariffs, immigration, and foreign policy",
    summary: "The 'Outnumbered' panelists discuss President Donald Trump's recent wins on immigration, trade, and foreign policy",
    link: "https://www.foxnews.com/video/6368256078112",
    image: "https://a57.foxnews.com/static.foxnews.com/foxnews.com/content/uploads/2025/02/1440/810/trumpsteel.png?ve=1&tl=1"
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
      <div className="news-topic">
        <h2>{newsTopic.title}</h2>
        <p>{newsTopic.description}</p>
      </div>
      <div className="news-list" style={{ display: "flex", justifyContent: "space-around", width: "100%" }}>
        {newsArticles.map((article, index) => (
          <div key={index} className="news-item" onClick={() => setSelectedArticle(article)}>
            <h3>{article.title}</h3>
            <img src={article.image} alt={article.title} className="news-image" />
          </div>
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
            <button onClick={handleSend}>Send Agreement Level</button>
            <div className="chat-thread">
              {messages.map((msg, index) => (
                <p key={index} className={msg.sender}>{msg.text}</p>
              ))}
            </div>
            <textarea
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Share your thoughts..."
              style={{ width: "70%" }}
            ></textarea>
            <button onClick={handleSend}>Send Thoughts</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
