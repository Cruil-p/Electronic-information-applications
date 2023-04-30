import numpy as np
import os

path = './data/tree.bin'


with open(path, "rb") as f:
    
    # print(os.path.getsize(path))
   
    bkt_num = np.frombuffer(f.read(4), dtype=np.int32)[0]
    # print("bkt count: ", bkt_num)
    
    bkt_indexs = []
    for i in range(bkt_num):

        bkt_index = np.frombuffer(f.read(4), dtype=np.int32)[0]
        # print("bkt index: ", bkt_index)
        bkt_indexs.append(bkt_index)


    node_count = np.frombuffer(f.read(4), dtype=np.int32)[0]
    # print("node count: ", node_count)

    centerids=[]
    childStarts=[]
    childEnds=[]
    for i in range(node_count):
        centerid = np.frombuffer(f.read(4), dtype=np.int32)[0]
        childStart = np.frombuffer(f.read(4), dtype=np.int32)[0]
        childEnd = np.frombuffer(f.read(4), dtype=np.int32)[0]
        centerids.append(centerid)
        childStarts.append(childStart)
        childEnds.append(childEnd)
    # print("centerids counts: ", childEnds[0] - 1)
    # print(centerids[childStarts[0]:childEnds[0]])
    for i in range (childStarts[0], childEnds[0]):
        nodes = []
        nodes.append(centerids[i])
        for j in range(childStarts[i], childEnds[i]):
            nodes.append(centerids[j])
        #nodes.append(centerids[childStarts[i]])
        #nodes.append(centerids[childEnds[i]])
        #print(nodes)
        
    #print(centerids)
    #print(childStarts)
    #print(childEnds)
    #print(childStarts[0:2560])
    #print(childEnds[0:2560])
    all_centers=[]
    for num in range(bkt_num):
        bkt = bkt_indexs[num]
        for i in range(childStarts[bkt], childEnds[bkt]):
            center = centerids[i]
            centers = []
            centers.append(center)
            for j in range(childStarts[i], childEnds[i]):
                #print(centerids[j])
                centers.append(centerids[j])
            # print(centers)
            # print(len(centers))
            all_centers = all_centers + centers
    #print(all_centers)
    # print(len(all_centers))
    path2 = './out/log.txt'
    ff = open(path2, 'w')
    ff.write(str(node_count) + '\n')
    for i in range(node_count):
        ff.write(str(centerids[i]) + ' ')
    ff.write('\n')       
    for i in range(node_count):
        ff.write(str(childStarts[i]) + ' ')
    ff.write('\n')
    for i in range(node_count):
        ff.write(str(childEnds[i]) + ' ')
    ff.close()
    
    # 读取父节点ID
    #parent_ids = np.frombuffer(f.read(node_count * 4), dtype=np.int32)
    #print("parent ids: ", parent_ids)

    # 读取子节点个数
    #child_counts = np.frombuffer(f.read(node_count * 4), dtype=np.int32)
    #print("child counts: ", child_counts)

    # 读取子节点ID

    #child_ids = np.frombuffer(f.read(node_count * 4), dtype=np.int32).reshape((node_count, 1))
    #print("child ids: ", child_ids)

    # 读取节点对应的聚类中心点
    #centers = np.frombuffer(f.read(node_count * 4), dtype=np.int32).reshape((node_count, 1))
    #print("centers: ", centers)

