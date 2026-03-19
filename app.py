import streamlit as st
import json

from utils.feature_extractor import extract_features
from model.preprocess import load_model
from agent.decision_engine import decide_next_step
from agent.llm_handler import ask_llm

# ==============================
# Load Model
# ==============================
model = load_model()

# ==============================
# Session State
# ==============================
if "history" not in st.session_state:
    st.session_state.history = []

if "features" not in st.session_state:
    st.session_state.features = {}

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# ==============================
# UI
# ==============================
st.set_page_config(page_title="AI Insurance Assistant", layout="wide")
st.title("🤖 AI Insurance Assistant")

# ==============================
# Show Chat History
# ==============================
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ==============================
# Input
# ==============================
user_input = st.chat_input("Describe your situation...")

if user_input and (len(st.session_state.history) == 0 or st.session_state.history[-1]["content"] != user_input):

    # 🚨 STOP if already processed
    #if st.session_state.get("last_processed") == user_input:
      #  st.stop()
    # Save current input
    st.session_state["last_processed"] = user_input

    # Save user message
    st.session_state.history.append({"role": "user", "content": user_input})

    # ------------------------------
    # Detect last question
    # ------------------------------
    last_question = None
    if len(st.session_state.history) > 1:
        last_question = st.session_state.history[-2]["content"].lower()

    # ------------------------------
    # Handle follow-up answers
    # ------------------------------
    if last_question and "third party" in last_question:
        st.session_state.features["third_party"] = user_input.lower()

    elif last_question and "damage level" in last_question:
        st.session_state.features["damage_level"] = user_input.lower()

    else:
        extracted = extract_features(user_input)
        try:
            features = json.loads(extracted)
            st.session_state.features.update(features)
        except:
            pass

    # ------------------------------
    # Decision Engine
    # ------------------------------
    decision = decide_next_step(str(st.session_state.features))

    # ------------------------------
    # Agent Logic
    # ------------------------------
    if decision == "ask_third_party":
        bot_reply = "Was another vehicle or third party involved?"

    elif decision == "ask_damage":
        bot_reply = "What is the damage level? (low / medium / high)"

    else:
        try:
            third_party = st.session_state.features.get("third_party", "no").lower()
            third_party_val = 1 if third_party == "yes" else 0

            damage = st.session_state.features.get("damage_level", "low").lower()

            if damage == "high":
                damage_val = 2
            elif damage == "medium":
                damage_val = 1
            else:
                damage_val = 0

            model_input = [[third_party_val, damage_val]]
            prediction = model.predict(model_input)[0]

            # Simple explanation (no API dependency)
            if prediction == "Accident":
                explanation = "The prediction is Accident because high damage and third-party involvement indicate a severe case."
            else:
                explanation = "The prediction is Minor because the damage is low and no major external involvement is detected."

            bot_reply = f"### ✅ Prediction: {prediction}\n\n### 🧠 Explanation:\n{explanation}"

        except Exception as e:
            bot_reply = f"Prediction Error: {e}"

    # Save bot reply
    st.session_state.history.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.write(bot_reply)

# ==============================
# MAIN LOGIC
# ==============================
if user_input and user_input != st.session_state.last_input:

    st.session_state.last_input = user_input

    # Save user message
    st.session_state.history.append({"role": "user", "content": user_input})

    # ------------------------------
    # Detect last question
    # ------------------------------
    last_question = None
    if len(st.session_state.history) > 1:
        last_question = st.session_state.history[-2]["content"].lower()

    # ------------------------------
    # Handle follow-up answers
    # ------------------------------
    if last_question and "third party" in last_question:
        st.session_state.features["third_party"] = user_input.lower()

    elif last_question and "damage level" in last_question:
        st.session_state.features["damage_level"] = user_input.lower()

    else:
        # First input → use LLM
        extracted = extract_features(user_input)
        try:
            features = json.loads(extracted)
            st.session_state.features.update(features)
        except:
            pass

    # ------------------------------
    # Decision Engine
    # ------------------------------
    decision = decide_next_step(str(st.session_state.features))

    # ------------------------------
    # Agent Logic
    # ------------------------------
    if decision == "ask_third_party":
        bot_reply = "Was another vehicle or third party involved?"

    elif decision == "ask_damage":
        bot_reply = "What is the damage level? (low / medium / high)"

    else:
        try:
            # ==============================
            # Convert features → numeric
            # ==============================
            third_party = st.session_state.features.get("third_party", "no").lower()
            third_party_val = 1 if third_party == "yes" else 0

            damage = st.session_state.features.get("damage_level", "low").lower()

            if damage == "high":
                damage_val = 2
            elif damage == "medium":
                damage_val = 1
            else:
                damage_val = 0

            model_input = [[third_party_val, damage_val]]

            # ==============================
            # Prediction
            # ==============================
            prediction = model.predict(model_input)[0]

            # ==============================
            # Explanation using LLM
            # ==============================
            explanation_prompt = f"""
User input: {user_input}
Features: {st.session_state.features}
Prediction: {prediction}

Explain clearly why this prediction was made.
"""

            explanation = ask_llm(explanation_prompt)

            if "Error" in explanation:
                if prediction == "Accident":
                    explanation = "The prediction is Accident because high damage and third-party involvement indicate a severe case."
                else:
                    explanation = "The prediction is Minor because the damage is low and no major external involvement is detected."

            bot_reply = f"### ✅ Prediction: {prediction}\n\n### 🧠 Explanation:\n{explanation}"

        except Exception as e:
            bot_reply = f"Prediction Error: {e}"

    # ------------------------------
    # Save + Display Response
    # ------------------------------
    st.session_state.history.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.write(bot_reply)