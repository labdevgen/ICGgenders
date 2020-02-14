from bs4 import BeautifulSoup
import pandas as pd

soup = BeautifulSoup(open("phonebook.html"), 'html.parser')
table = pd.read_html(str(soup.table))[0]
table.to_csv("ICG_data.csv")