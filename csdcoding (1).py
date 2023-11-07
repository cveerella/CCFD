# -*- coding: utf-8 -*-
"""CSDCoding.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18IJjgG4dYEbIyNuHi_Q-Faudp3mRtVV5
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec

data = pd.read_csv("creditcard.csv")

data.head()

print(data.shape)
print(data.describe())

fraud = data[data['Class'] == 1]
valid = data[data['Class'] == 0]
outlierFraction = len(fraud)/float(len(valid))
print(outlierFraction)
print('Fraud Cases: {}'.format(len(data[data['Class'] == 1])))
print('Valid Transactions: {}'.format(len(data[data['Class'] == 0])))

print("Amount details of the fraudulent transaction")
fraud.Amount.describe()

print("details of valid transaction")
valid.Amount.describe()

corrmat = data.corr()
fig = plt.figure(figsize = (12, 9))
sns.heatmap(corrmat, vmax = .8, square = True)
plt.show()

X = data.drop(['Class'], axis = 1)
Y = data["Class"]
print(X.shape)
print(Y.shape)
xData = X.values
yData = Y.values

from sklearn.model_selection import train_test_split
xTrain, xTest, yTrain, yTest = train_test_split(
        xData, yData, test_size = 0.2, random_state = 42)

from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier()
rfc.fit(xTrain, yTrain)
yPred = rfc.predict(xTest)

from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, matthews_corrcoef
from sklearn.metrics import confusion_matrix

n_outliers = len(fraud)
n_errors = (yPred != yTest).sum()
print("The model used is Random Forest classifier")

acc = accuracy_score(yTest, yPred)
print("The accuracy is {}".format(acc))
RanAcc=acc
prec = precision_score(yTest, yPred)
print("The precision is {}".format(prec))
RanPre=prec
rec = recall_score(yTest, yPred)
print("The recall is {}".format(rec))
RanRec=rec
f1 = f1_score(yTest, yPred)
print("The F1-Score is {}".format(f1))
RanF1=f1
MCC = matthews_corrcoef(yTest, yPred)
print("The Matthews correlation coefficient is{}".format(MCC))

from sklearn.metrics import confusion_matrix
LABELS = ['Normal', 'Fraud']
conf_matrix = confusion_matrix(yTest, yPred)
plt.figure(figsize =(12, 12))
sns.heatmap(conf_matrix, xticklabels = LABELS,
            yticklabels = LABELS, annot = True, fmt ="d");
plt.title("Confusion matrix")
plt.ylabel('True class')
plt.xlabel('Predicted class')
plt.show()

from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(random_state = 0,
                                    criterion = 'gini',  splitter='best', min_samples_leaf=1, min_samples_split=2)
classifier.fit(xTrain, yTrain)


from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, matthews_corrcoef
# Predicting Test Set
y_pred = classifier.predict(xTest)
acc = accuracy_score(yTest, y_pred)
DecAcc=acc
prec = precision_score(yTest, y_pred)
Decpre=prec
rec = recall_score(yTest, y_pred)
DecRec=rec
f1 = f1_score(yTest, y_pred)
DecF1=f1
MCC=matthews_corrcoef(yTest,y_pred)

results = pd.DataFrame([['Decision tree', acc, prec, rec, f1,MCC]],
               columns = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score','matthews_corrcoef'])
print(results)

import pandas as pd
import numpy as np
!pip install catboost
from catboost import Pool, CatBoostClassifier, cv, CatBoostRegressor
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_score, recall_score,f1_score,classification_report
import seaborn as sns
from imblearn.over_sampling import SMOTE

dataset=pd.read_csv('/content/creditcard.csv')
dataset['Class'].value_counts().plot(kind='bar',figsize=[10,5])
dataset['Class'].value_counts()

dataset = dataset.drop(['Time', 'Amount'], axis=1)
dataset.head()

label=dataset['Class']
Data=dataset.drop(["Class"],axis=1)

print("Data Types\n{}".format(Data.dtypes))

null_counts = Data.isnull().sum()
print("Number of null values in each feature:\n{}".format(null_counts))

x_train,x_test,y_train,y_test = train_test_split(Data,label,test_size=0.33,random_state=1236)

print("Label 1, Before using SMOTE: {} ".format(sum(y_train==1)))
print("Label 0, Before using SMOTE: {} ".format(sum(y_train==0)))

from imblearn.over_sampling import SMOTE

# Create a SMOTE object
smote = SMOTE(random_state=12)

# Use fit_resample method to oversample your data
x_train_OS, y_train_OS = smote.fit_resample(x_train, y_train)

print("Label 1, After using SMOTE: {}".format(sum(y_train_OS==1)))
print("Label 0, After using SMOTE: {}".format(sum(y_train_OS==0)))

model = CatBoostClassifier(iterations=100,
                             depth=12,
                             eval_metric='AUC',
                             random_seed = 2018,
                             od_type='Iter',
                             metric_period = 1,
                             od_wait=100)

model.fit(x_train_OS,y_train_OS)

predict = model.predict(x_test)

cm = pd.crosstab(y_test, predict, rownames=['Actual'], colnames=['Predicted'])
fig, (ax1) = plt.subplots(ncols=1, figsize=(5,5))

sns.heatmap(pd.DataFrame(cm), annot=True, cmap="Blues" ,fmt='g',
            xticklabels=['Not Fraud', 'Fraud'],
            yticklabels=['Not Fraud', 'Fraud'],)
ax1.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion Matrix', y=1.1,fontsize=14)
plt.show()

acc=accuracy_score(y_test,predict)
print('Accuracy =' ,acc)
CatAcc=acc

precision = precision_score(y_test, predict)
print('Precision =' ,precision)
CatPre=precision

recall = recall_score(y_test, predict)
print("Recall : ",recall )
CatRec=recall

f1score = f1_score(y_test,predict, average='macro')
print("F1 Score : ",f1score )
CatF1=f1score

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import numpy as np
import xgboost as xgb

import warnings
warnings.filterwarnings('ignore')

# %matplotlib inline

df = pd.read_csv("/content/creditcard.csv")

print('Total de linhas e colunas\n\n',df.shape, '\n')

df.isnull().sum()

df.info()

df.describe().round()

print ('Non Fraud % ',round(df['Class'].value_counts()[0]/len(df)*100,2))
print ()
print (round(df.Amount[df.Class == 0].describe(),2))
print ()
print ()
print ('Fraud %    ',round(df['Class'].value_counts()[1]/len(df)*100,2))
print ()
print (round(df.Amount[df.Class == 1].describe(),2))

plt.figure(figsize=(10,8))
sns.set_style('darkgrid')
sns.barplot(x=df['Class'].value_counts().index,y=df['Class'].value_counts(), palette=["C1", "C8"])
plt.title('Non Fraud X Fraud')
plt.ylabel('Count')
plt.xlabel('0:Non Fraud, 1:Fraud')
print ('Non Fraud % ',round(df['Class'].value_counts()[0]/len(df)*100,2))
print ('Fraud %    ',round(df['Class'].value_counts()[1]/len(df)*100,2));

feature_names = df.iloc[:, 1:30].columns
target = df.iloc[:1, 30:].columns


data_features = df[feature_names]
data_target = df[target]

feature_names

target

from sklearn.model_selection import train_test_split
np.random.seed(123)
X_train, X_test, y_train, y_test = train_test_split(data_features, data_target, train_size = 0.70, test_size = 0.30, random_state = 1)

xg = xgb.XGBClassifier()

xg.fit(X_train, y_train)

def PrintStats(cmat, y_test, pred):
    tpos = cmat[0][0]
    fneg = cmat[1][1]
    fpos = cmat[0][1]
    tneg = cmat[1][0]

def RunModel(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train.values.ravel())
    pred = model.predict(X_test)
    matrix = confusion_matrix(y_test, pred)
    return matrix, pred

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score, roc_curve

cmat, pred = RunModel(xg, X_train, y_train, X_test, y_test)

!pip search scikit-plot
!pip install scikit-plot
!pip install --upgrade pip

import scikitplot as skplt
skplt.metrics.plot_confusion_matrix(y_test, pred)

from sklearn.metrics import accuracy_score
a=accuracy_score(y_test, pred)
XgbAcc=a

from sklearn.metrics import precision_score,recall_score,f1_score
p=precision_score(y_test, pred)
r=recall_score(y_test, pred)
f1=f1_score(y_test, pred)

print (classification_report(y_test, pred))

from sklearn.metrics import f1_score
f1score=f1_score(y_test,pred,average='macro')
print("F1 Score :",f1score)

import pandas as pd
data={"Algorithm":["Random forest","Decision Tree","CATBoost","XGBoost"],
      "Accuracy":["0.9995962220427653","0.99907","0.9989041037590305","0.97"],
      "Precision":["0.9746835443037974","0.699115","0.6157635467980296","0.95"],
      "F1":["0.8700564971751412","0.748815","0.8538331591957888","0.85"],
      "Recall":["0.7857142857142857","0.806122","0.8333333333333334","0.78"]}
df=pd.DataFrame(data)
print(df)