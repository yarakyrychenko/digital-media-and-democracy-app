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

outcomes = list(data.outcome_clean.unique())
outcomes.sort(reverse=True)
outcomes.insert(0, "All")

data.effect = pd.Categorical(data.effect).rename_categories({-1: 'decrease', 0: 'no association', 1: "increase"})
effects = list(data.effect.unique())
effects.insert(0, "All")

# Abstract.Note for data_review
data["text"] = [str(data.loc[i, "Title"]) + " " + str(data.loc[i, "Abstract Note...8"]) for i in range(len(data))]
data.text = data.text.apply(lambda text: text.lower())

#lottie_tweet = load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_tnrzlN.json')
#st_lottie(lottie_tweet, speed=1, height=200, key="initial")

st.markdown("<h1 style='text-align: center;'> Digital Media and Democracy </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'> wordclouds of titles and abstracts of scientific papers </h3>", unsafe_allow_html=True)

st.session_state.stopwords = STOPWORDS.union(set(["find", "study", "investigate", "result", "sample", 
                                "finding", "paper", "article", "results", "findings",
                                "test", "one", "two", "three", "examine"]))


def make_wordcloud(text, color, stopwords = st.session_state.stopwords):
    text = " ".join(text)
    wordcloud = WordCloud(width=1800, height=1200, stopwords = stopwords,
                        max_font_size=250, max_words=150, background_color="white",
                        colormap=color, collocations=True).generate(text)  

    fig = plt.figure(figsize=(18,12))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return fig

def get_filtered_data(data, filtervars, vars = ["Year", "outcome_clean", "effect", "country"]):
    newdata = data.copy()
    for i in range(len(vars)):
        if len(filtervars[i]) == 0:
            pass 
        elif filtervars[i][0] == "All":
            pass
        else:
            tuplefilt = tuple(filtervars[i])
            newdata = newdata.query(f'{vars[i]} in {tuplefilt}')
    return newdata


st.multiselect("Filter by outcome measure", outcomes, default=["All"], key="OUTCOME")
st.multiselect("Filter by effect of digital media on outcome", effects, default=["All"], key="EFFECT")
st.multiselect("Filter by country of study", countries, default=["All"], key="COUNTRY")
st.multiselect("Filter by year of publication", years, default=["All"], key="YEAR")

if "last_filters" not in st.session_state:
    st.session_state.last_filters = []

st.session_state.filters = [st.session_state.YEAR , st.session_state.OUTCOME, st.session_state.EFFECT, st.session_state.COUNTRY ]
st.session_state.changed = st.session_state.filters != st.session_state.last_filters

newdf = get_filtered_data(data, st.session_state.filters)

if st.session_state.changed:
    df = newdf.drop_duplicates(subset=["Title"])
    if len(df.text) == 0:
        st.markdown("There are no articles matching your selection criteria.")
    else:
        st.markdown(f"There are {len(df.text)} articles matching your selection criteria.")
        st.pyplot(make_wordcloud(df.text, "cool"))  
    st.session_state.last_filters = st.session_state.filters

    df = newdf.drop_duplicates(subset=["Title"])
    df = df[df["Year"] != "Unkn"]
    df["DOITrue"] = df.DOI.apply(lambda doi : len(doi) < 100)
    df = df[df["DOITrue"]]
    df.sort_values(by=['Year'], ascending=False, inplace=True)
    df.reset_index(inplace=True)

overtime = get_filtered_data(data, st.session_state.filters[1:3],["outcome_clean", "effect"])
overtime  = overtime[overtime["Year"] != "Unkn"]
overtime  = overtime[overtime["country"] != "Unknown"]
overtime  = overtime[overtime["country"] != "World"]
overtime_selected = get_filtered_data(overtime, [st.session_state.COUNTRY], ["country"])
overtime_selected["selection"] = [1]*len(overtime_selected)
overtime_not_selected = overtime[overtime.index not in overtime_selected.index]
overtime_not_selected["selection"] = [1]*len(overtime_not_selected)
to_line = pd.DataFrame(
    [overtime_selected[["Year","selection"]].groupby('Year').agg('sum')["selection"], overtime_not_selected[["Year","selection"]].groupby('Year').agg('sum')["selection"]],
    columns=['selected countries', 'not selected'])
st.line_chart(to_line)

st.slider("How many titles would you like to explore?", min_value=0, max_value=len(df), value= 10 if len(df) > 9 else len(df) , step=1, key="number_to_print")
st.markdown(f"Showing {st.session_state.number_to_print} most recent articles:")

for i in range(len(df)):
    if i == st.session_state.number_to_print:
        break
    st.markdown(f"{df.loc[i,'Year']}. {df.loc[i,'Title']} https://doi.org/{df.loc[i,'DOI']}")

st.markdown("""

---

By [@YaraKyrychenko](https://twitter.com/YaraKyrychenko) based on data from:

Lorenz-Spreen, P., Oswald, L., Lewandowsky, S. et al. [A systematic review of worldwide causal and correlational evidence on digital media and democracy.](https://doi.org/10.1038/s41562-022-01460-1) Nat Hum Behav (2022).

[Data (OSF)](https://osf.io/7ry4a/) [Web App (GitHub)](https://github.com/yarakyrychenko/digital-media-and-democracy-app) 
""")
