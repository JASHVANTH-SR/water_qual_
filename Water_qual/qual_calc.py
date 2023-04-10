import streamlit as st


# Set up Streamlit app
def app():
    def is_potable(SAR,pH_GEN,TDS,NO2_NO3,Cl,SO4,F,HCO3,EC_GEN,RSC,Mg,Na):
    #"""Function that determines if water is potable based on the given inputs."""
        if (SAR<=26 and pH_GEN<=8.5 and pH_GEN>=6.5 and TDS<1200 and NO2+NO3<20 and Cl<250 and SO4<200 and F<=1 and HCO3<400 and EC_GEN<1500 and RSC<2.5 and Mg<37.5 and Na<=270):
            return "Potable"
        else:
            return "Not Potable"

    st.title("Water Potability Checker")
    st.write("Enter the following water quality parameters:")

    # Set up user input fields
    TDS = st.number_input("TDS")
    NO2_NO3 = st.number_input("NO2+NO3")
    Mg = st.number_input("Mg")
    K = st.number_input("K")
    Cl = st.number_input("Cl")
    SO4 = st.number_input("SO4")
    CO3 = st.number_input("CO3")
    HCO3 = st.number_input("HCO3")
    F = st.number_input("F")
    pH_GEN = st.number_input("pH_GEN")
    EC_GEN = st.number_input("EC_GEN")
    SAR = st.number_input("SAR")
    RSC = st.number_input("RSC")
    Na = st.number_input("Na")
    # Calculate if water is potable or not
    result = is_potable(SAR,pH_GEN,TDS,NO2_NO3,Cl,SO4,F,HCO3,EC_GEN,RSC,Mg,Na)

    # Display result
    st.write("Water is:", result)
