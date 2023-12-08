import torch


class Dataset(torch.utils.data.Dataset):
    def __init__(self, X, by):
        assert len(X.shape) == 2
        assert len(by.shape) == 1
        assert X.shape[0] == by.shape[0]

        self.X = X
        self.by = by

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        bx = self.X[index]
        y = self.by[index]
        
        return bx, y
