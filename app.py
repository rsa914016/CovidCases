import folium
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


def find_top_confirmed(n=15):
    df = pd.read_csv('covid data.csv')
    by_country = df.groupby('Country').sum()[['Confirmed']]
    df = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return df


cdf = find_top_confirmed()
pairs = [(country, int(confirmed)) for country, confirmed
         in zip(cdf.index, cdf['Confirmed'])]

corona_df = pd.read_csv('covid data.csv')
lst = ['Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active']
corona_df = corona_df[lst]
corona_df = corona_df.dropna()
corona_df = corona_df.astype('int')

m = folium.Map(location=[20.593684, 78.96288],
               tiles='Stamen toner',
               zoom_start=4)

temp1 = 'Confirmed : {}\nDeaths : {}\n'
temp2 = 'Recovered : {}\nActive : {}'
template = temp1 + temp2


def circle_maker(x):
    folium.Circle(location=(x[0], x[1]),
                  radius=float(x[2]),
                  color='red',
                  popup=template.format(*x[2:])).add_to(m)


corona_df.apply(lambda x: circle_maker(x), axis=1)
html_map = m._repr_html_()


@app.route('/')
def home():
    return render_template('home.html',
                           table=cdf, cmap=html_map, pairs=pairs)


if __name__ == '__main__':
    app.run(debug=True)
