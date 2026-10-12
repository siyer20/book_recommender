Initial Data Wrangling!

The purpose of this folder and its contents is to get a basic structure for the recommender working to later improve upon and add features to.

I'm using the jupyter notebook format to create easy to understand code so that if I take a break from this project and come back later, I can easily pick up where I left off.
Additionally, these notebooks are organized in such a way so that if I ever need to teach someone else these topics, I can use these as references.

Stages:
1. data exploration
2. data cleaning
3. data preparation for feature engineering
4. build rudimentary recommender
5. test, evaluate, improve

Organization:

book-recommender/
├── data/
│   ├── books.csv
│   └── processed/
│       ├── books_clean.csv
│       ├── book_genre_features.csv
│       ├── book_description_features.npz
│       └── book_combined_features.npz
├── notebooks/
│   ├── 01_explore_books.ipynb
│   ├── 02_clean_books.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_build_recommender.ipynb
└── requirements.txt
