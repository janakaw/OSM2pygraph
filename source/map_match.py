import os, sys
import xml.etree.ElementTree as ET
import numpy  
from rtree import index
import pprint
#from sPickle import *
import pickle
import time
import calendar
import pylab


#--------
from vector_calc import *
from load_map import *
from forest_m_candidate import *
from operator import itemgetter, attrgetter



def read_into_array(file):
    f = open(file,'r')
    a = []
    count=0
    
    for line in f:
        count=count+1
        if count>6:
            row = line.split(',')
            row_num = [float(row[0]),float(row[1])]
            a.append(row_num)
        else:
            continue
    
    return a

def read_into_array_taxi(file):
    f = open(file,'r')
    a = []
    count=0
    
    for line in f:
        row = line.split(',')
        row_num = [float(row[2]),float(row[3]), row[1]]
        a.append(row_num)
    
    return a

def serialize_all(node_lat_array, node_lon_array, node_list,
          adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list, gr):

    output = open('map-data-lists.pk', 'wb')

    # Pickle dictionary using protocol 0.
    pickle.dump(node_lat_array, output)
    pickle.dump(node_lon_array, output)
    pickle.dump(node_list, output)
    pickle.dump(adj_list, output)
    pickle.dump(node_way, output)
    pickle.dump(edge_count, output)
    pickle.dump(edge_tags, output)
    pickle.dump(node_vector, output)
    pickle.dump(edge_list, output)
    pickle.dump(inv_edge_list, output)
        
    print("gr-bef:" + str(len(gr.edges())))

    pickle.dump(gr, output)
    output.close()
    print("serialized")

#load all data structures from serialised file
def load_all():

    input_data = open('map-data-lists.pk', 'rb')

    node_lat_array = pickle.load(input_data)
    node_lon_array = pickle.load(input_data)
    node_list = pickle.load(input_data)
    adj_list = pickle.load(input_data)
    node_way = pickle.load(input_data)
    edge_count = pickle.load(input_data)
    edge_tags = pickle.load(input_data)
    node_vector = pickle.load(input_data)
    edge_list = pickle.load(input_data)
    inv_edge_list = pickle.load(input_data)
    
    gr = pickle.load(input_data)
    #print("lat array:" + str(len(list(node_lat_array))))
    #print("lon arrat:" + str(len(list(node_lon_array))))
    #print("node list:" + str(len(list(node_list))))
    print("gr-aft:" + str(len(gr.edges())))
    input_data.close()

    return [node_lat_array, node_lon_array, node_list,
          adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list, gr]

#create all the DSs from the scratch and serialize,
# returns the DSs
def create_and_serialize_data_structures(node_lat_array, node_lon_array, node_list,
          adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list, gr):
    
    map_path = "C:\Users\Janaka\Dropbox\Research\OSM\OSM\map_large\\beijing.osm"
    file_name = "beijing"
    map_root_osm = load_map(map_path)
        
    #load noda data into defined structures
    parse_map(map_root_osm, file_name, node_lat_array, node_lon_array, node_list,
          adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list, gr)
    print "size bef lat array : " + str(len(node_lat_array))

    serialize_all(node_lat_array, node_lon_array, node_list,
          adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list, gr)

    print("lat array:" + str(len(node_lat_array)))
    print("lon arrat:" + str(len(node_lon_array)))
    print("node list:" + str(len(node_list)))

    print "inv_list"
    print len(inv_edge_list)
    
    print "serialized"
    
    #[node_lat_array, node_lon_array, node_list,
    #     adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list] = load_all()
    
    return #[inv_edge_list, node_lat_array, node_lon_array]

#def read_map(map_root_osm, file_name):
def read_map():
    # latitude and longitude of nodes
    node_lat_array = {}
    node_lon_array = {}
    #node list, define as a dictionary rather than using a set
    node_list = {}
    #adjacency list
    adj_list = {}
    #node --> way mapping
    node_way = {}   
    #we will assign points to the edges closeby and select
    # the edge with highest count, init here
    edge_count = {}
    #edge type (highway type, way id)
    edge_tags = {}
    # keep node coord as a vector
    node_vector = {}
    # edges are kept in a map, key = lower_node_id, higher_node_id
    edge_list = {}
    #inverse edge list for easy access of end nodes
    inv_edge_list = {}

    #load noda data into defined structures
    #parse_map(map_root_osm, file_name, node_lat_array, node_lon_array, node_list,
    #      adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list)
    #print "size : " + str(len(node_lat_array))

    #serialize_all(node_lat_array, node_lon_array, node_list,
    #      adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list)

    #print "serialized"
    
    [node_lat_array, node_lon_array, node_list,
          adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list] = load_all()
    
    return [inv_edge_list, node_lat_array, node_lon_array]

