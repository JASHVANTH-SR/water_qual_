import streamlit as st
from PIL import Image
from multiapp import MultiApp
from Water_qual import sample,sample2,qual_calc,eda,eda2,vlp1,vlp2,chatbot # import your app modules here
from Water_qual import *
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.model_selection import train_test_split

# Modelling Libraries
from sklearn.linear_model import LogisticRegression,RidgeClassifier,SGDClassifier,PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC,LinearSVC,NuSVC
from sklearn.neighbors import KNeighborsClassifier,NearestCentroid
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB,BernoulliNB
from sklearn.ensemble import VotingClassifier

# Evaluation & CV Libraries
from sklearn.metrics import precision_score,accuracy_score
from sklearn.model_selection import RandomizedSearchCV,GridSearchCV,RepeatedStratifiedKFold
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen.canvas import Canvas
from PIL import ImageGrab
def save_as_pdf(app):
    # Capture screenshot of the entire page
    screenshot = ImageGrab.grab()
    screenshot = screenshot.transpose(method=Image.Transpose.ROTATE_270)

    # Save screenshot as PDF
    pdf_path = 'streamlit_app_output.pdf' # Path to save the PDF
    screenshot.save(pdf_path)

    print(f'Streamlit app output saved as PDF: {pdf_path}')

st.set_page_config(page_title="Water Quality", page_icon="🌾", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("The Water Quality Analysis App")
image = Image.open('tree.jpg')
st.image(image)
image = Image.open('tvalluvar.jpeg')
st.image(image)
st.markdown("நீரின்று அமையாது உலகெனின் யார்யார்க்கும்") 
st.markdown("வானின்று அமையாது ஒழுக்கு")


app1 = MultiApp()

# Add all your application here
app1.add_app("Individual Interpreter(Manual Upload)", sample.app)
app1.add_app("Individual Interpreter(Built in Dataset)", sample2.app)
app1.add_app("Summary Overall(Manual Upload)", vlp1.app)
app1.add_app("Summary Overall(Built in Dataset)", vlp2.app)
app1.add_app("Water Quality calculator", qual_calc.app)
app1.add_app("Exploratory Data Analysis(Manual Upload)", eda.app)
app1.add_app("Exploratory Data Analysis(Built in Dataset)", eda2.app)
app1.add_app("Querybot",chatbot.app)

app1.run()
if st.button('Save as PDF'):
        save_as_pdf(app1)
if st.button('show app credit'):
  st.markdown('''### This is the **Study App** created in Streamlit using the **pandas-profiling** library.
****Credit:**** App built in `Python` + `Streamlit` by [JASHVANTH S R ](https://www.linkedin.com/in/jashvanth-s-r-476646213)[HARUL GANESH S B ](https://www.linkedin.com/in/harul-ganesh/)[BALAJI S ](https://www.linkedin.com/in/balaji-s-csbs-dept-03790a202/)[GOWTHAM H](https://www.linkedin.com/in/gowtham-haribabu-9425861bb/)
---
''')
