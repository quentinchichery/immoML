import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

class Hollomon:
    def set_param_from_norm(self, X):
        self.K = (2000 - 500) * X[0] + 500
        self.n = (0.5 - 0.01) * X[1] + 0.01

    def hardening(self, x):
        y = self.K * x ** self.n
        return y


model = Hollomon()
x = np.linspace(0, 1, 30)

scale = 2000

# create data for training / test
dataset = []
for _ in range(10200):
    K = np.random.rand()
    n = np.random.rand()
    model.set_param_from_norm([K, n])
    y = model.hardening(x) / scale
    dataset.append([y , np.array([K, n])])

print(dataset[0])
dataset_train = dataset[:10000]
train_features = np.array([item[0] for item in dataset_train])
train_label = np.array([item[1] for item in dataset_train])
dataset_test = dataset[10000:]
test_features = np.array([item[0] for item in dataset_test])
test_label = np.array([item[1] for item in dataset_test])

# build neural network
input_size = 30
hidden_size = 30
output_size = 2
num_epochs = 10
batch_size = 1000
learning_rate = 0.01

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)  
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

model_nn = NeuralNet(input_size, hidden_size, output_size)

# Loss and optimizer
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model_nn.parameters(), lr=learning_rate)  

train_loss = []
test_loss = []
epochs = []

fig, ax = plt.subplots()


num_batch = int(len(train_features)/batch_size)
for epoch in range(num_epochs):
    epochs.append(epoch)
    
    # Train the model
    for batch in range(num_batch):
        batch_loss = []
        train_features_loader = train_features[ batch * batch_size : ((batch+1) * batch_size) -1]
        train_label_loader = train_label[ batch * batch_size : ((batch+1) * batch_size) -1]
        # for i, item in enumerate(dataset_train): 
        x = torch.from_numpy(train_features_loader).float()
        target = torch.from_numpy(train_label_loader).float()
        # Forward pass
        outputs = model_nn(x)
        loss = criterion(outputs, target)
        batch_loss.append(loss.item())
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
        print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
            .format(epoch+1, num_epochs, batch+1, num_batch, loss.item()))

    train_loss.append(max(batch_loss))

    # test
    x = torch.from_numpy(test_features).float()
    target = torch.from_numpy(test_label).float()
    outputs = model_nn(x)
    loss = criterion(outputs, target)
    test_loss.append(loss.item())

    plt.scatter(epochs, train_loss)
    plt.scatter(epochs, test_loss)
    plt.pause(1)
    plt.draw()


plt.ion()
fig, ax = plt.subplots()
x = np.linspace(0, 1, 30)


# use model to predict
for _ in range(10):
    K = np.random.rand()
    n = np.random.rand()
    print([K, n])
    model.set_param_from_norm([K, n])
    y = model.hardening(x)

    x_predict = model_nn(torch.from_numpy(y).float()/scale)
    print(x_predict)
    model.set_param_from_norm(x_predict.detach().numpy())
    y_predict = model.hardening(x)

    plt.cla()
    plt.scatter(x, y)
    plt.scatter(x, y_predict)
    plt.pause(1)
    plt.draw()

