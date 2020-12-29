#  The MIT License (MIT)
#  Copyright (c) 2020 Sergio Ahumada <sahumada@texla.cl>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.

import bs4
import pandas as pd
import requests
import time

seasons = ["{}-{:0>2}".format(i, (i + 1) % 100) for i in range(1963, 2020)]
webpage = 'https://www.bdfutbol.com/en/t/tger'


def bundesliga_data_collection():
    for s in seasons:
        url = "{}{}.html".format(webpage, s)
        print("processing url: {}".format(url))

        html = requests.get(url).response.text
        soup = bs4.BeautifulSoup(html, "html.parser")
        table = soup.find(id="classific")
        df_scores = pd.read_html(str(table))[0]

        df_scores.drop(columns=['Unnamed: 0', 'Unnamed: 2'],
                       inplace=True)

        df_scores.rename({'Unnamed: 1': 'position',
                          'Unnamed: 3': 'club',
                          'Pts.': 'points'},
                         axis=1, inplace=True)

        df_scores.to_csv("{}.csv".format(s), encoding='utf-8', index=False)

        time.sleep(0.2)

bundesliga_data_collection()

