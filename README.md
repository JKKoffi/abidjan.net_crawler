# abidjan.net_crawler

## Running scripts

```
python crawler path_to_csv path_to_new_csv
```

## Requirements

* `BeautifulSoup`

* `requests`

* `pandas`
* `unicodedata`

* `regex`

## Contact
koffikouakoujonathan58@gmail.com

*If you lie this , left me a star.*

## Notebooks

In the folder `notebooks`, you'll find all the notebooks, i used to crawl these data.

* `Crawl_by_ID.ipynb` : use this to grab data when you now the id in the url (`https://business.abidjan.net/AL/a/id.asp`

* `Crawl_by_File.ipynb`: use this if you already have the a file containing data previously grabbed.

* ` Crawl_by_date.ipynb`: to grab by a date followin this format `day month year`. If you leave this None, it will take the id from the min of the current year.


## GUI

### setup environment

* Create a virtual environment 

```
python -m venv ./venv
```

* install required pacages

```
pip install -r requirements.txt
```

* lauch the server

```
python app.py
```

* connect to the url : `http://127.0.0.1:8050/`

You'll have 3 choices, to grab by `id` or `date` or `file`.


It's possible also to run automatically your scripts under your `OS`, or a cloud. For more details visit this page (lin)[https://towardsdatascience.com/how-to-automate-live-data-to-your-website-with-python-f22b76699674]
