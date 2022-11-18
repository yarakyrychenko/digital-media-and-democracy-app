import pandas as pd, streamlit as st
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS

data = pd.read_excel("data_effects.xlsx").fillna("Unknown")
data.country = data.country.apply(lambda x: "USA" if x == "United States" else x)
countries = list(data.country.unique()).sort(reverse=True)
countries.insert(0, "All")
data.Year = data.Year.apply(lambda x: str(x)[:4])
years = list(data.Year.unique()).sort(reverse=True)
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

def make_wordcloud(out, color):
    text = preprocess(out)
    wordcloud = WordCloud(width=1800, height=1200,stopwords=STOPWORDS,
                        max_font_size=250, max_words=150, background_color="white",
                        colormap=color, collocations=True).generate(text)  

    fig = plt.figure(figsize=(18,12))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return fig

def get_filtered_txt(data, filtervars, vars = ["Year", "effect", "country"]):
    newdata = data.copy()
    for i in range(len(vars)):
        if len(filtervars[i]) == 0:
            pass 
        elif filtervars[i][0] == "All":
            pass
        else:
            tuplefilt = tuple(filtervars[i])
            newdata = newdata.query(f'{vars[i]} in {tuplefilt}')
    return newdata.text


st.multiselect("Filter by year", years, default=["All"], key="YEAR")
st.multiselect("Filter by effect", effects, default=["All"], key="EFFECT")
st.multiselect("Filter by country", countries, default=["All"], key="COUNTRY")

filters = [st.session_state.YEAR , st.session_state.EFFECT, st.session_state.COUNTRY ]
texts = get_filtered_txt(data, filters)
if len(texts) == 0:
    st.markdown("There are no articles matching your selection criteria.")
else:
    st.markdown(f"There are {len(texts)} articles matching your selection criteria.")
    if st.session_state.EFFECT == ["Detrimental"]:
        color = 'autumn' 
    elif st.session_state.EFFECT == ["Beneficial"]:
        color = 'summer' 
    else: 
        color = 'cool'

    figure = make_wordcloud(texts, color)
    st.pyplot(figure)

