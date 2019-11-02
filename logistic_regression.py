# -*- coding: utf-8 -*-
"""Logistic Regression

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13d0FzW1pyHMujATnn7MSFYhHReJbt65X

<img style="float: centre;" src="https://drive.google.com/uc?id=1ZVzMRu99qZNwgAM0myg0Ub0-I9hVcT9F">
"""

import torch
import torch.nn as nn
import torchvision.transforms.functional as TF
from torch.autograd import Variable
import numpy as np
import pandas as pd

"""Download the data set from 
#### https://www.kaggle.com/uciml/pima-indians-diabetes-database
"""

df = pd.read_csv("pima-indians-diabetes.data.csv",header=None)

df.head()

"""# Column names :
0. Number of times pregnant.
1. Plasma glucose concentration a 2 hours in an oral glucose tolerance test.
2. Diastolic blood pressure (mm Hg).
3. Triceps skinfold thickness (mm).
4. 2-Hour serum insulin (mu U/ml).
5. Body mass index (weight in kg/(height in m)^2).
6. Diabetes pedigree function.
7. Age (years).
8. Class variable (0 or 1).
"""

df.shape

int(df.shape[0]*0.7)

num_obs = df.shape[0]
train = df[:int(num_obs*0.7)]
test = df[int(num_obs*0.7):]

train.head()

test.head()

x_train = train.iloc[:,0:8]
y_train = train[[8]]

x_test = test.iloc[:,0:8]
y_test = test[[8]]

x_train = torch.tensor(x_train.values, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.long)
x_test = torch.tensor(x_test.values, dtype=torch.float32)
y_test = torch.tensor(y_test.values, dtype=torch.long)

x_train

x_test

y_train = y_train.reshape(-1)
y_test = y_test.reshape(-1)

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

y_test.size(0)

#CREATE THE CLASS
class LogisticRegressionModel(nn.Module):

    def __init__(self, input_dim, output_dim):
        
        super(LogisticRegressionModel, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)
    
    def forward(self, x):
        out = self.linear(x)
        return out
    print("The function is good!!")

input_dim = 8
output_dim = 2
print("The I/O is okay!!")

model = LogisticRegressionModel(input_dim, output_dim)
model.cuda()
print("Model uploaded to cuda")
criterion = nn.CrossEntropyLoss() 
num_epochs = 1000

learning_rate = 0.001
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

all_accuracy = []
all_loss = []
counter = 0

for epoch in range(num_epochs+1):
    
    if torch.cuda.is_available():
      train_inputs = Variable(x_train.cuda())
      true_train = Variable(y_train.cuda())
 
    else:
      train_inputs = Variable(x_train)
      true_train = Variable(y_train)    

    optimizer.zero_grad()
        

    train_outputs = model(train_inputs)
    
    loss = criterion(train_outputs,true_train)

    loss.backward()
       
    optimizer.step()
    
    if epoch % 50 == 0:
      correct = 0
      total = 0
      test_inputs = Variable(x_test.cuda())
      outputs = model(test_inputs)
      _, predicted = torch.max(outputs.data, 1)
      total += y_test.size(0)
      correct += (predicted.cpu() == y_test.cpu()).sum()
      accuracy = 100 * correct / total
      all_loss.append(loss.item())
      all_accuracy.append(accuracy)
      # Print Loss
      print('Epoch: {}, Loss: {}, Accuracy: {}%'.format(epoch, loss.item(),accuracy))

print(all_accuracy)
print(all_loss)

epoch = [x for x in range(0,1001,50)]
print(epoch)

import matplotlib.pyplot as plt
plt.figure(figsize=(8,8))
plt.title('Loss And Accuracy Plots')
plt.xlabel('Epochs')
plt.ylabel('Loss/Accuracy')
plt.plot(epoch, all_loss, label = 'Loss')
plt.plot(epoch, all_accuracy, label = 'Accuracy')
plt.legend()
plt.show()

"""#The end"""







































x_train = train.iloc[:,0:8]
y_train = train[[8]]
x_test = test.iloc[:,0:8]
y_test = test[[8]]

x_train = torch.tensor(x_train.values, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.float32)
x_test = torch.tensor(x_test.values, dtype=torch.float32)
y_test = torch.tensor(y_test.values, dtype=torch.long)

y_test = y_test.reshape(-1)

class LogisticRegressionModel(torch.nn.Module):

    def __init__(self):
        """
        In the constructor we instantiate nn.Linear module
        """
        super(LogisticRegressionModel, self).__init__()
        self.linear = torch.nn.Linear(8, 1)  # One in and one out

    def forward(self, x):
        """
        In the forward function we accept a Variable of input data and we must return
        a Variable of output data.
        """
        y_pred = torch.sigmoid(self.linear(x))
        return y_pred

model = LogisticRegressionModel()
model.cuda()
#LOSS CLASS
criterion = nn.BCELoss(reduction='mean')
num_epochs = 1000
#OPTIMIZER CLASS
learning_rate = 0.01
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

all_accuracy = []
all_loss = []
counter = 0
#TRAIN THE MODEL
for epoch in range(num_epochs+1):
    
    if torch.cuda.is_available():
      train_inputs = Variable(x_train.cuda())
      true_train = Variable(y_train.cuda())
 
    else:
      pass
        
    # Clear gradients w.r.t. parameters
    optimizer.zero_grad()
        
    # Forward pass to get output/logits
    train_outputs = model(train_inputs)
#     print(train_outputs.shape)
#     print(true_train.shape)    
    # Calculate Loss: softmax --> cross entropy loss
    loss = criterion(train_outputs, true_train)
        
    # Getting gradients w.r.t. parameters
    loss.backward()
        
    # Updating parameters
    optimizer.step()
    
    #counter+=1
    
    if epoch % 50 == 0:
      correct = 0
      total = 0
      test_inputs = Variable(x_test.cuda())
      outputs = model(test_inputs)
      _, predicted = torch.max(outputs.data, 1)

      total += y_test.size(0)
      correct += (predicted.cpu() == y_test.cpu()).sum()
    
      accuracy = 100 * correct / total
      all_loss.append(loss.item())
      all_accuracy.append(accuracy)
      # Print Loss
      print('Epoch: {}, Training Loss: {}, Test Accuracy: {}%'.format(epoch, loss.item(),accuracy))

print(all_accuracy)
print(all_loss)

epoch = [x for x in range(0,1001,50)]

import matplotlib.pyplot as plt
plt.figure(figsize=(8,8))
plt.title('Loss And Accuracy Plots')
plt.xlabel('Epochs')
plt.ylabel('Loss/Accuracy')
plt.plot(epoch, all_loss, label = 'Loss')
plt.plot(epoch, all_accuracy, label = 'Accuracy')
plt.legend()
plt.show()