def print_edge_array(path_log, edge_array, node_lat_array, node_lon_array, edge_obj_list):
    #    path_log = open("C:\\Users\\janakaw\\Dropbox\\Research\\geolife-osm-labs\\OSM\\logs\\matched_path_edge.txt",'w')
    
    for edge_id in edge_array:
        edge = edge_obj_list[int(edge_id)]
        lat_val = float(node_lat_array[str(edge[0])]) #+ 0.0013
        lon_val = float(node_lon_array[str(edge[0])]) #+ 0.0061
        path_log.write(str(lat_val)+","+str(lon_val)+"\n");
        lat_val = float(node_lat_array[str(edge[1])]) #+ 0.0013
        lon_val = float(node_lon_array[str(edge[1])]) #+ 0.0061
        path_log.write(str(lat_val)+","+str(lon_val)+"\n");
    path_log.close()

def print_node_array_geodetic(node_array_geodetic):
    path_log = open("C:\\Users\\Janaka\\Dropbox\\Research\\OSM\\OSM\\logs\\matched_path_geo.txt",'w')
    
    for node_geo in node_array_geodetic:
        path_log.write(node_geo);
    path_log.close()

def remove_duplicates(edge_list):

    edge_list_no_duplicates = []
    count = 0
    f = 0
    for i in edge_list:
        '''if count == 0:
            count = 1
            f=1
            prev = i.strip()
            continue
        cur = i.strip()
        if cur == prev:
            f = f + 1
            continue
        else:
            #can have a better matric based on edge length points/unit length
            if f>0:
                edge_list_no_duplicates.append(prev);
                print(prev + ":" + str(f))
            f = 1 
            prev = cur'''
        edge_list_no_duplicates.append(i.strip());
    
    #print(prev + ":" + str(f))
    #print("duplicates removed")
    return edge_list_no_duplicates


def get_common_node(edge1, edge2):
    [e1_end_0, e1_end_1] = edge1.split(',')
    [e2_end_0, e2_end_1] = edge2.split(',')
    if e1_end_0 == e2_end_0:
        return [0, 0]
    elif e1_end_0 == e2_end_1:
        return [0, 1]
    elif e1_end_1 == e2_end_0:
        return [1, 0]
    elif e1_end_1 == e2_end_1:
        return [1, 1]
    else:
        return [-1, -1]

def convert_edge_to_ECEF(edge, lat_a, lon_a):
    [end0, end1] = edge.split(',')
    v1 = geodetic_to_ECEF(lat_a[end0],lon_a[end0])
    v2 = geodetic_to_ECEF(lat_a[end1],lon_a[end1])
    return [v1, v2]

def get_node_id_edge(edge):
    return edge.split(',')

def get_geodetic_edge(edge, lat_a, lon_a):
    [end0, end1] = edge.split(',')
    return [[lat_a[end0], lon_a[end0]], [lat_a[end1], lon_a[end1]]]

