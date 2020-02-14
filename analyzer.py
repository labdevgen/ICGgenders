import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shared import one_word_replacments
import math

def rename_professions(profession):
    profession = profession.lower()

    profession = profession.replace(" (со степенью кандидата наук)","")
    profession = profession.replace(" (со степенью доктора наук)","")
    for word in one_word_replacments.keys():
        if word in profession:
            profession = one_word_replacments[word]
            break

    return profession

def getGivenName(s):
    s = s.split()
    if len(s) >= 2:
        return s[1]
    else:
        return np.nan

data = pd.read_csv("ICG_data.csv")
data.drop(columns={"Фото","Unnamed: 0",'Телефон рабочий', 'Номер комнаты', 'e-mail',
       'Филиал'},inplace=True)
data.drop(labels=data.index[pd.isna(data["Должность"])],
          inplace=True)

# preprocess positions (professions) first words of profession
data["Profession"] = data["Должность"].astype("str").apply(rename_professions)

# Get given name from ФИО
data["Given_name"] = data["ФИО"].astype("str").apply(getGivenName)
data.drop(labels=data.index[pd.isna(data["Given_name"])],
          inplace=True)

# Read names and get gender
names = pd.read_csv("FakeNameGenerator.com_ad1a0e21/FakeNameGenerator.com_ad1a0e21.csv")
names = names.drop_duplicates()
print("Names in database: ",len(names))
data = data.merge(right=names,left_on="Given_name",right_on="GivenName",how="left",validate="many_to_one")
data = data.drop(labels = data.index[pd.isna(data["GivenName"])])
data = data.drop(columns={"Подразделение","Должность","GivenName"})
print("Total rows: ", len(data))

# check that names are correct
genders_count = data.groupby(["Gender"]).count()
print("With gender defined :", genders_count)
# for label in data.groupby(["Gender"]).groups:
#     print ("---->",label)
#     print (data.iloc[data.groupby(["Gender"]).groups[label],[0,-2]])
males = genders_count.loc["male","Given_name"]
females = genders_count.loc["female","Given_name"]
plt.pie(x=genders_count["Given_name"],labels=data.groupby(["Gender"]).groups)
plt.title("ICG employers:\nmale : female = "+str(males)+" : "+str(females)+" = 1 : "+str(round(females/males,2)))
plt.savefig("GendersTotal.png",dpi=600)
plt.clf()

# count of employers on different jobs
byJob = data.groupby("Profession")
counts = byJob.count().reset_index().sort_values(by="Given_name",ascending=False)

N = 30
total = counts["ФИО"].sum()
top_N = counts["ФИО"][:N].sum()
top_N_groups = counts["Profession"].values[:N]
print(top_N/total, " employers are within top ",N," most popular professions")

plt.gca().barh((np.arange(N))*2 + 1, counts["ФИО"][:N].values, align='center', height = 1.5)

for i in reversed(np.argsort(counts["Profession"][:N].values)):
    print (i)
    x_value = counts["ФИО"][:N].values[i] // 2
    x_color = "white"
    if x_value < 25:
        x_value = x_value*2 + 3
        x_color = "black"
    else:
        x_value = x_value - len(counts["Profession"].values[i])
    plt.text(x_value, i*2 + 1.6, counts["Profession"].values[i], fontsize=15, color=x_color)

plt.gca().invert_yaxis()
plt.gca().set_yticks([])
plt.gca().tick_params(axis='both', which='major', labelsize=20)

#plt.gca().set_yticklabels(counts["Profession"])
plt.tight_layout()
#plt.show()
#plt.savefig("Professtions.png",dpi=600)
plt.clf()

top_N_groups = ['младший научный сотрудник','научный сотрудник',
                'старший научный сотрудник','ведущий научный сотрудник',
                'главный научный сотрудник','заведующий лабораторией',
                'мед. брат/сестра','лаборант','аспирант','инженер','врач','агроном',
                'вахтер', 'водитель', 'уборщик','подсобный рабочий','монтер','сестра-хозяйка',
                'бухгалтер', 'программист', 'экономист', 'техник', 'администратор','заместитель директора'
   ]

# for each job compute male/female stats:
# plt_size_x = int(math.sqrt(len(top_N_groups)))
plt_size_x = 4
#plt_size_y = plt_size_x
plt_size_y = 6
if plt_size_x*plt_size_y < len(top_N_groups):
    plt_size_x += 1

fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

colors = {"male":"red","female":"blue"}

for ind,group in enumerate(top_N_groups):
    plt.subplot(plt_size_x,plt_size_y,ind+1)
    curr_group = byJob.get_group(group)
    if ind < 6:
        title = group.replace(" ","\n")
    else:
        title = group
    byGender = curr_group.groupby("Gender")
    counts = byGender.count()
    if "male" in byGender.groups:
        males = counts.loc["male", "Given_name"]
    else:
        males = 0

    if "female" in byGender.groups:
        females = counts.loc["female", "Given_name"]
    else:
        females = 0

    plt.pie(x=counts["Given_name"], labels=byGender.groups, shadow=False,
            textprops={"fontsize":0}, colors=[colors[i] for i in byGender.groups])
    if ind < 6:
        fs = 20
    else:
        fs = 14
    plt.title(title+"(" + str(males+females) + ")\n1 : " + \
              str(round(females / males, 2)),
              fontsize=fs)

plt.tight_layout()
#plt.show()
plt.savefig("GendersByProf.png",dpi=600)
plt.clf()
raise
# fun: most common name

# with open("ICG_common_names","w") as fout:
#     name_counts = data["Given_name"].value_counts(ascending=False)
#     fout.write(str(name_counts[:50]))

def process_degree(x):
    if x.startswith("к."):
        return ("PhD")
    elif x.startswith("д."):
        return ("Dr")
    else:
        return ("No degree")

data["degree"] = data['Учёная степень'].astype("str").apply(process_degree)
byDegree = data.groupby('degree')
counts = byDegree.count().reset_index().sort_values(by="ФИО",ascending=False)
print(counts)
N = len(counts)
top_N_groups = counts["degree"].values[:N]
plt.gca().barh(np.arange(N) + 1, counts["ФИО"][:N].values, align='center')
plt.gca().invert_yaxis()
plt.gca().set_yticks(np.arange(N) + 1)
plt.gca().set_yticklabels(counts["degree"])
plt.tight_layout()
plt.show()
plt.savefig("Degrees.png",dpi=600)
plt.clf()

fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

for ind,group in enumerate(top_N_groups):
    plt.subplot(plt_size_x,plt_size_y,ind+1)
    curr_group = byDegree.get_group(group)
    title = group
    byGender = curr_group.groupby("Gender")
    counts = byGender.count()
    if "male" in byGender.groups:
        males = counts.loc["male", "Given_name"]
    else:
        males = 0

    if "female" in byGender.groups:
        females = counts.loc["female", "Given_name"]
    else:
        females = 0

    plt.pie(x=counts["Given_name"], labels=byGender.groups, shadow=True,
            textprops={"fontsize":0}, colors=[colors[i] for i in byGender.groups])
    plt.title(title+"(" + str(males+females) + ")\n1 : " + \
              str(round(females / males, 2)),
              fontsize=10)

plt.tight_layout()
plt.savefig("byDegree",dpi=300)
plt.clf()