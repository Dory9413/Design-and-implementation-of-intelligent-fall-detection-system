import os

import torch
from torch import nn

import djangoProject.settings


class GRUNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, n_layers):
        super(GRUNet, self).__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        self.GRU = nn.GRU(input_size=input_dim,
                          hidden_size=hidden_dim,
                          num_layers=n_layers,
                          batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        h0 = self.init_hidden(x)
        out, hn = self.GRU(x, h0)
        out = self.fc(self.relu(out[:, -1]))
        return out

    def init_hidden(self, x):
        h0 = torch.zeros(self.n_layers, x.size(0), self.hidden_dim)
        return h0.cpu()


input_dim = 3
output_dim = 2
n_layers = 2
hidden_dim = 256
fall_detection_model = None
MODEL_PATH = djangoProject.settings.STATIC_ROOT + os.sep + 'SmartFall_gru.pth'

