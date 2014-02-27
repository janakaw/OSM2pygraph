""" load_map.py: loads an OpenStreetMap in XML format and creates the corresponding graph,
    also creates an R-tree index for edges and nodes """
__author__ = "Janaka Seneviratne"
__copyright__ = "Copyright 2014, Janaka Seneviratne"
__version__ = "0.0.1"
__maintainer__ = "Janaka Seneviratne"
__email__ = "janaka.seneviratne@gmail.com"
__status__ = "example"

import sys
import xml.etree.ElementTree as ET

from rtree import index
import numpy as np 
from vector_calc import *

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

#for Edge class to get edge_label
from forest import *

def get_map_bounds(map_root_osm):
        print "read bound"
        bound = map_root_osm.findall('bound')[0]
        box_str = bound.get('box')
        box = box_str.split(',')         
        
        bottom_left =  (box[0],box[1])
        top_right = geodetic_to_ECEF(box[2],box[3])
        
        print "TL" + str(bottom_left) + ": BR" + str(top_right)
        d = distance_a(box[0],box[1],box[2],box[3])
        print str(d/1000)


def load_map(map_path):
        map_tree_osm = ET.parse(map_path)
        map_root_osm = map_tree_osm.getroot()
        return map_root_osm


# parse all nodes in osm file and fill in the data structures
def get_nodes(map_root_osm, node_list, adj_list, edge_count, node_way,
               edge_tags, node_lat_array, node_lon_array, node_vector, gr):
        node_count = 0
        for node in map_root_osm.findall('node'):
                node_count = node_count + 1       
                node_id = node.get('id')
                #simply maintain node (vetex) list, chose dictionary
                # as opposed to a list or set, avoid duplicates
                node_list[node_id]=1
                #init adjacency list
                adj_list[node_id]={}
                #similar to adjList , but used to count points per edges
                # init here
                edge_count[node_id]={}
                # ways attached to the node, used to get turns
                node_way[node_id]=[]
                #edge type (highway type, way id)
                edge_tags[node_id]={}
                #for easy access keep separately
                node_lat_array[node_id]=node.get('lat')
                node_lon_array[node_id]=node.get('lon')

                gr.add_node(int(node_id), attrs=[("coord","y")])
        print "node count : " + str(node_count)


# fill the node vector (geodetic to eucleadian conversion),
# done after get_nodes()
def fill_node_vector(node_lat_array, node_lon_array, node_vector, gr):
        for node in gr.nodes():
                ls = gr.node_attributes(node)
                if ls[0][1]=="y":
                        node_vector[str(node)] = geodetic_to_ECEF(node_lat_array[str(node)], node_lon_array[str(node)])
                
        print "node vector filled"

        
# input nodes in vector form (not in geodetic form) i.e. node_vector and file name
# existing rtree is deleted
def create_node_rtree(node_vector, file_name):

        node_index_3d = index.Rtree('node_index_3d_'+file_name,properties=p)

        for node_id in node_vector.keys():
                node_index_3d.insert(int(node_id),(node_vector[node_id][0],node_vector[node_id][1],node_vector[node_id][2],
                                                   node_vector[node_id][0],node_vector[node_id][1],node_vector[node_id][2]))
        print "node rtree created"
        

