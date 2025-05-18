import streamlit as st
import pandas as pd
import xgboost as xgb

# I load your trained model
model = xgb.Booster()
model.load_model("xgboost_model.json")

# Title of the app
st.title("Malaria Prediction App")

# Input data
st.header("**Patients Information**")

Age = st.number_input("Age", min_value=20, max_value=84, value=30)
Cough = st.selectbox("Cough", ["Yes", "No"])
EndemicArea = st.selectbox("EndemicArea", ["Yes", "No"])
AbdominalPain = st.selectbox("Abdominal Pain", ["Yes", "No"])
Vaccination = st.selectbox("Vaccination", ["Yes", "No"])
Mosquitos = st.selectbox("Mosquitos", ["Yes", "No"])
HighRiskGroup = st.selectbox("HighRiskGroup", ["Yes", "No"])
AreaOutbreak = st.selectbox("AreaOutbreak", ["Yes", "No"])
Chills = st.selectbox("Chills", ["Yes", "No"])
Fatique = st.selectbox("Fatigue", ["Yes", "No"])

# Prepare the input data for prediction
input_data = pd.DataFrame({
    'Age': [(Age - 20) / (84 - 20)],
    'Cough': [1 if Cough == "Yes" else 0],
    'EndemicArea': [1 if EndemicArea == "Yes" else 0],
    'AbdominalPain': [1 if AbdominalPain == "Yes" else 0],
    'Vaccination': [1 if Vaccination == "Yes" else 0],
    'Mosquitos': [1 if Mosquitos == "Yes" else 0],
    'HighRiskGroup': [1 if HighRiskGroup == "Yes" else 0],
    'AreaOutbreak': [1 if AreaOutbreak == "Yes" else 0],
    'Chills': [1 if Chills == "Yes" else 0],
    'Fatique': [1 if Fatique == "Yes" else 0]  
    
})

# Convert DataFrame to DMatrix for prediction
dmatrix = xgb.DMatrix(input_data)

if st.button("Predict"):
    predictions = model.predict(dmatrix)
    
    st.write("Prediction Probabilities:")
    st.write(predictions)
    
    threshold = st.slider("Select a threshold", min_value=0.0, max_value=1.0, value=0.5)
    
    predicted_class = "Malaria" if (predictions > threshold)[0] else "No Malaria"
    
    st.write("Predicted Outcome:")
    st.write(predicted_class)

    if predicted_class == "Malaria":
        st.write("You have symptoms that indicate malaria; please go for a check-up.")
    else:
        st.write("No, you are free from malaria; consider trying other tests.")