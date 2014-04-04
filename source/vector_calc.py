""" vector_calc.py """
__author__ = "Janaka Seneviratne"
__copyright__ = "Copyright 2014, Janaka Seneviratne"
__version__ = "0.0.1"
__maintainer__ = "Janaka Seneviratne"
__email__ = "janaka.seneviratne@gmail.com"
__status__ = "tested"

from numpy import power as pow, finfo, double
from numpy import degrees, radians, mat, cos, sin, arctan, sqrt, pi, arctan2 
import scipy
import matplotlib.pyplot
from visual import *
#from math import pow, degrees, radians
#from scipy import mat, cos, sin, arctan, sqrt, pi, arctan2


def cbrt(x):
    if x >= 0: 
        return   pow(x, 1.0/3.0)
    else:
        return -  pow( abs(x), 1.0/3.0)

# Constants defined by the World Geodetic System 1984 (WGS84)
a = 6378.137
b = 6356.7523142
esq = 6.69437999014 * 0.001
e1sq = 6.73949674228 * 0.001
f = 1 / 298.257223563


#   Calculate the line segment PaPb that is the shortest route between
#   two lines P1P2 (v1v2) and P3P4 (v3v4). Calculate also the values of mua and mub where
#      Pa = P1 + mua (P2 - P1)
#      Pb = P3 + mub (P4 - P3)
#   Return FALSE if no solution exists (parallel or coincident lines).
#  P1-v1 P2-v2 P3-v3 P4-v4 
def line_line_intersection(v1,v2,v3,v4):
	pa = []
	pb = []
	mua = 0.0
	mub = 0.0

	EPS =  finfo(double).eps
	#EPS = 00000000000000001 

	p13 = [(v1[0]-v3[0]),(v1[1]-v3[1]),(v1[2]-v3[2])]
	p43 = [(v4[0]-v3[0]),(v4[1]-v3[1]),(v4[2]-v3[2])]

	if  abs(p43[0]) < EPS and  abs(p43[1]) < EPS and  abs(p43[2]) < EPS:
		return []

	p21 = [(v2[0] - v1[0]), (v2[1] - v1[1]), (v2[2] - v1[2])]

	if  abs(p21[0]) < EPS and  abs(p21[1]) < EPS and  abs(p21[2]) < EPS:
		return []

	d1343 = p13[0]*p43[0] + p13[1]*p43[1] + p13[2]*p43[2]
	d4321 = p21[0]*p43[0] + p21[1]*p43[1] + p21[2]*p43[2]
	d1321 = p13[0]*p21[0] + p13[1]*p21[1] + p13[2]*p21[2]
	d4343 = p43[0]*p43[0] + p43[1]*p43[1] + p43[2]*p43[2]
	d2121 = p21[0]*p21[0] + p21[1]*p21[1] + p21[2]*p21[2]

	denom = d2121*d4343 - d4321*d4321

	if  abs(denom) < EPS:
		return []

	numer = d1343*d4321 - d1321*d4343

	mua = numer / denom
	mub = (d1343 + d4321*mua)/d4343

	pa = [(v1[0] + mua*p21[0]), (v1[1] + mua*p21[1]), (v1[2] + mua*p21[2])]
	pb = [(v3[0] + mua*p43[0]), (v3[1] + mua*p43[1]), (v3[2] + mua*p43[2])]

	return [pa, pb, mua, mub]
	
	

#projection of v1 on v2
def scalar_projection(v1,v2):
	return comp(v1,v2)

def shortest_dist_between_two_vectors(v1, v2, v3, v4):
	xp = cross((v2-v1),(v3-v4))
	n = xp/mag(xp)
	return dot((v1-v3),n)

def convert_geodetic_to_vector(pt):
	pt_c = geodetic_to_ECEF(pt[0],pt[1])
	return vector(pt_c[0],pt_c[1],pt_c[2])

def get_diff_angle(v1, v2, v3, v4):
	return  abs(diff_angle((v1-v2),(v3-v4)))

def get_mag(v1,v2):
	return mag(vector(v1[0], v1[1], v1[2])-vector(v2[0], v2[1], v2[2]))

def perpendicular_distance(v1, v2, v3):

	mg  = mag(v2 - v3)
	

	if dot(v2-v3,v1-v3) > 0 and dot(v3-v2,v1-v2) > 0:
		ang = 0
	else:
		ang = 1 
	if mg == 0:
		return [ang, 1000000]	
	return [ang, mag(cross((v2-v3),(v1-v3)))/mg]
		

def geodetic_to_ECEF_timestamp(lat,lon, timestamp):
	D2R =  pi/180;
	#meters
	a = 6378137.0 
	#first eccentricity squared 
	pow_e_2 = 6.69437999014*  pow(10,-3)
	#assume 0	
	h = 0 
	lat_rad = float(lat)*D2R;
	lon_rad = float(lon)*D2R;
	N = a/ sqrt(1-pow_e_2*  pow( sin(lat_rad),2))
	x = (N+h)* cos(lat_rad)* cos(lon_rad)
	y = (N+h)* cos(lat_rad)* sin(lon_rad)
	z = (N*(1-pow_e_2)+h)* sin(lat_rad)
	return [x,y,z, timestamp, lat, lon]

