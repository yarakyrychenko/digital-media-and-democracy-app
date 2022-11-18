import pandas as pd, streamlit as st
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS

data = pd.read_excel("data_review.xlsx").fillna("Unknown")
countries = list(data.country.unique())
countries.insert(0, "All")
years = list(data.Year.unique())
years.insert(0, "All")
effects = list(data.effect.unique())
effects.insert(0, "All")

data["text"] = [str(data.loc[i, "Title"]) + " " + str(data.loc[i, "Abstract.Note"]) for i in range(len(data))]

st.title(" Digital Media and Democracy") 
st.subheader("Create a wordcloud out of titles and abstracts of papers about digital media and democracy!")

def preprocess(out):
    text = " ".join(out)
    text = text.lower()
    #text = re.sub(pattern=r"http\S+",repl="",string=text.lower())
    #text = re.sub(pattern=r"@\S+",repl="",string=text)
    return text

def make_wordcloud(out):
    text = preprocess(out)
    wordcloud = WordCloud(width=1800, height=1200,stopwords=STOPWORDS,
                        max_font_size=250, max_words=200, background_color="white",
                        colormap='cool', collocations=True).generate(text)  

    fig = plt.figure(figsize=(18,12))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return fig

def get_filtered_txt(data, filtervar):
    if filtervar == "All":
        return data.text
    else:
        return data[data.country==filtervar].text

st.markdown("First, let's check how the research field evolved over time.")
st.selectbox("Filter by year", years, key="YEAR")

ytexts = get_filtered_txt(data, st.session_state.YEAR )
figure = make_wordcloud(ytexts)

st.markdown(f"The wordcloud is based on {len(texts)} articles.")
st.pyplot(figure)

st.markdown("Let's see how the abstracts differ by country.")
st.selectbox("Filter by country", countries, key="COUNTRY")

ctexts = get_filtered_txt(data, st.session_state.COUNTRY )
figure = make_wordcloud(ctexts)

st.markdown(f"The wordcloud is based on {len(texts)} articles.")
st.pyplot(figure)

