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
