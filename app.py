import pandas as pd, streamlit as st
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS

data = pd.read_excel("data_review.xlsx")
countries = list(data.country)
data.text = data.Title + " " + data["Abstract.Note"]
st.title(" Digital Media and Democracy") 
st.subheader("Create a wordcloud out of abstracts of papers about digital media and democracy!")

st.radio("Filter by country", countries, key="COUNTRY")

def preprocess(out):
    text = " ".join(out)
    text = text.lower()
    #text = re.sub(pattern=r"http\S+",repl="",string=text.lower())
    #text = re.sub(pattern=r"@\S+",repl="",string=text)
    return text

def make_wordcloud(out):
    text = preprocess(out)
    wordcloud = WordCloud(width=1800, height=1200,stopwords=STOPWORDS,
                        max_font_size=250, max_words=100, background_color="white",
                        colormap='cool', collocations=True).generate(text)  

    fig = plt.figure(figsize=(18,12))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return fig


texts = data[data.country==st.session_state.COUNTRY].text
figure = make_wordcloud(texts)
st.pyplot(figure)
