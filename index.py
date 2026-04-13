#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:39:03 2026

@author: mqu
"""

import pandas as pd
import re
import json
import matplotlib.pyplot as plt

# ############
# DATA LOADING
# ############
""" Loads clean json into a pandas df
    removing the comments in the dataset """
def load_json(filename):
    with open(f"datasets/{filename}", "r", encoding="utf-8") as f:
        text = f.read()
    clean_text = re.sub(r"^//.*\n", "", text, flags=re.MULTILINE)
    parsed_data = json.loads(clean_text)
    return pd.DataFrame(parsed_data)

df_size = load_json("haushaltsgruesse.json")
df_type = load_json("haushaltstyp.json")
df_situation = load_json("wohnsituation.json")


# ##############
# DATA CLEANSING
# ##############
df_size = df_size.drop(columns = ["merkmal_2", "merkmal_3", "merkmal_4", "periode", "kategorie_Nr", "rubrik_Nr", "jahr_Nr", "uri", "id", "einheit", "kategorie", "rubrik"])
df_size["wert"] = pd.to_numeric(df_size["wert"], errors="coerce")
df_size["jahr"] = pd.to_numeric(df_size["jahr"], errors="coerce")
df_size.loc[(df_size["name"] == "Haushalte") & (df_size["merkmal_1"] == "Haushalte"),"name"] = "Haushalte insgesamt"

df_situation = df_situation.drop(columns = ["merkmal_2", "merkmal_3", "merkmal_4", "periode", "kategorie_Nr", "rubrik_Nr", "jahr_Nr", "uri", "id", "kategorie", "rubrik"])
df_situation["einheit"] = df_situation["einheit"].replace("m&sup2;", "sqm")
df_situation["wert"] = pd.to_numeric(df_situation["wert"], errors="coerce")
df_situation["jahr"] = pd.to_numeric(df_situation["jahr"], errors="coerce")

df_type = df_type.drop(columns = ["merkmal_2", "merkmal_3", "merkmal_4", "periode", "kategorie_Nr", "rubrik_Nr", "jahr_Nr", "uri", "id", "kategorie", "rubrik"])
df_type["wert"] = pd.to_numeric(df_type["wert"], errors="coerce")
df_type["jahr"] = pd.to_numeric(df_type["jahr"], errors="coerce")
df_type = df_type[~(df_type["name"] == "Alleinerziehende ")]


# ##############
# SAVE PLOTS
# ##############
def save_plot(plt, name):
    print(f"Plot created into generated_plots > {name}.png")
    plt.savefig(f"generated_plots/{name}.png")
    return True


# ################
# df_size (2010-2023 with missing years)
# ################

# 1. Analysis: Household size evolution per year
df_household_size = df_size[(df_size["merkmal_1"] == "Haushalte") & (df_size["name"] != "Haushalte insgesamt")]
df_household_size = df_household_size.rename(columns={"name": "Household size"})
df_household_size = df_household_size.drop(columns = ["merkmal_1"])
df_household_size = df_household_size.pivot(
    index="jahr",
    columns="Household size",
    values="wert"
)
df_household_size = df_household_size.rename(columns={
    "eine Person": "1 person",
    "zwei Personen": "2 persons",
    "drei Personen": "3 persons",
    "vier Personen und mehr": "4+ persons"
})
df_household_size = df_household_size[["1 person", "2 persons", "3 persons", "4+ persons"]]
# plot
df_household_size.plot(marker="o", figsize=(15,10), linestyle="--")
plt.title("Household size distribution over time")
plt.xlabel("Year")
plt.ylabel("Number of Households")
plt.grid(True)
#plt.show()
save_plot(plt, "1.1 - Household size evolution over time")

# 2. Analysis: average household size evolution per year
df_household_average = df_size[(df_size["name"] == "Durchschnittliche Haushaltsgröße")].drop(columns = ["merkmal_1"])
df_household_average["name"] = "Average Household size"
df_household_average = df_household_average.rename(columns={"name": "Household size"})
df_household_average = df_household_average.pivot(
    index="jahr",
    columns="Household size",
    values="wert"
)
# plot
df_household_average.plot(marker="o", figsize=(15,10), linestyle="--")
plt.title("Household Size Distribution Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Households")
plt.grid(True)
#plt.show()
save_plot(plt, "1.2 - Average household size distribution over time")


# ################
# INITIAL ANALYSIS for df_type (2018-2023)
# ################
# 3. Analysis: Average rent % evolution per year
df_rent_perc = df_type[~(df_type["name"] == "insgesamt")].drop(columns = ["merkmal_1", "einheit"])
df_rent_perc = df_rent_perc.rename(columns={"wert": "Percentage of income", "name" : "Household Type"})
df_rent_perc = df_rent_perc.pivot(
    index="jahr",
    columns="Household Type",
    values="Percentage of income"
)
df_rent_perc = df_rent_perc[["Alleinstehende < 65 J. ", "Alleinstehende Rentner", "Paare ohne Kind", "Paare mit Kind(ern)", "Rentnerpaare"]]
df_rent_perc.plot(marker="o", figsize=(15,10), linestyle="--")
plt.title("Share of income by Household type spent on housing over time")
plt.xlabel("Year")
plt.ylabel("% of net income")
plt.grid(True)
#plt.show()
save_plot(plt, "2.1 - Share of income by Household type spent on housing over time")


# ################
# INITIAL ANALYSIS for df_situation (2000-2024)
# ################


