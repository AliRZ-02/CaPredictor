# Name: Ali Raza Zaidi
# Date: January 2, 2021
# Program: modeler.py
# Purpose: Create Models for future Contracts based on current player data

# Import Statements ---------------------------------------------------------------------------
import pandas
import joblib
from sklearn import linear_model
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from scipy.stats import linregress

# Gathering Data ------------------------------------------------------------------------------
center_o27 = pandas.read_csv("..\Data\Clean\Centers-O27.csv")
center_u27_long = pandas.read_csv("..\Data\Clean\Centers-U27-Long.csv")
center_u27_short = pandas.read_csv("..\Data\Clean\Centers-U27-Short.csv")
defence_o27 = pandas.read_csv("..\Data\Clean\Defence-O27.csv")
defence_u27_short = pandas.read_csv("..\Data\Clean\Defence-U27-Short.csv")
defence_u27_long = pandas.read_csv("..\Data\Clean\Defence-U27-Long.csv")
goalies = pandas.read_csv("..\Data\Clean\Goalies.csv")
lw_o27 = pandas.read_csv("..\Data\Clean\LeftWings-O27.csv")
lw_u27_long = pandas.read_csv("..\Data\Clean\LeftWings-U27-Long.csv")
lw_u27_short = pandas.read_csv("..\Data\Clean\LeftWings-U27-Short.csv")
rw_o27 = pandas.read_csv("..\Data\Clean\RightWings-O27.csv")
rw_u27_long = pandas.read_csv("..\Data\Clean\RightWings-U27-Long.csv")
rw_u27_short = pandas.read_csv("..\Data\Clean\RightWings-U27-Short.csv")

# Data Splitting & Model Creation --------------------------------------------------------------

# UFA Centers
c_o27_in = center_o27[["Contract Length", "Age", "G/82", "A/82", "P/82", "P/GP"]]
c_o27_out = center_o27["Cap %"]

c_o27_reg = linear_model.LinearRegression()
c_o27_reg.fit(c_o27_in, c_o27_out)

# Non-Bridge RFA Centers
c_u27_long_in = center_u27_long[
    ["Contract Length", "Age", "G/82", "A/82", "P/82", "P/GP"]
]
c_u27_long_out = center_u27_long["Cap %"]

c_u27_long_reg = linear_model.LinearRegression()
c_u27_long_reg.fit(c_u27_long_in, c_u27_long_out)

# Bridge RFA Centers
c_u27_short_in = center_u27_short[
    ["Contract Length", "Age", "G/82", "A/82", "P/82", "P/GP"]
]
c_u27_short_out = center_u27_short["Cap %"]

c_u27_short_reg = linear_model.LinearRegression()
c_u27_short_reg.fit(c_u27_short_in, c_u27_short_out)

# UFA Defenceman
d_o27_in = defence_o27[
    [
        "Contract Length",
        "Age",
        "G/82",
        "A/82",
        "P/82",
        "P/GP",
        "Blocks/82",
        "Hits/82",
        "GP",
        "TOI/G",
        "S%",
    ]
]
d_o27_out = defence_o27["Cap %"]

d_o27_reg = linear_model.LinearRegression()
d_o27_reg.fit(d_o27_in, d_o27_out)

# Non-Bridge RFA Defenceman
d_u27_long_in = defence_u27_long[
    [
        "Contract Length",
        "Age",
        "G/82",
        "A/82",
        "P/82",
        "P/GP",
        "Blocks/82",
        "Hits/82",
        "GP",
        "TOI/G",
        "S%",
    ]
]
d_u27_long_out = defence_u27_long["Cap %"]

d_u27_long_reg = linear_model.LinearRegression()
d_u27_long_reg.fit(d_u27_long_in, d_u27_long_out)

# Bridge RFA Defenceman
d_u27_short_in = defence_u27_short[
    [
        "Contract Length",
        "Age",
        "G/82",
        "A/82",
        "P/82",
        "P/GP",
        "Blocks/82",
        "Hits/82",
        "GP",
        "TOI/G",
        "S%",
    ]
]
d_u27_short_out = defence_u27_short["Cap %"]

