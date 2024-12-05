import sys
import numpy as np
#cvopt for solving optimization problems
from cvxopt import solvers
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


#reading a dataset

df = pd.read_csv('./pulsar_star_dataset.csv')
df.head()

#splitting the dataset into features and labels
X = df.drop('target_class', axis=1)
y = df['target_class'] 

#converting dataset into numby array for easy use
X = np.array(X)
y = np.array(y)

#converting labels into -1 and 1 as per SVm formulation
y[y==0] = -1

#splitting the dataset to train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#standardizing dataset
mean = np.mean(X_train, axis=0)
std = np.std(X_train, axis=0)
X_train = (X_train - mean) / std
X_test = (X_test - mean) / std

class SVM(object):
   #defining the kernel functions using numpy vectorization to speed up the process
    def linear_kernel(self, X1, X2):
        return np.dot(X1, X2.T)

    def __init__(self,kernel_str = 'linear',C=1.0, gamma =1.0) -> None:
        if kernel_str == 'linear':
            self.kernel = self.linear_kernel
        else:
          self.kernel = "invalid"
          print("Invalid kernel")

        self.C = C
        self.gamma = gamma
        self.kernel_str = kernel_str
        if self.C is not None: self.C = float(self.C)
        if self.gamma is not None: self.gamma = float(self.gamma)
