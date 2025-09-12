import numpy as np

class Trajectory(object):
    def __init__(self, ts):
        self.ts = ts
            
    #Inputs: ts - a 2D np array of any shape. Probably a time series. 
    # b - the number of bins in each dimension
    #Output: bins - A dictionary of arrays that contains the boundaries of the bins in each dimension
    def set_bins(self,b):
        self.b = b
        d,n = self.ts.shape
        bins = {}
        for i in range(d):
            top = max(self.ts[i,:])
            bot = min(self.ts[i,:])
            step = (top - bot)/b
            ibins = []
            for j in range(b+1):
                ibins.append(bot+j*step)
            bins[i] = ibins
        self.bins = bins
        # return bins

    #Inputs: ts - time series
    #bins - the partition of each dimension into its bins
    #b - number of bins in each dimension

    #Output: binseq - a 1D array the length of ts that lists which bin each entry in the time series is in

    def bin_sequence(self):
        d,n = self.ts.shape
        bin_seq = np.zeros((n))
        for i in range(n):
            bin_n = 0
            for j in range(d):
                k = 1
                while k <= self.b:
                    if self.ts[j,i] <= self.bins[j][k]:
                        bin_n += (k-1)*(self.b**j)
                        k = self.b + 1
                    else: 
                        k = k + 1 
            bin_seq[i] = bin_n
        self.bin_seq = bin_seq
        # return binseq

    #inputs: bin-seq - the bin sequence of the time series
    #outputs: A - the adjacency matrix
    # vertices - the list of vertices, enumerated as bin numbers
    def adjacency(self, prob = False):
        vertices, counts = np.unique(self.bin_seq, return_counts=True)
        order = len(vertices)
        A = np.zeros((order,order))
        for i in range(len(self.bin_seq)-1):
            A[np.where(vertices == self.bin_seq[i]),np.where(vertices == self.bin_seq[i+1])] += 1
        if prob:
            A[:,i] = A[:,i]/np.sum(A[:,i])
        return A, vertices, counts

    def bin_centers(self):
        bin_cent = np.zeros((self.b**3,3))
        for k in range(self.b):
            for j in range(self.b):
                for i in range(self.b):
                    bin_cent[k*self.b**2 + j*self.b + i,0] += np.mean(self.bins[0][i:i+2]) 
                    bin_cent[k*self.b**2 + j*self.b + i,1] += np.mean(self.bins[1][j:j+2]) 
                    bin_cent[k*self.b**2 + j*self.b + i,2] += np.mean(self.bins[2][k:k+2]) 

        return bin_cent