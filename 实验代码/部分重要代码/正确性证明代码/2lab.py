import pandas as pd
from sklearn.cluster import MiniBatchKMeans, KMeans
import kmeans
import numpy as np
from numpy import loadtxt
import time

def bvecs_mmap(fname):
    x = np.memmap(fname, dtype='uint8', mode='r')
    d = x[:4].view('int32')[0]
    return x.reshape(-1, d + 4)[:, 4:]

def ivecs_read(fname):
    a = np.fromfile(fname, dtype='int32')
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()

def ivecs_read(fname):
    a = np.fromfile(fname, dtype='int32')
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()


def fvecs_read(fname):
    return ivecs_read(fname).view('float32')


xb = fvecs_read('./sift1m/sift_base.fvecs')
xq = fvecs_read('./sift1m/sift_query.fvecs')
xl = fvecs_read('./sift1m/sift_learn.fvecs')
gt = ivecs_read('./sift1m/sift_groundtruth.ivecs')

# xb = bvecs_mmap('./sift10m/sift_10M_learn.bvecs') # 10M
# xq = bvecs_mmap('./sift10m/sift_10M_query.bvecs')
# gt = ivecs_read('./sift10m/sift_10M_groundtruth.ivecs')

xb = np.array(xb)
xb = xb.reshape(-1, 128)
xb = np.array(xb, dtype=np.float32)
xq = np.array(xq)
xq = xq.reshape(-1, 128)
xq = np.array(xq, dtype=np.float32)
xl = np.array(xl)
xl = xl.reshape(-1, 128)
xl = np.array(xl, dtype=np.float32)
clus = 256

mini_kmeans = MiniBatchKMeans(n_clusters = clus, random_state = 0, batch_size = 500, verbose = 0, max_iter = 10, n_init = 1).fit(xb)
mini_centers = mini_kmeans.cluster_centers_
counts1 = pd.Series(mini_kmeans.labels_)
print(len(mini_centers))

kmeans = KMeans(n_clusters = clus, random_state = 0, n_init= 'auto', init = "k-means++")
kmeans = kmeans.fit(xb)
kmeans_centers = kmeans.cluster_centers_
counts2 = pd.Series(kmeans.labels_)
print(len(kmeans_centers))

cnt_mini = [0] * clus
cnt_kmeans = [0] * clus
mini = [0] * clus
kmean = [0] * clus

for i in range(len(counts1)):
    mini[counts1[i]] = mini[counts1[i]] + 1
    kmean[counts2[i]] = kmean[counts2[i]] + 1
numsum = len(xl) # the number of random numbers
for i in range(numsum):
    a = xl[i]
    min1 = 10000000.1
    min2 = 10000000.1
    idx1 = clus
    idx2 = clus
    for j in range(clus):
        dist1 = np.sum(np.square(a - mini_centers[j]))
        dist2 = np.sum(np.square(a - kmeans_centers[j]))
        if (dist1 < min1):
            min1 = dist1
            idx1 = j
        if (dist2 < min2):
            min2 = dist2
            idx2 = j
    cnt_mini[idx1] = cnt_mini[idx1] + 1
    cnt_kmeans[idx2] = cnt_kmeans[idx2] + 1
print(cnt_mini)
print(mini)
print(cnt_kmeans)
print(kmean)
sum1 = 0
sum2 = 0
for i in range(len(cnt_mini)):
    sum1 = sum1 + cnt_mini[i]
    sum2 = sum2 + cnt_kmeans[i]
print(sum1 == numsum)
print(sum2 == numsum)
ans1 = [0.0] * clus
ans2 = [0.0] * clus
for i in range(clus):
    if (cnt_mini[i] != 0):
        ans1[i] = mini[i] / cnt_mini[i] / 10
    if (cnt_kmeans[i] != 0):
        ans2[i] = kmean[i] / cnt_kmeans[i] / 10
print(ans1)
print(ans2)