d_u27_short_reg = linear_model.LinearRegression()
d_u27_short_reg.fit(d_u27_short_in, d_u27_short_out)

# UFA Left-Wingers
lw_o27_in = lw_o27[["Contract Length", "Age", "G/82", "A/82", "P/82", "P/GP"]]
lw_o27_out = lw_o27["Cap %"]

lw_o27_reg = linear_model.LinearRegression()
lw_o27_reg.fit(lw_o27_in, lw_o27_out)

# Non-Bridge RFA LW
lw_u27_long_in = lw_u27_long[["Contract Length", "Age", "G/82", "A/82", "P/82", "P/GP"]]
lw_u27_long_out = lw_u27_long["Cap %"]

lw_u27_long_reg = linear_model.LinearRegression()
lw_u27_long_reg.fit(lw_u27_long_in, lw_u27_long_out)

# Bridge RFA LW
lw_u27_short_in = lw_u27_short[
    ["Contract Length", "Age", "G/82", "A/82", "P/82", "P/GP"]
]
lw_u27_short_out = lw_u27_short["Cap %"]

lw_u27_short_reg = linear_model.LinearRegression()
lw_u27_short_reg.fit(lw_u27_short_in, lw_u27_short_out)

# UFA RW
rw_o27_in = rw_o27[["Contract Length", "Age", "G/82", "A/82", "P/82", "P/GP"]]
rw_o27_out = rw_o27["Cap %"]

rw_o27_reg = linear_model.LinearRegression()
rw_o27_reg.fit(rw_o27_in, rw_o27_out)

# Non-Bridge RFA RW
rw_u27_long_in = rw_u27_long[["Contract Length", "Age", "G/82", "A/82", "P/82", "P/GP"]]
rw_u27_long_out = rw_u27_long["Cap %"]

rw_u27_long_reg = linear_model.LinearRegression()
rw_u27_long_reg.fit(rw_u27_long_in, rw_u27_long_out)

# Bridge RFA RW
rw_u27_short_in = rw_u27_short[
    ["Contract Length", "Age", "G/82", "A/82", "P/82", "P/GP"]
]
rw_u27_short_out = rw_u27_short["Cap %"]

rw_u27_short_reg = linear_model.LinearRegression()
rw_u27_short_reg.fit(rw_u27_short_in, rw_u27_short_out)

# Goalies
goalies_in = goalies[["Contract Length", "Games", "GAA", "SV%", "Win %"]]
goalies_out = goalies["Cap %"]

g_reg = linear_model.LinearRegression()
g_reg.fit(goalies_in, goalies_out)

# Model Dumping
joblib.dump(c_o27_reg, "..\Models\C-O27-Model.joblib")
joblib.dump(c_u27_long_reg, "..\Models\C-U27-L-Model.joblib")
joblib.dump(c_u27_short_reg, "..\Models\C-U27-S-Model.joblib")
joblib.dump(d_o27_reg, "..\Models\D-O27-Model.joblib")
joblib.dump(d_u27_long_reg, "..\Models\D-U27-L-Model.joblib")
joblib.dump(d_u27_short_reg, "..\Models\D-U27-S-Model.joblib")
joblib.dump(lw_o27_reg, "..\Models\L-O27-Model.joblib")
joblib.dump(lw_u27_long_reg, "..\Models\L-U27-L-Model.joblib")
joblib.dump(lw_u27_short_reg, "..\Models\L-U27-S-Model.joblib")
joblib.dump(rw_o27_reg, "..\Models\R-O27-Model.joblib")
joblib.dump(rw_u27_long_reg, "..\Models\R-U27-L-Model.joblib")
joblib.dump(rw_u27_short_reg, "..\Models\R-U27-S-Model.joblib")
joblib.dump(g_reg, "..\Models\G-Model.joblib")