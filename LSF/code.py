from operator import itemgetter
import csv
import numpy as np
from numpy.linalg import inv
# Reading Facebook data from fb_data.csv
def read_FB_data():
    nodes = []										# "nodes" list that stores the list of unique friends (including self)
    with open('mutualfriends.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:							# For every row
            nodes.append(row[0])					# Column no 1
            nodes.append(row[1]) 					# Column no 2
        nodes_set = set(nodes)
        nodes = list(nodes_set)						# Unique list of people
        #print nodes
        #print len(nodes)
    i = 0
    data = {}										# Dictionary of people and their unique IDs (0,1,2 etc)
    for name in nodes:								# Populate the dictionary
        data[name] = i
        i = i + 1
    return data										# Return the dictionary



def construct_P_matrix(nodes):
    n = 550											# Size of actual P matrix
    #print nodes
    p_matrix = [[0 for i in xrange(n)] for i in xrange(n)]		# P Matrix declaration. All 0s    
    #print p_matrix
    with open('mutualfriends.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:							# For every row
            p_matrix[nodes[row[0]]][nodes[row[1]]] = 1
            p_matrix[nodes[row[1]]][nodes[row[0]]] = 1
    
    
    #print nodes
    #for row in p_matrix:
        #print row[0]
        #break
        #print "\n"
    #print p_matrix
    
    matrix = np.array(p_matrix,dtype='f')
    #print matrix
    #for row in matrix:
        #print row
    row_sums = [sum(row) for row in matrix]		    # Calculate row sums
    #print row_sums                    
    
    for i in range(0,len(matrix[0])):				# Iterate through every row
        for j in range(0,len(matrix[0])):
            if matrix[i][j] == 1:
                matrix[i][j] = float(1)/row_sums[i]	# Calculate the probability
    
    #while i < len(p_matrix):
        #while j < len(p_matrix):
        #print matrix[i]
        #matrix[i][j] = p_matrix[i][j]
        #i = i+1
    
    #for row in matrix:
        #print row
        #print p_matrix[0]
        #break
        #print "\n"
        
    return matrix
 

# Split P matrix into dangling and non dangling part
def split_dangling_nodes(p_matrix):
    dangling_nodes_count = 0
    for row in p_matrix:
        dangling_node_value = 0
        if all(item == dangling_node_value for item in row):		# Check if a row is a dangling row         
            dangling_nodes_count = dangling_nodes_count + 1
            #dangling_row = row								
            #p_matrix.remove(row)					# Delete row from p_matrix
            #p_matrix.append(dangling_row)			# Append dangling row as last row of p_matrix
    n = len(p_matrix)
    #print dangling_nodes_count
    row_count = n - dangling_nodes_count					# Set n to len(p_matrix) - dangling_nodes_count         				
    #print row_count
    #print p_matrix
    p11 = p_matrix[0:row_count,0:row_count]
    				
    p12 = p_matrix[0:row_count,row_count:n]
    #print c               
    return p11,p12,dangling_nodes_count


def coefficient_matrix_calculation(p11,p12,p_matrix):
    identity_matrix = np.matrix(np.identity(len(p_matrix)))		# Identity Matrix
    #print identity_matrix
    #print len(p11)
    i11 = identity_matrix[0:len(p11),0:len(p11)]
    #alpha = 0.85
    alpha = 0.01
    alpha_p11_matrix = alpha * p11
    i11minus_alpha_p11 = i11 - alpha_p11_matrix
    #print i11minus_alpha_p11[0]
    return i11minus_alpha_p11



def matrix_inverse(i11minus_alpha_p11):
    return inv(i11minus_alpha_p11)


def calculate_pi1_t(inverse_i11minus_alpha_p11):
    
    v1_t = [1 for i in xrange(len(inverse_i11minus_alpha_p11))]
    #print v1_t
    #print len(v1_t)
    for i in xrange(len(v1_t)):
        v1_t[i] = float(v1_t[i])/len(v1_t)
    print v1_t
    return v1_t * inverse_i11minus_alpha_p11

def calculate_pi2_t(dangling_nodes_count,p12,pi1_t):
    v2_t = [1 for i in xrange(dangling_nodes_count)]
    #print v2_t
    #print len(v1_t)
    for i in xrange(len(v2_t)):
        v2_t[i] = 0.002
    #print v2_t
    pi1_t_p12 = pi1_t * p12
    #alpha_pi1_t_p12 = 0.85 * pi1_t_p12
    alpha_pi1_t_p12 = 0.01 * pi1_t_p12
    
    return v2_t + alpha_pi1_t_p12  
      

def include_dangling_nodes(p_matrix):
    new_p_matrix = [[0 for i in xrange(533)] for i in xrange(533)]		# P Matrix declaration. All 0s    
    np_matrix = np.array(new_p_matrix,dtype='f')
    np_matrix[:500,:500] = p_matrix
    return np_matrix  




nodes = read_FB_data()								# nodes -  dictionary with unique names with IDs
#print nodes
#print len(nodes)
#for k,v in nodes.items():
    #if v == 500:
        #print k, 'corresponds to', v

p_matrix = construct_P_matrix(nodes)				# Construct the P matrix
# Algorithm for solving
p11 , p12, dangling_nodes_count = split_dangling_nodes(p_matrix)			# Split matrix into dangling and non dangling nodes

'''
dangling_node = "d"
dangling_value = 0
key = n - dangling_nodes_count
#print key 
while dangling_value < dangling_nodes_count:		#Edit Dictionary so that it includes dangling nodes as well
    value = dangling_node + str(dangling_value)
    nodes[value] = key
    dangling_value = dangling_value +1
    key = key + 1

#for k,v in nodes.items():
    #if v >= 500:
        #print k, 'corresponds to', v

key = n - dangling_nodes_count						#Start from 500
list_of_nos = list(xrange(n))
print nodes
#print list_of_nos
for x in range(dangling_nodes_count):
    random_no = random.randint(0,499)
    #Swap with key
    print "Random number is :"+str(random_no)
    print "Key is :"+str(key)
    for k,v in nodes.items():
        if v == random_no:
            print k, 'corresponds to', v
        if v == key:
            print k, 'corresponds to', v

    for k,v in nodes.items():
        if v == random_no:
            nodes[k] = key
        if v == key:
            nodes[k] = random_no
        
    a, b = list_of_nos.index(random_no), list_of_nos.index(key)
    list_of_nos[b], list_of_nos[a] = list_of_nos[a], list_of_nos[b]
    #Increment key
    key = key+1
    #print list_of_nos
print list_of_nos
print nodes
new_order = list_of_nos
new_p_matrix = p_matrix[:, new_order][new_order]
#print new_p_matrix[0]
'''
#print p12

# Next Step, calculating I-alphaP11

i11minus_alpha_p11 = coefficient_matrix_calculation(p11,p12,p_matrix)
#print i11minus_alpha_p11 
inverse_i11minus_alpha_p11 = matrix_inverse(i11minus_alpha_p11)
#print inverse_i11minus_alpha_p11 

pi1_t = calculate_pi1_t(inverse_i11minus_alpha_p11)
pi2_t = calculate_pi2_t(dangling_nodes_count,p12,pi1_t)
#print pi1_t
#print pi2_t
pi_t = []
i = 0
for x in np.nditer(pi1_t):
    
    pi_t.append(float(x))
    i = i + 1
for x in np.nditer(pi2_t):
    pi_t.append(float(x))
    i = i + 1
#print pi_t

dangling_node = "d"
dangling_value = 0
key = 500
#print key 
while dangling_value < 50:		#Edit Dictionary so that it includes dangling nodes as well
    value = dangling_node + str(dangling_value)
    nodes[value] = key
    dangling_value = dangling_value +1
    key = key + 1

#print nodes

sorted_nodes = sorted(nodes.items(), key=itemgetter(1))
#print sorted_nodes
target = open("pi_t.txt", 'w')
for x in pi_t:
    target.write(str(x))
    target.write("\n")
target.close()

target = open("names.txt", 'w')
for x in sorted_nodes:
    target.write(x[0])
    target.write("	")
    target.write(str(x[1]))
    target.write("\n")

target.close()


