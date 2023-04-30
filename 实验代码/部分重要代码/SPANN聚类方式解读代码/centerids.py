import faiss
import numpy as np
from numpy import loadtxt

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


# xb = fvecs_read('../sift1m/sift_base.fvecs')
# xq = fvecs_read('../sift1m/sift_query.fvecs')
# gt = ivecs_read('../sift1m/sift_groundtruth.ivecs')


xb = bvecs_mmap('./sift10m/sift_10M_learn.bvecs') # 10M
xq = bvecs_mmap('./sift10m/sift_10M_query.bvecs')
gt = ivecs_read('./sift10m/sift_10M_groundtruth.ivecs')

xb = np.array(xb)
xb = xb.reshape(-1, 128)
xb = np.array(xb, dtype=np.float32)

xq = np.array(xq)
xq = xq.reshape(-1, 128)
xq = np.array(xq, dtype=np.float32)


path1 = "./out/outfile.txt"

with open(path1, "r") as tf:
    lines = tf.read().split('\n')
nlist = int(len(lines))
# print(nlist)

number = 0
centriods = []
ori_cen = []
for line in lines:
    li = line.split(' ')
    # print(len(li))
    # for k in li:
    nodes = np.zeros(128)
    number = number + 1
    # if number <= 100:
        # print(li[0])
    ori_cen.append(xb[int(li[0])])
    for i in li:
        xxx = xb[int(i)]
        xxx = np.array(xxx)
        nodes += xxx
    #  print(nodes)
    centriods.append(nodes/len(li))
# print(number)
centriods = np.array(centriods)
centriods = centriods.reshape(-1, 128)
ori_cen = np.array(ori_cen)
ori_cen = ori_cen.reshape(-1, 128)
# print(centriods)
# print(len(centriods))
# print(ori_cen)
# print(len(ori_cen))

def sift_10M_search(centroids, xt, query, gt, nprobe):
    # 通过centroids 将所有数据添加到相应的聚类中心里
    # 使用faiss.Kmenas的assign()操作, 可以直接输出每个簇中的训练数据编号，然后查询gt中top10是否在搜索范围内
    n_clus = len(centroids)
    dim = xt.shape[1]
    km = faiss.Kmeans(
        d=dim, k=n_clus,
        max_points_per_centroid=1,
        verbose=True
    )
    km.train(centroids)
    _, assign = km.assign(xt)

    bc = np.bincount(assign, minlength=n_clus)  # 会出现只有一个点的簇，这个问题比较麻烦
    print('incremental training', np.std(bc))

    o = assign.argsort()
    i0 = 0
    clusters = []  # 将所有点添加到相应的聚类中心
    for c1 in range(n_clus):
        i1 = i0 + bc[c1]
        subset = o[i0:i1]
        clusters.append(subset)
        i0 = i1
    ndis = 0
    count = 0

    for i in range(len(query)):
        q = query[i]
        dis = np.square(q - centroids)
        dis = np.sum(dis, axis=1)
        nprobe_clus_idx = np.argsort(dis)[:nprobe]
        gt_10 = gt[i][:10]
        candidate = []
        for idx in nprobe_clus_idx:
            candidate.append(clusters[idx])

        for gt_item in gt_10:
            for j in range(len(candidate)):
                ndis = ndis + len(candidate[j])
                if gt_item in candidate[j]:
                    count = count + 1
    recall = count/(10*len(query))
    print("recall: ", recall)
    print("nids: ", ndis/(nprobe*len(query)))
    del km
    return recall
nprobe = 10
print("means cen: ")
re = sift_10M_search(centriods, xb, xq, gt, nprobe) # means cen
print("ori cen: ")
re = sift_10M_search(ori_cen, xb, xq, gt, nprobe) # ori cen
