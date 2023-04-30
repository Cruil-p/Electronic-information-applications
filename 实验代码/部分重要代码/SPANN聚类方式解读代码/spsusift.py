import os
import SPTAG
import numpy as np
import time
import sys

n = 10000000 # data number
k = 2  # K Neighborhoods
r = 3  # query number
NumberOfThreads = '16'
Kmeans = sys.argv[1]
Leaf = sys.argv[2]

def ivecs_read(fname):
    a = np.fromfile(fname, dtype='int32')
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()


def fvecs_read(fname):
    return ivecs_read(fname).view('float32')

def bvecs_mmap(fname):
    x = np.memmap(fname, dtype='uint8', mode='r')
    d = x[:4].view('int32')[0]
    return x.reshape(-1, d + 4)[:, 4:]

def ivecs_read(fname):
    a = np.fromfile(fname, dtype='int32')
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()


def testBuild(algo, distmethod, x, out):
   i = SPTAG.AnnIndex(algo, 'Float', x.shape[1])
   i.SetBuildParam("DFS", 'true', "Index")
   i.SetBuildParam("NumberOfThreads", NumberOfThreads, "Index")
   i.SetBuildParam("BKTNumber", '1', "Index")
   i.SetBuildParam("BKTKmeansK", Kmeans, "Index")
   i.SetBuildParam("BKTLeafSize", Leaf, "Index")
   i.SetBuildParam("DistCalcMethod", distmethod, "Index")
   if i.Build(x, x.shape[0], False):
       i.Save(out)

def testBuildWithMetaData(algo, distmethod, x, s, out):
   i = SPTAG.AnnIndex(algo, 'Float', x.shape[1])
   i.SetBuildParam("NumberOfThreads", '4', "Index")
   i.SetBuildParam("DistCalcMethod", distmethod, "Index")
   if i.BuildWithMetaData(x, s, x.shape[0], False, False):
       i.Save(out)

def testSearch(index, q, k):
   j = SPTAG.AnnIndex.Load(index)
   for t in range(q.shape[0]):
       print(t)
       print(q[t])
       result = j.Search(q[t], k)
       print (result[0]) # ids
       print (result[1]) # distances

def testSearchWithMetaData(index, q, k):
   j = SPTAG.AnnIndex.Load(index)
   j.SetSearchParam("MaxCheck", '1024', "Index")
   for t in range(q.shape[0]):
       result = j.SearchWithMetaData(q[t], k)
       print (result[0]) # ids
       print (result[1]) # distances
       print (result[2]) # metadata

def testAdd(index, x, out, algo, distmethod):
   if index != None:
       i = SPTAG.AnnIndex.Load(index)
   else:
       i = SPTAG.AnnIndex(algo, 'Float', x.shape[1])
   i.SetBuildParam("NumberOfThreads", '4', "Index")
   i.SetBuildParam("DistCalcMethod", distmethod, "Index")
   if i.Add(x, x.shape[0], False):
       i.Save(out)

def testAddWithMetaData(index, x, s, out, algo, distmethod):
   if index != None:
       i = SPTAG.AnnIndex.Load(index)
   else:
       i = SPTAG.AnnIndex(algo, 'Float', x.shape[1])
   i.SetBuildParam("NumberOfThreads", '4', "Index")
   i.SetBuildParam("DistCalcMethod", distmethod, "Index")
   if i.AddWithMetaData(x, s, x.shape[0], False, False):
       i.Save(out)

def testDelete(index, x, out):
   i = SPTAG.AnnIndex.Load(index)
   ret = i.Delete(x, x.shape[0])
   print (ret)
   i.Save(out)
   
def Test(algo, distmethod):
   # x = np.ones((n, 128), dtype=np.float32) * np.reshape(np.arange(n, dtype=np.float32), (n, 1))
   x = bvecs_mmap("./sift10m/sift_10M_learn.bvecs")
   x = x.reshape(-1, 128)
   x = np.array(x, dtype=np.float32)
   q = np.ones((r, 128), dtype=np.float32) * np.reshape(np.arange(r, dtype=np.float32), (r, 1)) * 2
   m = ''
   for i in range(n):
       m += str(i) + '\n'

   m = m.encode()

   print ("Build.............................")
   start_time = time.time()
   testBuild(algo, distmethod, x, path)
   print("Jet lag: {0:.6f}s".format(time.time() - start_time))
   # testSearch(path, q, k)
   #print ("Add.............................")
   #testAdd(path, x, path, algo, distmethod)
   #testSearch(path, q, k)
   #print ("Delete.............................")
   #testDelete(path, q, path)
   #testSearch(path, q, k)

   #print ("AddWithMetaData.............................")
   #testAddWithMetaData(None, x, m, path, algo, distmethod)
   #testSearchWithMetaData(path, q, k)
   #print ("Delete.............................")
   #testDelete(path, q, path)
   #testSearchWithMetaData(path, q, k)


path = './data'

if __name__ == '__main__':
   Test('BKT', 'L2')
   # Test('KDT', 'L2')
   print(os.listdir(path))

