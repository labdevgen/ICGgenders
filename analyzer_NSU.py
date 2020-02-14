import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shared import one_word_replacments
import math

data = pd.read_csv("NSU_abitura.txt",sep=" ",header=None)
data.rename(columns={0:"LastName",1:"Given_name",2:"MiddleName"}, inplace=True)
print(data.head())

# Read names and get gender
names = pd.read_csv("FakeNameGenerator.com_ad1a0e21/FakeNameGenerator.com_ad1a0e21.csv")
names = names.drop_duplicates()
print("Names in database: ",len(names))
data = data.merge(right=names,left_on="Given_name",right_on="GivenName",how="left",validate="many_to_one")
data = data.drop(columns={"GivenName"})
print("Total rows: ", len(data))

genders_count = data.groupby(["Gender"]).count()
print("With gender defined :", genders_count)
# for label in data.groupby(["Gender"]).groups:
#     print ("---->",label)
#     print (data.iloc[data.groupby(["Gender"]).groups[label],[0,-2]])
males = genders_count.loc["male","Given_name"]
females = genders_count.loc["female","Given_name"]
plt.pie(x=genders_count["Given_name"],labels=data.groupby(["Gender"]).groups)
plt.title("NSU Dep. of LS students:\nmale : female = "+str(males)+" : "+str(females)+" = 1 : "+str(round(females/males,2)))
plt.savefig("GendersTotalNsu.png",dpi=600)
plt.clf()