def link_edges(edge_list, node_lat_array, node_lon_array):
    # keep nodes in "lat,lon" form
    path_node_list = []
    start_flag = 0
    count = 0
    # previous end that was connected
    prev_common_end = -1
    common_end = -1
    for edge in edge_list:
        if start_flag == 0:
            temp_list=[]
            prev = edge
            prev_ends = get_geodetic_edge(prev, node_lat_array, node_lon_array)
            start_flag = 1
            continue
        cur = edge
        #1. same edge
        if prev == cur:
            continue
        cur_ends = get_geodetic_edge(cur, node_lat_array, node_lon_array)
        # check for case 1 - two edges share a node on graph
        [end1, end2] = get_common_node(prev, cur)
        #print str(end1) + ":" + str(end2) 
        #common node on graph is available
        # 2. common node exists
        if end1 != -1:
            if start_flag == 1:
                temp_list.append(prev_ends[(end1+1)%2][0]+","+prev_ends[(end1+1)%2][1]+"\n")
            temp_list.append(prev_ends[end1][0]+","+prev_ends[end1][1]+"\n")
            prev_common_end = end2
            #path_node_list.append(cur_ends[(end2+1)%2][0]+","+cur_ends[(end2+1)%2][1]+"\n")
            count = count + 1
            prev = cur
            prev_ends = cur_ends            
        # 3. no common node
        # a. map fault
        # b. outlier
        else:
            #connecte list added to master lis
            path_node_list.append(temp_list)
            #init next connected list
            temp_list=[]
            prev = edge
            prev_ends = get_geodetic_edge(prev, node_lat_array, node_lon_array)
            temp_list.append(prev_ends[0][0]+","+prev_ends[0][1]+"\n")
            temp_list.append(prev_ends[1][0]+","+prev_ends[1][1]+"\n")
            start_flag = 1
            
            '''if prev_common_end == -1:
                print "no prev common end"
                continue
            e1 = convert_edge_to_ECEF(prev, node_lat_array, node_lon_array)
            e2 = convert_edge_to_ECEF(cur, node_lat_array, node_lon_array)

            d2 = get_mag(e1[(prev_common_end+1)%2],e2[0])
            d3 = get_mag(e1[(prev_common_end+1)%2],e2[1])

            if d2 < d3:
                common_end = 0
            else:
                common_end = 1
                d2 = d3

            path_node_list.append(prev_ends[(prev_common_end+1)%2][0]+","+prev_ends[(prev_common_end+1)%2][1]+"\n")
            path_node_list.append(cur_ends[common_end][0]+","+cur_ends[common_end][1]+"\n")

            prev_common_end = common_end '''
            #inter_sect = line_line_intersection(e1[0],e1[1],e2[0],e2[1])

            '''if len(inter_sect) == 0:
                path_node_list.append(prev_ends[(end1+1)%2][0]+","+prev_ends[(end1+1)%2][1]+"\n")
                path_node_list.append(prev_ends[end1][0]+","+prev_ends[end1][1]+"\n")
                path_node_list.append(cur_ends[(end2+1)%2][0]+","+cur_ends[(end2+1)%2][1]+"\n")
                print "no intersect" + str(start_flag)
                #return path_node_list
            else:
                [p1, p2, mua, mub] = inter_sect
                # shortest distance between the two edges 
                d = get_mag(p1,p2)
                print "d: " + str(d) + ":" + str(start_flag)
                # if distance between two edges is less than
                # 200m append verticle segment p1,p2 to
                # list, v1 or v2 (part of prevedge) is already in the list
                # 
                if d < 50:
                    [lat, lon] = ecef2geodetic(p1[0], p1[1], p1[2])
                    path_node_list.append(str(lat)+","+str(lon)+"\n")
                    [lat, lon] = ecef2geodetic(p2[0], p2[1], p2[2])
                    path_node_list.append(str(lat)+","+str(lon)+"\n")'''
                       
                
            
        
    path_node_list.append(temp_list)

    count1 = 0
    for l in path_node_list:
        count1 = count1 + 1
        path_log = open("C:\\Users\\Janaka\\Dropbox\\Research\\OSM\\OSM\\logs\\matched_path_geo_" + str(count1) + ".txt",'w')
        for node_geo in l:
            path_log.write(node_geo);
        path_log.close()
        
    return path_node_list[0]

def read_into_array_input(file):
        f = open(file,'r')
        a = []
        count=0

        for line in f:
                a.append(line)
                
        return a

# input date time string : output-> seconds since the epoch (assuming UTC)
def convert_datetime_str_to_timestamp(date_time):
    t = time.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    return calendar.timegm(t)
    

def serialize_object_maps(edge_map, node_map):

    output = open('map-object-lists.pk', 'wb')

    # Pickle dictionary using protocol 0.
    pickle.dump(edge_map, output)
    pickle.dump(node_map, output)
            
    print("gr-bef:" + str(len(edge_map)))

    output.close()
    print("serialized")

#load all data structures from serialised file
def load_object_maps():

    input_data = open('map-object-lists.pk', 'rb')

    edge_map = pickle.load(input_data)
    node_map = pickle.load(input_data)
    
    input_data.close()

    return [edge_map, node_map]

def create_obj_map(gr, edge_list):
    edge_obj_list = {}
        
    
    # create a map of edge objects indexed by edge_id given in load_map
    for edge in gr.edges():
        e = Edge(int(edge[0]),int(edge[1]),-1,-1, -1, "-1", -1, "-1", "-1", "-1", "-1")
        at0 = gr.node_attributes(edge[0])
        at1 = gr.node_attributes(edge[1])
        # check if both node are valid (has lat, lon)
        if at0[0][1]=="y" and at1[0][1] == "y":
            e_attrs = gr.edge_attributes(edge)
            # e_attrs[2][1] - unique edge id given in load_map
            edge_obj_list[edge_list[e.edge_label_str][0]] = edge

    node_obj_list = {}

    # create a map of node objects indexed by node_id given in load_map
    for node in gr.nodes():
        node_obj_list[str(node)] = node
    
    return [edge_obj_list, node_obj_list];
