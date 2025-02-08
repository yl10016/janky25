import React, { useState } from "react";
import "./styles.css";
import {
  onSnapshot, addDoc
} from "firebase/firestore"
import { responsesCollection } from "./firebase"

const newsPath = "/example.csv";
const titlePath = "/title.txt";

const newsTopic = {
  title: "Trump, Trade and Tariffs",
  description: "Description blah blah blah"
};

const hardcodedResponses = [
  "That's an interesting perspective!",
  "I see your point. What other solutions might work?",
  "This is a complex issue, isn't it?",
];

function App() {
  const [newsTopic, setNewsTopic] = useState({ title: "", description: "" });
  const [newsArticles, setNewsArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [agreement, setAgreement] = useState(50);
  const [responses, setResponses] = useState([]);
  const [agreementSent, setAgreementSent] = useState(false);
  const [datasetIndex, setDatasetIndex] = useState(1);
  
  const chatEnd = React.useRef(null);

  React.useEffect(() => {
    // Load topic data
    fetch(titlePath)
      .then(response => response.text())
      .then(text => {
        const [title, description] = text.split("\n");
        setNewsTopic({ title: title.trim(), description: description.trim() });
      });
  }, []);

  React.useEffect(() => {
    const unattacher = onSnapshot(responsesCollection, function(snapshot){
      const unrolledResponses = snapshot.docs.map(doc => {
        return {
          ...doc.data(),
          id: doc.id
        }
      })
      const filteredResponses = unrolledResponses.filter(obj => {
        return selectedArticle && obj['doc_id'] == selectedArticle['id']
      })
      console.log(filteredResponses)
      setResponses(filteredResponses)
    })
    return unattacher
  }, [selectedArticle])

  React.useEffect(() => {
    console.log(selectedArticle)
    if(!userInput) return;
    addDoc(responsesCollection, {
      'doc_id': selectedArticle['id'],
      'agreement': agreement,
      'comment': userInput
    })
  }, [userInput])

  React.useEffect(() => {
    chatEnd.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages])

  const handleSend = () => {
    if (!userInput.trim()) return;
    
    const randomResponse =
      hardcodedResponses[Math.floor(Math.random() * hardcodedResponses.length)];
    
    setMessages([...messages, { text: userInput, sender: "user" }, { text: randomResponse, sender: "bot" }]);
    setUserInput("");
  };

  React.useEffect(() => {
    // Load CSV data
    fetch(newsPath)
      .then(response => response.text())
      .then(csvText => {
        const allArticles = parseCSV(csvText);
        updateNewsArticles(allArticles);
      });
  }, [datasetIndex]);

  React.useEffect(() => {
    // Change dataset every 12 hours
    const interval = setInterval(() => {
      setDatasetIndex(prevIndex => prevIndex + 1);
    }, 12 * 60 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const parseCSV = (csvText) => {
    const rows = csvText.split("\n").slice(1);
    return rows.map(row => {
      const [id, title, summary, link, image] = row.split("	");
      return { id: parseInt(id, 10), title, summary, link, image };
    }).filter(article => article.id);
  };

  const updateNewsArticles = (allArticles) => {
    const startId = datasetIndex * 3 - 2;
    const filteredArticles = allArticles.filter(article =>
      article.id >= startId && article.id < startId + 3
    );
    setNewsArticles(filteredArticles);
  };

  const handleSendAgreement = () => {
    setAgreementSent(true);
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
            <center>
              <div className="agreement-box">
                <label>Agreement Level: <span className="bold">{agreement}%</span></label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={agreement}
                  onChange={(e) => setAgreement(e.target.value)}
                  className="styled-slider"
                  disabled={agreementSent}
                />
                <button className="button" onClick={handleSendAgreement} disabled={agreementSent}>Send</button>
              </div>
            </center>
            {agreementSent && <p>Your agreement level: {agreement}%</p>}
            <div className="chat-thread">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.sender}`}>
                  {msg.text}
                </div>
              ))}
            </div>
            {!agreementSent && <textarea
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Respond freely here!..."
            ></textarea>}
            {!agreementSent && <button onClick={handleSend}>Send Thoughts!</button>}
            <div ref={chatEnd} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
