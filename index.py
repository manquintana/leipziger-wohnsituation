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
def create_yearly_plot(dataframe, title, y_label, name):
    dataframe.plot(marker="o", figsize=(15,10), linestyle="--")
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(y_label)
    plt.grid(True)
    plt.savefig(f"generated_plots/{name}.png")
    print(f"Plot created into generated_plots > {name}.png")
    return True


# ################
# df_size (2010-2023 with missing years)
# ################

# 1. Analysis: Household size evolution per year
df_size_1 = df_size[(df_size["merkmal_1"] == "Haushalte") & (df_size["name"] != "Haushalte insgesamt")]
df_size_1 = df_size_1.rename(columns={"name": "Household size"})
df_size_1 = df_size_1.drop(columns = ["merkmal_1"])
df_size_1 = df_size_1.pivot(
    index="jahr",
    columns="Household size",
    values="wert"
)
df_size_1 = df_size_1.rename(columns={
    "eine Person": "1 person",
    "zwei Personen": "2 persons",
    "drei Personen": "3 persons",
    "vier Personen und mehr": "4+ persons"
})
df_size_1 = df_size_1[["1 person", "2 persons", "3 persons", "4+ persons"]]
create_yearly_plot(df_size_1, "Household size distribution over time", "Number of Households", "1.1 - Household size evolution over time")

# 2. Analysis: average household size evolution per year
df_size_2 = df_size[(df_size["name"] == "Durchschnittliche Haushaltsgröße")].drop(columns = ["merkmal_1"])
df_size_2["name"] = "Average Household size"
df_size_2 = df_size_2.rename(columns={"name": "Household size"})
df_size_2 = df_size_2.pivot(
    index="jahr",
    columns="Household size",
    values="wert"
)
create_yearly_plot(df_size_2, "Average household size distribution over time", "Number of Households", "1.2 - Average household size distribution over time")


# ################
# INITIAL ANALYSIS for df_type (2018-2023)
# ################
# 3. Analysis: Average rent % evolution per year
df_type_3 = df_type[~(df_type["name"] == "insgesamt")].drop(columns = ["merkmal_1", "einheit"])
df_type_3 = df_type_3.rename(columns={"wert": "Percentage of income", "name" : "Household Type"})
df_type_3 = df_type_3.pivot(
    index="jahr",
    columns="Household Type",
    values="Percentage of income"
)
df_type_3 = df_type_3[["Alleinstehende < 65 J. ", "Alleinstehende Rentner", "Paare ohne Kind", "Paare mit Kind(ern)", "Rentnerpaare"]]
create_yearly_plot(df_type_3, "Share of income by Household type spent on housing over time", "% of income", "2.1 - Share of income by Household type spent on housing over time")


# ################
# INITIAL ANALYSIS for df_situation (2000-2024)
# ################
# 4. Analysis: Average sqm per person
df_situation_4 = df_situation[df_situation["merkmal_1"] == "Durchschnittliche Wohnfläche pro Person"].drop(columns = ["merkmal_1", "einheit"])
df_situation_4 = df_situation_4[df_situation_4["name"].isin(["1-Personen-Haushalte", "2-Personen-Haushalte", "3-Personen-Haushalte", "4- und Mehr-Personen-Haushalte"])]
df_situation_4 = df_situation_4.rename(columns={"wert": "sqm", "name" : "Household Composition"})
df_situation_4 = df_situation_4.pivot(
    index="jahr",
    columns="Household Composition",
    values="sqm"
)
create_yearly_plot(df_situation_4, "Average sqm per person over time", "Household Composition", "3.1 - Average living space in sqm per person by household composition over time")

# 5. Analysis: Average room number per person

    
# 6. Analysis: Property regime



