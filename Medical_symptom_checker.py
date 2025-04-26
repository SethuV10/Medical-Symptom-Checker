import streamlit
import streamlit as st
from ner_module import extract_symptoms
from model_module import predict_condition
from db_module import insert_log
import spacy
nlp = spacy.load("en_core_web_sm")
st.title("Medical Symptom Checker")
user_input = st.text_area("Describe your symptoms", height=200)
def predict_condition(symptoms):
    predictions = []

    if "fever" in symptoms and "cough" in symptoms:
        predictions.append(("Flu", 0.9))
    if "headache" in symptoms and "nausea" in symptoms:
        predictions.append(("Migraine", 0.85))
    if "fatigue" in symptoms:
        predictions.append(("Anemia", 0.75))

    if not predictions:
        predictions.append(("Unknown condition", 0.5))

    return predictions


if st.button("Check Possible Conditions"):
    if user_input.strip():
        with st.spinner("Analyzing your symptoms..."):
            symptoms = extract_symptoms(user_input)
            predictions = predict_condition(symptoms)
            insert_log(symptoms, predictions)

        st.subheader(" Extracted Symptoms:")
        st.write(symptoms if symptoms else "No medical terms found.")

        st.subheader(" Possible Conditions:")
        for condition, score in predictions:
            st.markdown(f"**{condition}** (Confidence: {score:.2f})")
    else:
        st.warning("Please enter a description of your symptoms.")