#call this method after get_nodes() 
def get_ways(map_root_osm, node_way, adj_list, edge_count, edge_tags, edge_list, inv_edge_list, gr):

        #for rtree we need a int edge_id
        edge_id = 0
        missed_nodes_count = 0
                       
        way_count = 0
        for highway in map_root_osm.findall("./way/tag[@k='highway']/.."):
                # 1. update node_way map (node_id ----> way_id)
                # 2. tag edges incident on the way correctly
                # n1----n2----n3---....---np
                #      i. adj_list ii. edge_count iii. edge_tags

                way_count = way_count + 1
                start_way = 0
                way_id = highway.get('id')

                way_type = ""
                bicycle = ""
                cycleway = ""
                access = ""
                foot = ""
                lanes = ""
                motor_vehicle = ""
                oneway = ""
                surface = ""
                name = ""
                bridge = ""
                railway = ""
                waterway = ""
                name_en = ""
                lanes = ""
                service = ""
                horse = ""
                public_transport = ""
                int_name = ""
                junction = ""
                tunnel = ""
                name_zh_pinyin = ""
                name_zh = ""
                name_fr = ""
                alt_name = ""
                name_zh_classical = ""
                toll = ""
                lit = ""

                # store way type, motorway, service, foot path
                for tag in highway.findall("./tag"):                                                                         
                        if "highway" == tag.get('k'):
                                way_type = tag.get('v')
                        if "bicycle" == tag.get('k'):
                                bicycle = tag.get('v')
                        if "cycleway" == tag.get('k'):
                                cycleway = tag.get('v')
                        if "access" == tag.get('k'):
                                access = tag.get('v')
                        if "foot" == tag.get('k'):
                                foot = tag.get('v')
                        if "lanes" == tag.get('k'):
                                lanes = tag.get('v')
                        if "motor_vehicle" == tag.get('k'):
                                motor_vehicle = tag.get('v')
                        if "oneway" == tag.get('k'):
                                oneway = tag.get('v')
                        if "surface" == tag.get('k'):
                                surface = tag.get('v')
                        if "name" == tag.get('k'):
                                name = tag.get('v')
                        if "bridge" == tag.get('k'):
                                bridge = tag.get('v')
                        if "railway" == tag.get('k'):
                                railway = tag.get('v')
                        if "waterway" == tag.get('k'):
                                waterway = tag.get('v')
                        if "name:en" == tag.get('k'):
                                name_en = tag.get('v')
                        if "lanes" == tag.get('k'):
                                lanes = tag.get('v')
                        if "service" == tag.get('k'):
                                service = tag.get('v')
                        if "horse" == tag.get('k'):
                                horse = tag.get('v')
                        if "public_transport" == tag.get('k'):
                                public_transport = tag.get('v')
                        # same as name:en
                        if "int_name" == tag.get('k'):
                                int_name = tag.get('v')
                        if "junction" == tag.get('k'):
                                junction = tag.get('v')
                        if "tunnel" == tag.get('k'):
                                tunnel = tag.get('v')
                        if "name:zh_pinyin" == tag.get('k'):
                                name_zh_pinyin = tag.get('v')
                        if "name:zh" == tag.get('k'):
                                name_zh = tag.get('v')
                        if "name:fr" == tag.get('k'):
                                name_fr = tag.get('v')
                        if "alt_name" == tag.get('k'):
                                alt_name = tag.get('v')
                        if "name:zh-classical" == tag.get('k'):
                                name_zh_classical = tag.get('v')
                        if "toll" == tag.get('k'):
                                toll = tag.get('v')
                        if "lit" == tag.get('k'):
                                lit = tag.get('v')


                way_features = dict([("way_id", way_id), 
                ("way_type", way_type),
                ("bicycle", bicycle),
                ("cycleway", cycleway),
                ("access", access), 
                ("foot", foot), 
                ("lanes", lanes), 
                ("motor_vehicle", motor_vehicle),
                ("oneway", oneway),
                ("surface", surface), 
                ("name", name),
                ("bridge", bridge), 
                ("railway", railway), 
                ("waterway", waterway), 
                ("name_en", name_en), 
                ("lanes", lanes), 
                ("service", service), 
                ("horse", horse), 
                ("public_transport", public_transport), 
                ("int_name", int_name), 
                ("junction", junction), 
                ("tunnel", tunnel), 
                ("name_zh_pinyin", name_zh_pinyin), 
                ("name_zh", name_zh),
                ("name_fr", name_fr), 
                ("alt_name", alt_name), 
                ("name_zh_classical", name_zh_classical), 
                ("toll", toll), 
                ("lit", lit)])
                                
                        
                # process each highway , consider a highway as a simple
                # path on the graph
                for node in highway.findall("./nd"):
                        if start_way == 0:
                                start_way = 1
                                bef_id = node.get('ref')
                                try:
                                        node_way[bef_id].append(way_id)
                                except:
                                        continue
                                
                                
                        cur_id = node.get('ref')
                        try:
                                node_way[cur_id].append(way_id)
                        except:
                                continue

                        # did not check how these nodes are missing in nodes list
                        if not(gr.has_node(int(bef_id))):
                                missed_nodes_count = missed_nodes_count + 1
                                gr.add_node(int(bef_id), attrs=[("coord","n")])
                                
                        if not(gr.has_node(int(cur_id))):
                                missed_nodes_count = missed_nodes_count + 1
                                gr.add_node(int(cur_id), attrs=[("coord","n")])
                                                
                        if not(gr.has_edge((int(bef_id), int(cur_id)))):
                                gr.add_edge((int(bef_id), int(cur_id)), wt=-1, label='', attrs='')
                        
                        
                        try:
                                # distance of the edge init to zero
                                adj_list[cur_id][bef_id] = 0
                                adj_list[bef_id][cur_id] = 0
                        
                                #init the point count for this edge 
                                edge_count[cur_id][bef_id] = 0
                                edge_count[bef_id][cur_id] = 0

                                #store edge type as a string
                                edge_tags[cur_id][bef_id] = way_type
                                edge_tags[bef_id][cur_id] = way_type

                                #add edge to a edge list
                                bef_id_int = int(bef_id)
                                cur_id_int = int(cur_id)

                                #create key
                                if bef_id_int < cur_id_int:
                                        #swap the values
                                        edge_key = bef_id + "," + cur_id
                                else:
                                        edge_key = cur_id + "," + bef_id
                                
                                # keep edges as a map, make sure no duplicates        
                                edge_list[edge_key] = [edge_id, way_features]
                                inv_edge_list[edge_id] = edge_key
                                edge_id = edge_id + 1
                                
                                #store cur_id before next iteration
                                bef_id = cur_id
                        except:
                                continue

        print len(inv_edge_list)
        print("missed nodes count:" + str(missed_nodes_count))
        print "way count : " + str(way_count)