flag = 0
def sort_by_dist(p, edge_obj_list, node_lat_array, node_lon_array):
    global flag
    
    temp = {}
    dist_list = {}
    
    for i in edge_obj_list:
        e1 = convert_geodetic_to_vector([node_lat_array[str(edge_obj_list[i].node1)], node_lon_array[str(edge_obj_list[i].node1)]])
        e2 = convert_geodetic_to_vector([node_lat_array[str(edge_obj_list[i].node2)], node_lon_array[str(edge_obj_list[i].node2)]])
        dist = perpendicular_distance(vector(p[0],p[1],p[2]), e1, e2)
        #if dist[0]==0:
        temp[str(dist[1])] = edge_obj_list[i]
        dist_list[dist[1]] = dist

    sorted_list = sorted(dist_list)
    if flag==0:
        print(sorted_list)
        flag = 1

    i=0
    for d in sorted_list:
       edge_obj_list[i] = temp[str(dist_list[d][1])]
       edge_obj_list[i].dist_from_point = round(dist_list[d][1],2);
       edge_obj_list[i].ang = dist_list[d][0];
       i = i + 1 
    return edge_obj_list

def find_nn(p, count, cur_edge_list, cur_edge_obj_list, edge_obj_list, edge_list, c1, edge_index_3d, gr, node_lat_array, node_lon_array):

    if count == 12:
        return sort_by_dist(p, cur_edge_obj_list, node_lat_array, node_lon_array)

    for n in edge_index_3d.nearest((p[0],p[1],p[2],p[0],p[1],p[2]),12):
                   
                exist = False

                #avoid repeating edges
                if c1 == 0:
                    cur_edge_list.append(n)
                else:
                    for n1 in cur_edge_list:
                        if str(n1) == str(n):
                            exist = True
                            break;
                    if exist:
                        continue;
                    cur_edge_list.append(n)
                
                edge = edge_obj_list[int(str(n))]
                wt = gr.edge_weight(edge)
                e = Edge(int(edge[0]),int(edge[1]),-1,-1, -1, "-1", -1, "-1", "-1", "-1", "-1")
                attr_list = edge_list[e.edge_label_str][1]
                
                #print(n)
                
                #if wt > 0.0001:
                    
                way_id = int(attr_list["way_id"])
                way_type = str(attr_list["way_type"])
                road_name = str(attr_list["name"].encode('utf-8'))
                name_en = str(attr_list["name_en"].encode('utf-8'))
                lanes = str(attr_list["lanes"].encode('utf-8'))
                oneway = str(attr_list["oneway"].encode('utf-8'))

                edge_forest = Edge(int(edge[0]),int(edge[1]), 1 , wt, way_id, way_type, p[3], road_name, name_en, lanes, oneway)
                cur_edge_obj_list[c1] = edge_forest
                c1 = c1 + 1
    count = count + 1
    return sort_by_dist(p, cur_edge_obj_list, node_lat_array, node_lon_array)
    #return find_nn(p, count, cur_edge_list, cur_edge_obj_list, edge_obj_list, edge_list, c1, edge_index_3d, gr, node_lat_array, node_lon_array)

