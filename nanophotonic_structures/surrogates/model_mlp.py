from torch import nn


class MLP(nn.Module):
    def __init__(self, dim_input):
        super().__init__()

        self.layer_first = nn.Linear(dim_input, 128)
        self.bn_first = nn.BatchNorm1d(128)
        self.relu_first = nn.ReLU()
        self.layer_second = nn.Linear(128, 64)
        self.bn_second = nn.BatchNorm1d(64)
        self.relu_second = nn.ReLU()
        self.layer_third = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, X):
        outputs = self.layer_first(X)
        outputs = self.bn_first(outputs)
        outputs = self.relu_first(outputs)

        outputs = self.layer_second(outputs)
        outputs = self.bn_second(outputs)
        outputs = self.relu_second(outputs)

        outputs = self.layer_third(outputs)
        outputs = self.sigmoid(outputs)
        
        outputs = outputs.squeeze(1)

        return outputs


if __name__ == '__main__':
    import torch

    dim_input = 12

    inputs = torch.rand(64, dim_input)
    obj = MLP(dim_input)

    outputs = obj(inputs)
    print(outputs.shape)
