from bs4 import BeautifulSoup
import requests
import pandas as pd


title = ''
genre = ''
description = ''
data = []
urls = ["https://www.rottentomatoes.com/m/the_long_walk_of_carlos_guerrero",
        'https://www.rottentomatoes.com/m/kalki_2898_ad',
        'https://rottentomatoes.com/m/something_to_stand_for_with_mike_rowe',
        'https://www.rottentomatoes.com/m/horizon_an_american_saga_chapter_1',
        'https://www.rottentomatoes.com/m/a_quiet_place_day_one',
]

for url in urls:
     source = requests.get(url)
     soup = BeautifulSoup(source.text,'html.parser')
     headers = soup.find_all('div', class_='media-hero-wrap')
     descrps = soup.find_all('div', class_='media-scorecard no-border')
     for head in headers:
         meds = head.find_all('media-hero', attrs={'data-modulesnavigationmanager': 'mediaHero'})
         for ms in meds:
             h1s = ms.find_all("h1", attrs={'slot': 'titleIntro'})
             for h1 in h1s:
                 rts = h1.find_all('rt-text', attrs={'context':'label'})
                 for rt in rts:
                     span = rt.find('span') 
                     title = span.text.strip()
         gen = head.find("rt-text", attrs={'slot': 'genre'})
         genre = gen.text.strip()
                     
     for head in descrps:
         medias = head.find_all("media-scorecard", attrs={"data-mediascorecardmanager":"mediaScorecard"})
         for media in medias:
             drawers = media.find_all("drawer-more", attrs={"slot":"description"})
             for drawer in drawers:
                 des = drawer.find("rt-text", attrs={'slot':'content'})
                 description = des.text.strip()
                 data.append([title,genre,description])
                 
                 
                 
df = pd.DataFrame(data, columns=['Title','Genre','Description'])
df.to_csv("movies.csv", index=False)
    
                 