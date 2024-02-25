import bs4
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import googlesearch

query = str(input("Enter a search query to preform sentiment analysis on: "))
print()


def get_search_results(search_query='Google', num_sites=10, pause_time=2):
    search_results = googlesearch.search(search_query, num_results=num_sites, sleep_interval=pause_time)
    return search_results


def get_site_content(url):
    para_list = []
    html_obj = requests.get(url)
    html = html_obj.text
    # print(html)
    soupy = bs4.BeautifulSoup(html, 'html.parser')
    # print(soupy)
    paragraphs = soupy.findAll('p')
    # print(content)
    for para in paragraphs:
        para_list.append(para.get_text())
    return para_list


def vader_analysis(text):
    if type(text) == str:
        return SentimentIntensityAnalyzer().polarity_scores(text).get('compound')
    elif type(text) == list:
        avg = 0
        for sent in text:
            senti = SentimentIntensityAnalyzer().polarity_scores(sent).get('compound')
            if senti != 0.0:
                avg += senti
        if len(text) != 0:
            avg /= len(text)
        else:
            return 'sentiment could be not preformed'
        return round(avg, 2)
    return 'sentiment could not be preformed'


results = get_search_results(query, num_sites=10, pause_time=5)

print("Vader Scale: -1 (extremely negative) to 1 (extremely positive)")
print("------------------------------------------------------------------------")
for site in results:
    content = get_site_content(site)
    vader = vader_analysis(content)
    feels = ""
    if type(vader) != float:
        print(f"{site}: {vader}")
        print()
        continue
    elif vader >= 0.5:
        feels = "Positive"
    elif vader <= -0.5:
        feels = "Negative"
    else:
        feels = "Neutral"

    print(f"{site}: {vader} ({feels})")
    print()
