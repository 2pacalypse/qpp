import torch.nn as nn

class Scan_NN(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(61, 32),
            nn.LeakyReLU(),
            #nn.Linear(64, 32)
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 61),
            #nn.LeakyReLU(),
            #nn.Linear(64,64)
        )

    def forward(self, x):
        enc = self.encoder(x)
        dec = self.decoder(enc)
        return dec, enc


class Join_NN(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(67, 32),
            nn.LeakyReLU(),
            #nn.Linear(69,32)
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 67),
            #nn.LeakyReLU(),
            #nn.Linear(69,69)
        )

    def forward(self, x):
        enc = self.encoder(x)
        dec = self.decoder(enc)
        return dec, enc 


class Estimator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16,1),
            #nn.ReLU(),
            #nn.LeakyReLU(),
            #nn.LeakyReLU(),
            #nn.Linear(4, 1),
            #nn.LeReLU(),
            #nn.LeakyReLU(),
            #nn.Linear(8,1),
        )

    def forward(self, x):
        return self.model(x)


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(8,6),
            #nn.LeakyReLU()
            nn.ReLU(),
            nn.Linear(6,3),
            nn.ReLU(),
            nn.Linear(3,1),
            nn.ReLU(),

        )

    def forward(self, x):
        return self.model(x)