def geodetic_to_ECEF(lat,lon):
	D2R =  pi/180;
	#meters
	a = 6378137.0 
	#first eccentricity squared 
	pow_e_2 = 6.69437999014*  pow(10,-3)
	#assume 0	
	h = 0 
	lat_rad = float(lat)*D2R;
	lon_rad = float(lon)*D2R;
	N = a/ sqrt(1-pow_e_2*  pow( sin(lat_rad),2))
	x = (N+h)* cos(lat_rad)* cos(lon_rad)
	y = (N+h)* cos(lat_rad)* sin(lon_rad)
	z = (N*(1-pow_e_2)+h)* sin(lat_rad)
	return [x,y,z]


#
#https://code.google.com/p/pysatel/source/browse/trunk/coord.py?r=22
#
def geodetic2ecef(lat, lon, alt):
    """Convert geodetic coordinates to ECEF."""
    lat, lon = radians(lat), radians(lon)
    xi = sqrt(1 - esq * sin(lat))
    x = (a / xi + alt) * cos(lat) * cos(lon)
    y = (a / xi + alt) * cos(lat) * sin(lon)
    z = (a / xi * (1 - esq) + alt) * sin(lat)
    return x, y, z

#
#https://code.google.com/p/pysatel/source/browse/trunk/coord.py?r=22
#
def ecef2geodetic(x, y, z):
    """Convert ECEF coordinates to geodetic.
    J. Zhu, "Conversion of Earth-centered Earth-fixed coordinates \
    to geodetic coordinates," IEEE Transactions on Aerospace and \
    Electronic Systems, vol. 30, pp. 957-961, 1994."""
    r =  sqrt(x * x + y * y)
    Esq = a * a - b * b
    F = 54 * b * b * z * z
    G = r * r + (1 - esq) * z * z - esq * Esq
    C = (esq * esq * F * r * r) / (  pow(G, 3))
    S = cbrt(1 + C +  sqrt(C * C + 2 * C))
    P = F / (3 *   pow((S + 1 / S + 1), 2) * G * G)
    Q =  sqrt(1 + 2 * esq * esq * P)
    r_0 =  -(P * esq * r) / (1 + Q) +  sqrt(0.5 * a * a*(1 + 1.0 / Q) - \
	P * (1 - esq) * z * z / (Q * (1 + Q)) - 0.5 * P * r * r)
    U =  sqrt(  pow((r - esq * r_0), 2) + z * z)
    V =  sqrt(  pow((r - esq * r_0), 2) + (1 - esq) * z * z)
    Z_0 = b * b * z / (a * V)
    h = U * (1 - b * b / (a * V))
    lat =  arctan((z + e1sq * Z_0) / r)
    lon =  arctan2(y, x)
    return  degrees(lat),  degrees(lon)



def geodetic_to_ECEF_line(lat1,lon1,lat2,lon2):
	pt1 = geodetic_to_ECEF(lat1,lon1)
	pt2 = geodetic_to_ECEF(lat2,lon2)
	return [pt1,pt2]


def distance(node1,node2,lat_a, lon_a):
	lat1 = float(lat_a[node1])
	lat2 = float(lat_a[node2])
	lon1 = float(lon_a[node1])
	lon2 = float(lon_a[node2])

	RADIUS = 6371 #KM

	D2R =  pi/180;

	lat1_rad = lat1*D2R;
	lat2_rad = lat2*D2R;
	lon1_rad = lon1*D2R;
	lon2_rad = lon2*D2R;

	a =    pow( sin((lat1_rad-lat2_rad)/2),2) +  cos(lat1_rad)* cos(lat2_rad)*   pow( sin((lon1_rad-lon2_rad)/2),2);

	distance =  abs(2*RADIUS* arctan2( sqrt(a),  sqrt(1-a)));
	return distance*1000; #meter

def distance_geodetic(lat1,lon1,lat2,lon2):
	RADIUS = 6371 #KM

	D2R =  pi/180;

	lat1_rad = float(lat1)*D2R;
	lat2_rad = float(lat2)*D2R;
	lon1_rad = float(lon1)*D2R;
	lon2_rad = float(lon2)*D2R;

	a =    pow( sin((lat1_rad-lat2_rad)/2),2) +  cos(lat1_rad)* cos(lat2_rad)*  pow( sin((lon1_rad-lon2_rad)/2),2);

	distance =  abs(2*RADIUS* arctan2( sqrt(a),  sqrt(1-a)));
	return distance*1000; #meter

def edge_center(n1, n2):
        return [(n1[0]+n2[0])/2, (n1[1]+n2[1])/2, (n1[2]+n2[2])/2]

def distance(p1,p2):
        return sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2) + pow(p1[2]-p2[2],2) )


    