def create_edge_rtree(edge_list, file_name, node_vector):

        edge_index_3d = index.Rtree('edge_index_3d_'+file_name,properties=p)

        for edge_id in edge_list:
                [end0, end1] = edge_id.split(',')
                               
                edge_index_3d.insert(edge_list[edge_id][0],(mbr_min[0], mbr_min[1], mbr_min[2],
                                              mbr_max[0], mbr_max[1], mbr_max[2]))    

        print "edge tree created"

def create_edge_rtree_graph(gr, file_name, node_vector, edge_list):

        edge_index_3d = index.Rtree('edge_index_3d_'+file_name,properties=p)
        
        for edge in gr.edges():
                e = Edge(int(edge[0]),int(edge[1]),-1,-1, -1, "-1", -1,-1)
                at0 = gr.node_attributes(edge[0])
                at1 = gr.node_attributes(edge[1])
                #e_attrs = gr.edge_attributes(edge)
                
                if at0[0][1]=="y" and at1[0][1] == "y":
                        edge_index_3d.insert(int(edge_list[e.edge_label_str][0]),(mbr_min[0], mbr_min[1], mbr_min[2], mbr_max[0], mbr_max[1], mbr_max[2]),int(edge_list[e.edge_label_str][0]))    

        print "edge tree created"  

# after get_ways to fill adjacency list with distances
def fill_adj_list_with_edge_lengths(adj_list, node_lat_array, node_lon_array, gr):

        start_flag = 0
        print(str(len(adj_list)))
        for edge in gr.edges():
                w = gr.edge_weight(edge)
                if w==-1:
                        at0 = gr.node_attributes(edge[0])
                        at1 = gr.node_attributes(edge[1])
                        
                        if at0[0][1]=="y" and at1[0][1] == "y":
                                d=distance_geodetic(node_lat_array[str(edge[0])], node_lon_array[str(edge[0])],
                                node_lat_array[str(edge[1])], node_lon_array[str(edge[1])])
                                adj_list[str(edge[0])][str(edge[1])] = d # meters
                                adj_list[str(edge[1])][str(edge[0])] = d # meters
                                w = d
                                gr.set_edge_weight(edge,wt=round(w,3))
                        else:
                                continue
                
   
                
        print("adj list filled")        

        
def parse_map(map_root_osm, file_name, node_lat_array, node_lon_array, node_list,
              adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list, gr):

        get_nodes(map_root_osm, node_list, adj_list, edge_count, node_way,
               edge_tags, node_lat_array, node_lon_array, node_vector, gr)

        fill_node_vector(node_lat_array, node_lon_array, node_vector, gr)
                     
        get_ways(map_root_osm, node_way, adj_list, edge_count, edge_tags, edge_list, inv_edge_list, gr)

        fill_adj_list_with_edge_lengths(adj_list, node_lat_array, node_lon_array, gr)

        #insert all edges into a serialized R-tree
        #create_edge_rtree(edge_list, file_name, node_vector)
        create_edge_rtree_graph(gr, file_name, node_vector, edge_list)
 

        print len(inv_edge_list)
        
        
#this method shows how to call parse map
def define_types():

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
        parse_map(map_root_osm, file_name, node_lat_array, node_lon_array, node_list,
              adj_list, node_way, edge_count, edge_tags, node_vector, edge_list, inv_edge_list)