def map_match():
    #read trajectory file into an array
    #infile = "C:\\Users\\janakaw\\Dropbox\\Research\\geolife-osm-labs\\OSM\\T\\003\\20081023175854.plt"
        
    # latitude and longitude of nodes
    node_lat_array = {}
    node_lon_array = {}
    #node list, define as a dictionary rather than using a set
    node_list = {}
    #adjacency list
    adj_list = {}
    #node --> way mapping
    node_way = {}
    #we will assign points to the edges closeby and select
    # the edge with highest count, init here
    edge_count = {}
    #edge type (highway type, way id)
    edge_tags = {}
    # keep node coord as a vector
    node_vector = {}
    # edges are kept in a map, key = lower_node_id, higher_node_id
    edge_list = {}
    #inverse edge list for easy access of end nodes
    inv_edge_list = {}

    # Graph creation
    gr = graph()

    edge_obj_list = {}
    
    node_obj_list = {}
            
    # load data structures from scratch
    #create_and_serialize_data_structures(node_lat_array, node_lon_array, node_list,
    #      adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list, gr);

    #serialize_all(node_lat_array, node_lon_array, node_list,
    #      adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list, gr1);
    [node_lat_array, node_lon_array, node_list,
          adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list, gr] = load_all()


    #########
    #[edge_obj_list, node_obj_list] = create_obj_map(gr, edge_list)
    #serialize_object_maps(edge_obj_list, node_obj_list)
    #########
    [edge_obj_list, node_obj_list] = load_object_maps()
    
    print "loaded"

    #return

    # load edge r-tree index from archived file
    p = index.Property()
    p.dimension = 3
    edge_index_3d = index.Rtree('edge_index_3d_beijing',properties=p)

    #inpath = "C:\Users\janakaw\Dropbox\Research\geolife-osm-labs\OSM\logs\\004-trajs.txt"
    #path = 'C:\Users\Janaka\Dropbox\Research\OSM\OSM\logs\paths-taxi-01-mapped\\'
    #path = 'C:\Users\janakaw\Dropbox\Research\geolife-osm-labs\OSM\logs\paths-004-mapped-trial\\'


    

    
        


    
    forest_count = 0
    traj_path_root = 'C:\\taxidata\\01_part\\'

    #init forest
    f = Forest(node_lat_array, node_lon_array, gr)
    
    #process a trajectory batch (of all taxies) for a day: p - a taxi 
    for p in os.listdir(traj_path_root):
        p = p.strip()
        traj_path = traj_path_root  + '\\\\' + p;
        print(str(traj_path))
        a = read_into_array_taxi(traj_path)

        #file to log edges in a 
        #path_log = open(traj_path_root + p +"-edge.txt",'w')
        # each taxi trajectory in the day is represented as a forest
        forest_count = forest_count + 1

       
    
        point_array = []
        for pt in a:
            point_array.append(geodetic_to_ECEF_timestamp(pt[1],pt[0],convert_datetime_str_to_timestamp(pt[2])))
        
        print "finding nearest edges"

        # edges are kept on a map: key = edge_id : value = frequency
        mapped_path_edges = {}
        #start = time.clock()
        tc = 0
        ttc = 0
        
        print("pt array size:" + str(len(point_array)))
        print("edge count bef:" + str(tc))
        
        for p in point_array:
            # nearest 1 edge
            tc = tc + 1
            #if tc > 1000:
            #    break;

            cur_edge_list = []
            cur_edge_obj_list = {}
            
            # 5 neighbours considered to handle complex intersections
            c1 = 0
            #edge_index_3d.insert(int(500000),(p[0],p[1],p[2],p[0],p[1],p[2]), obj=500000)
            #print("len:" + str(count(edge_index_3d.nearest((p[0],p[1],p[2],p[0],p[1],p[2]),3))))
            #print("#######")
            #for n in edge_index_3d.nearest((0,0,0, 200,200,200),5):

            cur_edge_obj_list = find_nn(p, 1, cur_edge_list, cur_edge_obj_list, edge_obj_list, edge_list, c1, edge_index_3d, gr, node_lat_array, node_lon_array)
                
            '''for n in edge_index_3d.nearest((p[0],p[1],p[2],p[0],p[1],p[2]),12):
            #for n in edge_index_3d.intersection((str(int(p[0])- 100),str(int(p[1])-100),str(int(p[2])-100),str(int(p[0])+100),str(int(p[1])+100),str(int(p[2])+100)), objects=True):

                
                exist = False

                #avoid repeating edges
                if c1 == 0:
                    cur_edge_list.append(n)
                else:
                    for n1 in cur_edge_list:
                        if str(n1) == str(n):
                            exist = True
                            break;
                    if exist:
                        continue;
                    cur_edge_list.append(n)
                
                edge = edge_obj_list[int(str(n))]
                wt = gr.edge_weight(edge)
                e = Edge(int(edge[0]),int(edge[1]),-1,-1, -1, "-1", -1, "-1", "-1", "-1", "-1")
                attr_list = edge_list[e.edge_label_str][1]
                
                #print(n)
                
                #if wt > 0.0001:
                    
                way_id = int(attr_list["way_id"])
                way_type = str(attr_list["way_type"])
                road_name = str(attr_list["name"].encode('utf-8'))
                name_en = str(attr_list["name_en"].encode('utf-8'))
                lanes = str(attr_list["lanes"].encode('utf-8'))
                oneway = str(attr_list["oneway"].encode('utf-8'))

                edge_forest = Edge(int(edge[0]),int(edge[1]), 1 , wt, way_id, way_type, p[3], road_name, name_en, lanes, oneway)
                cur_edge_obj_list[c1] = edge_forest
                c1 = c1 + 1'''
                
            if len(cur_edge_obj_list) > 5:
                #print(len(cur_edge_obj_list))
                f.insert_forest(p, cur_edge_obj_list)#[0], cur_edge_obj_list[1], cur_edge_obj_list[2])
        #print("edge count:" + str(tc))
        #print("edge count distinct:" + str(ttc))
        
        c=0

        f.print_forest(gr, edge_list);
        print(len(mapped_path_edges))
         
    
map_match()




