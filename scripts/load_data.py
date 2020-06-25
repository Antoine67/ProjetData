import numpy as np
from scipy.spatial import distance

def load_from(path):

    with open(path, 'r') as f:
        lines = list(map(lambda l: l.replace('\n', '').split(), f.readlines()))
        file_name = lines[0][2]
        
        
        capacity = int(lines[5][2])
        cities_nb = int(lines[3][2])
        
        vehicules_nb = int(file_name.split("k",1)[1]) 
        
        cities_coords = []
        
        
        cities = lines[7:]
        index = 0
        for i,line in enumerate(cities):
            if(line[0] == 'EOF' or line[0] == 'DEMAND_SECTION'):
                break;
            cities_coords.append(line)
            index = i
            
        demand_matrix = []   
        for line in cities[index+2:]:
            if(line[0] == 'EOF' or line[0] == 'DEPOT_SECTION'):
                break;
            demand_matrix.append(line[1])
            
        demand_matrix = np.array(demand_matrix).astype(np.int)
        return np.array(cities_coords), capacity, cities_nb, vehicules_nb, demand_matrix
            

def get_particular_info(path, string):
    with open(path, 'r') as f:
        lines = list(map(lambda l: l.replace('\n', '').split(), f.readlines()))
        for line in lines:
            if len(line) != 0 and string == line[0]:
                return int(line[-1])
        return None

def get_all_path(path):
    
    returnArray = []
    with open(path, 'r') as f:
        lines = list(map(lambda l: l.replace('\n', '').split(), f.readlines()))
        for line in lines:
            comboArray = []
            
            comboArray.append(line[0])
            comboArray.append(line[1])
            returnArray.append(comboArray)
        return returnArray
    
def get_data(cities_coords):
    length = len(cities_coords)
    adjacency_mat = np.zeros((length,length))
    cities_coords =  cities_coords.astype(np.int)
    for i, city in enumerate(cities_coords):
        #print(city)
        a = np.array([city[1],city[2]])
        for j in range(length):
            b =  np.array([cities_coords[j][1], cities_coords[j][2]])
            #dist = np.linalg.norm(a-b)
            dist = distance.euclidean(a, b)
            #print('A:',a,'B:',b,'out:',dist) 
            adjacency_mat[j][i] = dist
    #adjacency_mat = np.ceil(adjacency_mat)
    return adjacency_mat
            

            
def  from_file_to_adj_matr(path):
    cities_coords, capacity, cities_nb,vehicules_nb, demand_matrix = load_from(path)
    return get_data(cities_coords), capacity, cities_nb,vehicules_nb, demand_matrix, cities_coords 
               

if __name__ == '__main__':
    print(from_file_to_adj_matr('../data/A-VRP/A-n32-k5.vrp'))

