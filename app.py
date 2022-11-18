import pandas as pd, streamlit as st
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS

data = pd.read_excel("data_effects.xlsx").fillna("Unknown")
countries = list(data.country.unique())
countries.insert(0, "All")
years = (data.Year.unique())
years.insert(0, "All")
data.effect = pd.Categorical(data.effect).rename_categories({-1: 'Detrimental', 0: 'No association', 1: "Beneficial"})
effects = list(data.effect.unique())
effects.insert(0, "All")

# Abstract.Note for data_review
data["text"] = [str(data.loc[i, "Title"]) + " " + str(data.loc[i, "Abstract Note...8"]) for i in range(len(data))]

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

def get_filtered_txt(data, filtervars, vars = ["Year", "effect", "country"]):
    newdata = data.copy()
    for i in range(len(vars)):
        if filtervars[i] == "All":
            pass
        else:
            newdata = newdata[newdata[vars[i]]==filtervars[i]]
    return newdata.text


st.selectbox("Filter by year", years, key="YEAR")
st.selectbox("Filter by effect", effects, key="EFFECT")
st.selectbox("Filter by country", countries, key="COUNTRY")

filters = [st.session_state.YEAR , st.session_state.EFFECT, st.session_state.COUNTRY ]
texts = get_filtered_txt(data, filters)
if len(texts) == 0:
    st.markdown("There are no articles matching your selection criteria.")
else:
    st.markdown(f"There are {len(texts)} articles matching your selection criteria.")
    figure = make_wordcloud(texts)
    st.pyplot(figure)

