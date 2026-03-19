# 🤖 AI Insurance Assistant (Agentic AI + ML)

## 🚀 Overview

AI Insurance Assistant is an intelligent system that combines **Large Language Models (LLMs)** with **Machine Learning** to assist users in identifying insurance categories based on real-world scenarios.

The system behaves like an **AI agent** that interacts with users, asks follow-up questions, extracts structured data, and provides predictions with explanations.

---

## ✨ Features

* 💬 Chat-based interface using Streamlit
* 🧠 LLM-powered natural language understanding
* 🔄 Multi-step reasoning (Agent behavior)
* 📊 ML-based insurance category prediction
* 📝 Explainable AI outputs
* ⚡ Robust fallback (works even without API)

---

## 🧠 Architecture

User Input → LLM → Feature Extraction → Agent Decision
→ Follow-up Questions → ML Model → Prediction → Explanation

---

## ⚙️ Tech Stack

* Python
* Streamlit
* OpenAI API
* Scikit-learn
* Pandas

---

## 🧩 How It Works

1. User describes an insurance-related issue
2. LLM extracts key features
3. Agent decides next step:

   * Ask follow-up questions
   * OR predict directly
4. ML model predicts insurance category
5. System explains the prediction

---

## 🧪 Example

**Input:**
I had a car accident and my vehicle is badly damaged

**Flow:**

* Was another vehicle involved? → yes
* What is the damage level? → high

**Output:**
Prediction: Accident
Explanation: High damage and third-party involvement indicate a severe case

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/ai-insurance-agent.git
cd ai-insurance-agent
pip install -r requirements.txt
streamlit run app.py
```

---

## 📌 Future Improvements

* Add RAG (insurance knowledge base)
* Improve ML model with real dataset
* Deploy on cloud
* Add voice interaction

---

## 👨‍💻 Author

Vivek Shinde
