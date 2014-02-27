""" forest_m_candidate.py maintains candidate list for all points and logs """
__author__ = "Janaka Seneviratne"
__copyright__ = "Copyright 2014, Janaka Seneviratne"
__version__ = "0.0.1"
__maintainer__ = "Janaka Seneviratne"
__email__ = "janaka.seneviratne@gmail.com"
__status__ = "tested"

import os, sys
import xml.etree.ElementTree as ET
import numpy  
from rtree import index

import pickle, pprint
import time
import pylab
import pygraph

from vector_calc import *
from load_map import *
from Queue import *
#from pygraph.algorithms import *

edge_label = 0
m_gr = None
edge_list = None

flag = 0
#to hold edge info
class Edge:
	def __init__(self, node1, node2, count, weight, way_id, way_type, timestamp, road_name, name_en, lanes, oneway):
		self.node1 = node1
		self.node2 = node2
		self.count = count
		self.weight = weight
		self.way_id = way_id
		self.way_type = way_type
		self.timestamp = timestamp
		self.name = road_name
		self.name_en = name_en
		self.lanes = lanes 
		self.oneway = oneway
		self.get_edge_label()


	def get_edge_label(self):
		if self.node1 < self.node2:
			self.edge_label_str = str(self.node1) + "," + str(self.node2)
		else:
			self.edge_label_str = str(self.node2) + "," + str(self.node1)

#create a component
#traverse and print component
class Component:

	# init Component attributes
	# init edge attributes and add the edge to Components 
	def __init__(self, point, time_stamp, point_id, edge_list): # time as a count
		global point_label
		# point => is a tuple: (x,y,z)
		self.point = point
		# point_id assigned to identify the site
		self.point_id = point_id
		# last time this point was seen
		self.time = time_stamp
		self.point_count = 1

		self.edge_list = {}
                
		for i in edge_list:
                        self.edge_list[i] = edge_list[i];
		#self.edge_list[2] = e2;
		#self.edge_list[3] = e3;

			
	def add_point(self, point, time_stamp):
		if (time_stamp > self.time + 10):
			return -1;

		if self.point[0] == point[0] and self.point[1] == point[1] and self.point[2] == point[2]:
			self.point_count = self.point_count + 1;
			return 1;
		return -1;

	def print_point(self, lat_val, lon_val, path_log):
		path_log.write( str(lat_val) + "," + str(lon_val) + "\n" );
		#path_log.write( str(lat_val) + "," + str(lon_val) + "\n" );
		return

	def print_edge(self, edge_id, edge, forest_log):
		
		forest_log.write(str(self.point_id)
				 + ":" + str(edge_id)
				 + ":" + str(edge.node1)
				 + ":" + str(edge.node2)
				 + ":" + str(self.point_count)
				 + ":" + str(edge.weight)
				 + ":" + str(edge.way_id)
				 + ":" + str(edge.way_type.encode('utf-8'))
				 + ":" + str(edge.timestamp)
				 + ":" + str(edge.name)
				 + ":" + str(edge.name_en.encode('utf-8'))
				 + ":" + str(edge.lanes.encode('utf-8'))
				 + ":" + str(edge.oneway.encode('utf-8'))
				 + ":" + "\n" );
		return             


	# print edges into files
	def print_point_all(self, forest, point_candidate_log):
		log_point = "/home/logdir/" + str(self.point_id)+".txt"
		point_log = open(log_point,'w');
		
		self.print_point(float(self.point[4]), float(self.point[5]), point_log)
		
		for i in self.edge_list:
			#print("point_id:" + str(self.point_id) + "," + str(i))
			if isinstance(self.edge_list[i], Edge):
				#print(":"+str(i))
				self.print_edge_point(i, self.edge_list[i], forest, point_log)
				self.print_edge(i, self.edge_list[i], point_candidate_log)
		      
			       
		point_log.close()
		return
	
	def print_edge_point(self, edge_index, edge, forest, point_log):
		#print point
		
		# print edge
		if forest.node_latitude_array.has_key(str(edge.node1)):
                        self.print_point (float(forest.node_latitude_array[str(edge.node1)]) , float(forest.node_longitude_array[str(edge.node1)]) , point_log)
					
		if forest.node_latitude_array.has_key(str(edge.node2)):
                        self.print_point (float(forest.node_latitude_array[str(edge.node2)]) , float(forest.node_longitude_array[str(edge.node2)]) , point_log)
		
		return
			
class Forest:

	# init Forest attribs
	def __init__(self, node_lat_array, node_lon_array, map_gr):
		global edge_label 
		edge_label = 0
		self.node_latitude_array = node_lat_array
		self.node_longitude_array = node_lon_array
		self.map_gr = map_gr
		
		
		self.point_list = []
		self.time = 0
		self.point_id = 0
		
		
	def insert_forest(self, point, edge_list):
		inserted = False
				
		for p in self.point_list:
			ret = p.add_point(point, self.time)
			if ret == 1:
				inserted = True
				self.time = self.time + 1
				break

		if not(inserted):
			c = Component(point, self.time, self.point_id, edge_list)
			self.point_list.append(c)
			self.time = self.time + 1
			self.point_id = self.point_id + 1
		
	def print_forest(self, map_gr1, edge_list_in):
		global m_gr
		global edge_list
		m_gr = map_gr1
		edge_list = edge_list_in

		matrix_log_path = "/home/user/all_paths.txt"
		
		matrix_log = open(matrix_log_path,'w')

                for p in self.point_list:
			p.print_point_all(self, matrix_log)
		
						   
		matrix_log.close()
		return        
		
		

		

		
