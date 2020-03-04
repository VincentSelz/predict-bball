"""This script reads in data cleans/curates it and does first steps toward analyzing it."""
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# from pandas.plotting import scatter_matrix
# from matplotlib import pyplot
# from sklearn.svm import SVC
# from sklearn.utils.multiclass import type_of_target
# from sklearn import preprocessing
# from bld.project_paths import project_paths_join as ppj
# Works for Waf
# dataset = pd.read_excel((ppj("OUT_DATA","Seasons.xlsx")))
dataset = pd.read_excel("../data/Seasons.xlsx")
# # TODO: specifiy what can be dropped and what not
clean_data = dataset.dropna()
clean_data = clean_data[
    [
        "gameid",
        "Date",
        "Away Team",
        "PTS Away",
        "Home Team",
        "PTS Home",
        "Win Difference",
        "Home Win",
        "Games No Home Team",
        "Games No Away Team",
        "Home Wins",
        "Away Wins",
        "Home Losses",
        "Away Losses",
        "Home PTS Average",
        "Away PTS Average",
        "Home OPP PTS Average",
        "Away OPP PTS Average",
        "Home Win Percentage",
        "Away Win Percentage",
        "Home Point Differential",
        "Away Point Differential",
        "Home Days Off",
        "Away Days Off",
    ]
]

# Split-out validation dataset
array = clean_data.values

# How do I get wide format?
X = array[:, 18:24]
y = array[:, 7]
y = y.astype("int")
X_train, X_validation, Y_train, Y_validation = train_test_split(
    X, y, test_size=0.20, random_state=2
)

# Spot Check Algorithms
models = []
models.append(("LR", LogisticRegression(solver="liblinear", multi_class="ovr")))
models.append(("LDA", LinearDiscriminantAnalysis()))
models.append(("KNN", KNeighborsClassifier()))
models.append(("CART", DecisionTreeClassifier()))
models.append(("NB", GaussianNB()))
# models.append(('SVM', SVC(gamma='auto')))

# evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=2, shuffle=True)
    cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring="accuracy")
    results.append(cv_results)
    names.append(name)
    print("{}: {:f} ({:f})".format(name, cv_results.mean(), cv_results.std()))

model = LinearDiscriminantAnalysis()
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)

# Evaluate predictions
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
