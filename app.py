import pandas as pd, streamlit as st
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS
from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

data = pd.read_excel("data_effects.xlsx").fillna("Unknown")
data.country = data.country.apply(lambda x: "USA" if x == "United States" else x)
countries = list(data.country.unique())
countries.sort(reverse=True)
countries.insert(0, "All")
data.Year = data.Year.apply(lambda x: str(x)[:4])
years = list(data.Year.unique())
years.sort(reverse=True)
years.insert(0, "All")
data.effect = pd.Categorical(data.effect).rename_categories({-1: 'Detrimental', 0: 'No association', 1: "Beneficial"})
effects = list(data.effect.unique())
effects.insert(0, "All")

# Abstract.Note for data_review
data["text"] = [str(data.loc[i, "Title"]) + " " + str(data.loc[i, "Abstract Note...8"]) for i in range(len(data))]

#lottie_tweet = load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_tnrzlN.json')
#st_lottie(lottie_tweet, speed=1, height=200, key="initial")

st.markdown("<h1 style='text-align: center;'> Digital Media and Democracy </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>  wordclouds of titles and abstracts of scientific papers </h3>", unsafe_allow_html=True)

stopwords = STOPWORDS.update(["find", "study", "investigate", "result", "sample", 
                                "finding", "paper", "article", "results", "findings",
                                "test", "one", "two", "three", 
                                "social", "media"])

def preprocess(out):
    text = " ".join(out)
    text = text.lower()
    #text = re.sub(pattern=r"http\S+",repl="",string=text.lower())
    #text = re.sub(pattern=r"@\S+",repl="",string=text)
    return text

def make_wordcloud(out, color):
    text = preprocess(out)
    wordcloud = WordCloud(width=1800, height=1200,stopwords=stopwords,
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


st.multiselect("Filter by year of publication", years, default=["All"], key="YEAR")
st.multiselect("Filter by effect of digital media on democracy", effects, default=["All"], key="EFFECT")
st.multiselect("Filter by country of study", countries, default=["All"], key="COUNTRY")

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

st.markdown("""

---

By [@YaraKyrychenko](https://twitter.com/YaraKyrychenko) based on data from:

Lorenz-Spreen, P., Oswald, L., Lewandowsky, S. et al. [A systematic review of worldwide causal and correlational evidence on digital media and democracy.](https://doi.org/10.1038/s41562-022-01460-1) Nat Hum Behav (2022).

[Data (OSF)](https://osf.io/7ry4a/) [Web App (GitHub)](https://github.com/yarakyrychenko/digital-media-and-democracy-app) 
""")
