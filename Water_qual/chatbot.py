import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections
import random

# Define the chatbot responses
keywords_response = {
    # Add your keywords and responses here
    # Example:
    r"(hi|hello|hey)": ["Hello! How can I help you"],
    r"what is your name": ["My name is ChatGPT.", "You can call me ChatGPT."],
    # Add more patterns and responses as needed
        # SAR
    r"(SAR|sodium adsorption ratio)": ["The Sodium Adsorption Ratio (SAR) is a parameter that measures the concentration of sodium in relation to calcium and magnesium in water. SAR should be less than or equal to 26 for safe drinking water.", "High SAR values in water can indicate potential risk for soil degradation and crop damage."],

    # pH_GEN
    r"(pH_GEN|general pH)": ["The General pH (pH_GEN) is a measure of the acidity or alkalinity of water. pH_GEN should be between 6.5 and 8.5 for safe drinking water.", "pH values outside this range may indicate potential corrosion of pipes or adverse health effects."],

    # TDS
    r"(TDS|total dissolved solids)": ["Total Dissolved Solids (TDS) is a measure of the concentration of inorganic and organic substances dissolved in water. TDS should be less than 1200 mg/L for safe drinking water.", "High TDS levels can affect the taste, odor, and color of water and may indicate the presence of contaminants."],

    # NO2_NO3
    r"(NO2_NO3|nitrite and nitrate)": ["Nitrite and Nitrate (NO2_NO3) are nitrogen compounds that can be found in water due to pollution from agricultural runoff, septic systems, and other sources. The combined concentration of NO2 and NO3 should be less than 20 mg/L for safe drinking water.", "Elevated levels of NO2 and NO3 can indicate potential health risks, especially for infants and pregnant women."],

    # Cl
    r"(Cl|chloride)": ["Chloride (Cl) is an ion that can be found in water from natural sources, such as saltwater intrusion, as well as anthropogenic sources like road salt or wastewater discharge. Cl should be less than 250 mg/L for safe drinking water.", "High levels of Cl in water can affect taste, corrode pipes, and may indicate potential contamination."],

    # SO4
    r"(SO4|sulfate)": ["Sulfate (SO4) is an ion that can be found in water from natural sources, such as minerals in rocks and soils, as well as anthropogenic sources like industrial discharges. SO4 should be less than 200 mg/L for safe drinking water.", "Elevated levels of SO4 in water can affect taste, odor, and appearance, and may indicate potential health risks."],

    # F
    r"(F|fluoride)": ["Fluoride (F) is an ion that can be found in water from natural sources, such as minerals in rocks and soils, as well as anthropogenic sources like fluoridated water supplies. F should be less than or equal to 1.0 mg/L for safe drinking water.", "Excessive fluoride levels in water can cause dental fluorosis and other potential health risks."],

    # HCO3
    r"(HCO3|bicarbonate)": ["Bicarbonate (HCO3) is an ion that can be found in water from natural sources, such as carbonate rocks, as well as anthropogenic sources like wastewater discharge. HCO3 should be less than 400 mg/L for safe drinking water.", "High levels of HCO3 in water can affect taste, alkalinity, and may indicate potential contamination."],

    # EC_GEN
    r"(EC_GEN|general electrical conductivity)": ["General Electrical Conductivity (EC_GEN) or Conductivity is a measure of the ability of water to conduct electrical current and is related to the concentration of dissolved ions in water. EC_GEN should be less than 1500 µS/cm for safe drinking water.", "High EC_GEN levels in water can indicate potential contamination or presence of dissolved solids that may affect taste, quality, and potential health risks."],

    # RSC
r"(RSC|residual sodium carbonate)": ["Residual Sodium Carbonate (RSC) is a measure of the potential of water to cause sodium-related problems in soil and is calculated based on the concentration of bicarbonate, carbonate, and calcium ions. RSC should be less than 2.5 meq/L for safe drinking water.", "Elevated RSC levels in water can indicate potential risk for soil degradation, sodicity, and reduced crop yields."],

# Mg
r"(Mg|magnesium)": ["Magnesium (Mg) is an essential mineral and is naturally present in water from rocks and soils. Mg should be less than 37.5 mg/L for safe drinking water.", "High levels of Mg in water can affect taste, hardness, and may indicate potential contamination."],

# Na
r"(Na|sodium)": ["Sodium (Na) is an essential mineral and is naturally present in water from rocks and soils, as well as anthropogenic sources like saltwater intrusion and wastewater discharge. Na should be less than or equal to 270 mg/L for safe drinking water.", "High levels of Na in water can affect taste, hardness, and may indicate potential health risks, especially for individuals on low-sodium diets."],

   r"(potability|is the water potable|safe to drink)": ["Water potability refers to the suitability of water for drinking or other domestic uses. It is important to ensure that water meets the acceptable standards and guidelines for potability before consuming it.", "Potability of water can be determined by testing various parameters, including physical, chemical, and microbiological characteristics."],

    r"(Na%|sodium percentage|sodium content)": ["Sodium percentage (Na%) is a measure of the concentration of sodium in water, expressed as a percentage of the total dissolved solids. Acceptable Na% levels in drinking water may vary depending on regional guidelines, but generally, it is recommended to be below 10% for safe drinking water.", "High levels of sodium in drinking water can contribute to increased dietary sodium intake, which may be a concern for individuals with certain health conditions, such as high blood pressure or heart disease."],
    r"(K|potassium)": ["Potassium (K) is an essential nutrient for plant growth.", "Potassium is an important element in soil and water analysis."],

    r"(F|fluoride)": ["Fluoride (F) is a naturally occurring mineral that is added to drinking water in many communities to prevent dental cavities. Acceptable fluoride levels in drinking water may vary depending on regional guidelines, but generally, it is recommended to be within the range of 0.5 - 1.5 mg/L for safe drinking water.", "Excessive fluoride levels in drinking water can cause dental fluorosis, which is a cosmetic condition that affects the appearance of teeth. In some cases, high fluoride levels in water may also cause skeletal fluorosis, a condition that affects bones."]
}

# Create a function to get chatbot responses
def get_response(user_input):
    for pattern, responses in keywords_response.items():
        if nltk.re.search(pattern, user_input, nltk.re.IGNORECASE):
            return responses

# Set up Streamlit UI
def app():
    st.title("InfoBot")
    st.write("Type a message and ChatBot will respond!")

    # Chat input box
    user_input = st.text_input("You:", key='user_input')

    # Chat output box
    if st.button("Send"):
        responses = get_response(user_input)
        if responses:
            for response in responses:
                st.write("InfoBot:", response)
        else:
            st.write("InfoBot: I'm sorry, I don't understand. Can you please rephrase your question or provide more context?")

# Run the Streamlit app
