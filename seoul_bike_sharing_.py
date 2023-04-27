# -*- coding: utf-8 -*-
"""Seoul-Bike-Sharing_.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qxpi7YPknsHcwsGAq9BPGi54FLZ6-0ze
"""

# Importing Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
import os

import warnings
warnings.filterwarnings('ignore')

"""Loding DataSet from CSV to DataFrame"""

# os.getcwd()

# importing the csv into DataFrame using Pandas
df = pd.read_csv("Group_19_data_cleaned.csv",encoding= 'unicode_escape',parse_dates=[0])
df.head(2)

#info of the dataset
df.info()

# new_df = df

# fig,axes = plt.subplots(1,3,figsize=(20,5))
# # here we use log10 
# sns.distplot(np.log10(new_df['Rented Bike Count']+0.0000001),ax=axes[0],color='red').set_title("log 10")
# # here we use square 
# sns.distplot((new_df['Rented Bike Count']**2),ax=axes[1],color='red').set_title("square")
# # here we use square root 
# sns.distplot(np.sqrt(new_df['Rented Bike Count']),ax=axes[2], color='green').set_title("Square root")

df=df.astype({'Rented Bike Count':'float','Hour':'object','Date':'datetime64','Holiday':'object','Functioning Day':'object'})

df=df.rename(columns={'Temperature(°C)':'Temperature','Humidity(%)':'Humidity','Rainfall(mm)':'Rainfall','Snowfall (cm)':'Snowfall','Wind speed (m/s)':'Wind speed','Visibility (10m)':'Visibility','Solar Radiation (MJ/m2)':'Radiation','Dew point temperature(°C)':'Dew point temperature'})

df.describe().style.background_gradient()

df=pd.get_dummies(df,columns=['Holiday','Seasons','Functioning Day','Hour'],drop_first=True)

X=df.iloc[:,3:]
y=df.iloc[:,2]

y

"""Splitting our dataset into train and test set """

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.30,random_state=0)

from sklearn.preprocessing import StandardScaler

sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.transform(X_test)

model_comparison = {}

"""**Random Forest Regression**"""

from sklearn.ensemble import RandomForestRegressor

n_estimators = [5,20,50,100] # number of trees in the random forest
max_features = ['auto', 'sqrt'] # number of features in consideration at every split
max_depth = [int(x) for x in np.linspace(10, 120, num = 12)] # maximum number of levels allowed in each decision tree
min_samples_split = [2, 6, 10] # minimum sample number to split a node
min_samples_leaf = [1, 3, 4] # minimum sample number that can be stored in a leaf node
bootstrap = [True, False] # method used to sample data points

random_grid = {'n_estimators': n_estimators,

'max_features': max_features,

'max_depth': max_depth,

'min_samples_split': min_samples_split,

'min_samples_leaf': min_samples_leaf,

'bootstrap': bootstrap}

## Importing Random Forest Classifier from the sklearn.ensemble
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

from sklearn.model_selection import RandomizedSearchCV
rf_random = RandomizedSearchCV(estimator = rf,param_distributions = random_grid,
               n_iter = 100, cv = 5, verbose=2, random_state=35, n_jobs = -1)

rf_random.fit(X_train, y_train)

print ('Random grid: ', random_grid, '\n')
# print the best parameters
print ('Best Parameters: ', rf_random.best_params_, ' \n')

randmf = RandomForestRegressor(n_estimators = 100, min_samples_split = 10, min_samples_leaf= 1, max_features = 'auto', max_depth= 110, bootstrap=True) 
randmf.fit( X_train, y_train)

y_pred=randmf.predict(X_test)

print(f"Model R-Square : {r2_score(y_test,y_pred)*100:.2f}%")
print(f"Model MSE : {mean_squared_error(y_test,y_pred)*100:.2f}%")
accuracies = cross_val_score(estimator = randmf, X = X_train, y = y_train, cv = 5)
print("Cross Val Accuracy: {:.2f} %".format(accuracies.mean()*100))
print("Cross Val Standard Deviation: {:.2f} %".format(accuracies.std()*100))
model_comparison['Random forest Regression']=[r2_score(y_test,y_pred),mean_squared_error(y_test,y_pred),(accuracies.mean()),(accuracies.std())]

plt.figure(figsize=(17,7))
plt.plot((y_pred)[:80])
plt.plot((np.array(y_test)[:80]))
plt.legend(["Predicted","Actual"])
plt.title("Random Forest")
plt.show()



"""**Linear Regression**"""

