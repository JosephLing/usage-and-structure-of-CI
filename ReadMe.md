# Usage and Structure of continuous integration as configuration?

This repo is the corpus for the dissertation. Please note that some of the code is a bit messy although I did try to keep it reasonably clean while working on it. 


# paper
Is in `./report/` and all the plots are stored in `./src/results/` and that is where they will be generated each time `render_main.py` is run.

Most of the tables of data are automatically generated although there is one manual one which is stored in the report dir.


## data

The corpus of intial data won't fit on github file restrictions so I will link to a google drive download soon. The result of running that data through the data parser script does fit so that is currently zipped in `./src/`.

The comparison dataset is `./src/breadth_corpus.csv` which was provided by Michael Hilton. The comparison is against *Usage, costs, and benefits of continuous integration in open-source projects* (http://cope.eecs.oregonstate.edu/CISurvey/).

# run
First create the virtual python enviroment 

then inside the virtual enviroment run: `pip install -r requirements.txt`

## scraping
Create .env file with token inside named GITHUB_TOKEN

`config.py` stores the configuration of what files are searched for when scraping

`python scraper.py` to create the data 


## processing data
Run `python main.py` with the `.env` setup to CHECK and then RENDER to create all the things

Or you can run `checker.py` (combines all the csv files into and removes duplicates) and then `data_parser.py` (creates a csv of all the projects that have CI and parses the CI configuration for various pieces of data) manually if you want not use `main.py`.


## rendering

`render_main.py` will generate the plots for the paper although they are currently already stored in `./src/results/`

## testing
There are a few unit tests for the `data_parser.py` script in particular and they can be run with the default python unit test way: `python -m unittest`.


