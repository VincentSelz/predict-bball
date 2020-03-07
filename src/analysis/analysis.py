"""Reads in data curates it and does first steps toward analyzing it."""
import numpy as np
import pandas as pd
from pregame import dropNaNs
from pregame import get_datasets
from pregame import order_dataset
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

from bld.project_paths import project_paths_join as ppj

# Read in Data
dataset = pd.read_excel(ppj("IN_DATA", "Seasons.xlsx"))
# dataset = pd.read_excel("../data/Seasons.xlsx")

# Last cleaning parts and slicing into four darasets
clean_data = dropNaNs(dataset)
clean_data = order_dataset(clean_data)
slim_data = clean_data.drop(clean_data.columns[[list(range(7))]], axis=1)
datasets = get_datasets(slim_data)

# Get algorithms
models = []
models.append(("LR", LogisticRegression(solver="liblinear", multi_class="ovr")))
models.append(("LDA", LinearDiscriminantAnalysis()))
models.append(("QDA", QuadraticDiscriminantAnalysis()))
models.append(("KNN", KNeighborsClassifier(n_neighbors=9, weights="distance")))
models.append(("DTC", DecisionTreeClassifier()))
models.append(("NB", GaussianNB()))
models.append(
    ("MLP", MLPClassifier(activation="logistic", solver="sgd", random_state=81))
)

results = {}
for key, dataset in datasets:
    array = dataset.values
    X = array[:, 1:]
    y = array[:, 0]
    y = y.astype("int")
    X_train, X_validation, Y_train, Y_validation = train_test_split(
        X, y, test_size=0.20, random_state=8
    )
    results[key] = []
    names = []
    for name, model in models:
        kfold = StratifiedKFold(n_splits=10, random_state=24, shuffle=True)
        cv_results = cross_val_score(
            model, X_train, Y_train, cv=kfold, scoring="accuracy"
        )
        results[key].append(cv_results.mean())
        names.append(name)

# Export matrix
result = pd.DataFrame.from_dict(results)
result.set_index([names], inplace=True)

# Export as Excel file and as tex file
result.to_excel(ppj("OUT_ANALYSIS", "datasetmatrix.xlsx"))
result.to_latex(ppj("OUT_TABLES", "datasetmatrix.tex"))


perc_diff = datasets[1]
perc_diff = perc_diff[1]
array = perc_diff.values
X = array[:, 1:]
y = array[:, 0]
y = y.astype("int")
X_train, X_validation, Y_train, Y_validation = train_test_split(
    X, y, test_size=0.20, random_state=8
)

# Use the best model
model = LogisticRegression(solver="liblinear", multi_class="ovr")
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)


# Get predictions
score = accuracy_score(Y_validation, predictions)
confusion = confusion_matrix(Y_validation, predictions)
confusion = pd.Dataframe(confusion)
report = classification_report(Y_validation, predictions, output_dict=True)
report = pd.DataFrame(report).transpose()
report.at["accuracy", "support"] = len(Y_validation)
for t in "precision", "recall":
    report.at["accuracy", t] = np.nan

# Export as Excel file and as tex file
score.to_latex(ppj("OUT_TABLES", "score.tex"))
confusion.to_excel(ppj("OUT_ANALYSIS", "confusion.xlsx"))
confusion.to_latex(ppj("OUT_TABLES", "confusion.tex"))
report.to_excel(ppj("OUT_ANALYSIS", "ClassificationReport.xlsx"))
report.to_latex(ppj("OUT_TABLES", "ClassificationReport.tex"))