from sklearn.linear_model import LinearRegression
model= LinearRegression()
model.fit(X_train, y_train)
y_pred=model.predict(X_test)
print(f"Model R-Square : {r2_score(y_test,y_pred)*100:.2f}%")
print(f"Model MSE : {mean_squared_error(y_test,y_pred)*100:.2f}%")
accuracies = cross_val_score(estimator = model, X = X_train, y = y_train, cv = 5)
print("Cross Val Accuracy: {:.2f} %".format(accuracies.mean()*100))
print("Cross Val Standard Deviation: {:.2f} %".format(accuracies.std()*100))
model_comparison['LinearRegression']=[r2_score(y_test,y_pred),mean_squared_error(y_test,y_pred),(accuracies.mean()),(accuracies.std())]

y_pred

plt.figure(figsize=(17,7))
plt.plot((y_pred)[:80])
plt.plot((np.array(y_test)[:80]))
plt.legend(["Predicted","Actual"])
plt.title("Linear Regressor")
plt.show()

"""**DECISION TREE**"""

parameters={"splitter":["best","random"],
            "criterion": ["squared_error"],
            "max_depth" : [1,3,5,7,9,10],
            "min_samples_leaf":[1],
            "min_samples_split": [2],
           "min_weight_fraction_leaf":[0.0],
           "max_features":["auto","log2","sqrt",None],
           "max_leaf_nodes":[None,10,20,30,40,50,60,70,80,90] }

grid=GridSearchCV(DecisionTreeRegressor(),param_grid=parameters,n_jobs=-1,cv=3,verbose=200)
grid.fit(X_train,y_train)

grid.best_params_

grid.best_score_

model=DecisionTreeRegressor(max_depth=10,max_features='auto',min_samples_leaf=1,max_leaf_nodes=90,min_samples_split=2,min_weight_fraction_leaf=0.0,splitter='best',criterion= 'squared_error',)
model.fit(X_train,y_train)

y_pred = model.predict(X_test)

print(f"Model R-Square : {r2_score(y_test,y_pred)*100:.2f}%")
print(f"Model MSE : {mean_squared_error(y_test,y_pred)*100:.2f}%")
accuracies = cross_val_score(estimator = model, X = X_train, y = y_train, cv = 5)
print("Cross Val Accuracy: {:.2f} %".format(accuracies.mean()*100))
print("Cross Val Standard Deviation: {:.2f} %".format(accuracies.std()*100))
model_comparison['Decision Tree Regression']=[r2_score(y_test,y_pred),mean_squared_error(y_test,y_pred),(accuracies.mean()),(accuracies.std())]

plt.figure(figsize=(17,7))
plt.plot((y_pred)[:80])
plt.plot((np.array(y_test)[:80]))
plt.legend(["Predicted","Actual"])
plt.title("Decision Tree")
plt.show()

"""**KNN**"""



from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.2,random_state =2)

from sklearn.preprocessing import StandardScaler

std = StandardScaler()
std_train = std.fit_transform(X_train)
std_test = std.transform(X_test)

from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix

X_train.shape,y_train.shape,X_test.shape

df.isnull().sum()

regressor = KNeighborsRegressor(n_neighbors=10)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
regressor.score(X_test, y_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)

error = []

# Calculating MAE error for K values between 1 and 39
for i in range(1, 40):
    knn = KNeighborsRegressor(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    mae = mean_absolute_error(y_test, pred_i)
    error.append(mae)

import matplotlib.pyplot as plt 

plt.figure(figsize=(12, 6))
plt.plot(range(1, 40), error, color='red', 
         linestyle='dashed', marker='o',
         markerfacecolor='blue', markersize=10)
         
plt.title('K Value MAE')
plt.xlabel('K Value')
plt.ylabel('Mean Absolute Error')

accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train, cv = 5)
print("Cross Val Accuracy: {:.2f} %".format(accuracies.mean()*100))
print("Cross Val Standard Deviation: {:.2f} %".format(accuracies.std()*100))
model_comparison['K-Nearest Neighbor']=[r2_score(y_test,y_pred),mean_squared_error(y_test,y_pred),(accuracies.mean()),(accuracies.std())]

plt.figure(figsize=(17,7))
plt.plot((pred_i)[:80])
plt.plot((np.array(y_test)[:80]))
plt.legend(["Predicted","Actual"])
plt.title("KNN")
plt.show()

"""### Model Comparison"""

Model_com_df=pd.DataFrame(model_comparison).T
Model_com_df.columns=['R-Square','MSE','CV Accuracy','CV std']
Model_com_df=Model_com_df.sort_values(by='R-Square',ascending=False)
Model_com_df.style.format("{:.2%}").background_gradient(cmap='RdYlBu_r')