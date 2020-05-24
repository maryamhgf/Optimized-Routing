#Phase 2 and Phase 3:
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from ortools.linear_solver import pywraplp
from skimage import draw
from skimage import io
from skimage.draw import line,ellipse
from PIL import Image, ImageDraw

#Function to display path on map( Phase 3): 
def display_path_on_map(path, pixel_position_x, pixel_position_y):
    im = Image.open('.\Project\map.png')
    draw = ImageDraw.Draw(im) 
    point=[]
    for i in range(len(path)):
       point.append(pixel_position_x[path[i]])
       point.append(pixel_position_y[path[i]])
    draw.line(point, fill = (256, 0, 0), width = 5)
    radius = 40
    draw.ellipse([pixel_position_x[path[0]] + radius/2, pixel_position_y[path[0]] + radius / 2, pixel_position_x[path[0]] - radius / 2,
            pixel_position_y[path[0]] - radius / 2], fill = (0,0,0))
    draw.ellipse([pixel_position_x[path[0]] + radius / 2, pixel_position_y[path[0]] + radius / 2, 
            pixel_position_x[path[0]] - radius / 2, pixel_position_y[path[0]] - radius / 2], fill = (0,0,0))
    draw.ellipse([pixel_position_x[path[len(path) - 1]] + radius / 2, pixel_position_y[path[len(path) - 1]] + radius / 2, 
            pixel_position_x[path[len(path) - 1]] - radius / 2, pixel_position_y[path[len(path) - 1]] - radius / 2], fill = (0,0,0))
    im.show()

#Read data from .csv file:
with open('.\Project\Information_CSV.csv') as file:
    data1 = csv.reader(file)
    data = list(data1)

#Store datas in lists:
node_names = []
node_neighbors = []
node_neighbors_weight = []
node_longitude = []
node_latitude = []
for r in range(1, len(data)):
    row = data[r]
    node_names.append(str(row[1]))
    node_longitude.append(float(row[2]))
    node_latitude.append(float(row[3]))
    node_neighbors.append(str(row[4]).split(","))
    node_neighbors_weight.append(str(row[5]).split(","))
for n in range(len(node_neighbors_weight)):
    node_neighbors_weight[n] = [int(i) for i in node_neighbors_weight[n]] 
    node_neighbors[n] = [int(i)-1 for i in node_neighbors[n]] 

#pixel positon of points on map:
pixel_position_x = [1517, 1461, 1449, 1273, 1252, 1072, 1325, 836, 823, 1139, 712, 689, 
    655, 631, 521, 289, 125, 45, 541, 150, 332]
pixel_position_y = [349, 255, 341, 305, 357, 279, 205, 485, 460, 180, 106, 233, 447, 
        568, 610, 689, 448, 221, 196, 219, 406]

#Edge and flatten edge matrix:
edge_matrix = []
f = []
edge_flat = []
node_number = len(node_names)
for i in range(node_number):
    temp_edge_matrix = []
    for j in range(node_number):
        if(j in node_neighbors[i]):
            temp_edge_matrix.append(1)
            edge_flat.append(1)
            f.append(node_neighbors_weight[i][node_neighbors[i].index(j)])
        else:
            temp_edge_matrix.append(0)
            edge_flat.append(0)
            f.append(0)
    edge_matrix.append(temp_edge_matrix)

    #Get the way user gives points:(by name or index(optional)):
    for i in range(len(node_names)):
        print(i+1,":", node_names[i])
    print("#########################")
while True:
    print("How do you like to enter start and end point? please enter 'index' or 'name'-> without sapce")
    print("Enter 'Quit' if you are done looking for directions.")
    option = input()
    #Get staring and end point:
    if(option == 'name'):
        print("enter starting place")
        start = node_names.index(input())
        print("enter destination place")
        end = node_names.index(input())
    elif(option == 'index'):
        print("enter starting index")
        start = int(input()) - 1
        print("enter destination index")
        end = int(input()) - 1
        
        if( start > len(node_names)-1 or end > len(node_names)-1 or start < 0 or end < 0):  
            print(start)   
            print("Index out of range")
            continue
        

    elif(option == 'Quit'):
        print("Have a nice trip:)")
        break
    else:
        print("!!!error entering your choice!!!")
        continue

    #variables' coefficients in constraints:
    A_eq = []
    B_eq = []
    for p in range(node_number):
        row=np.zeros((1, node_number ** 2))
        for i in range(node_number):
            row[0][i * 21 + p] = 1
        for i in range(node_number):
            row[0][p * 21 + i] = -1
        if(p != start and p != end):
            B_eq.append(0)
        elif(p == start):
            B_eq.append(1)
        elif(p == end):
            B_eq.append(-1)
        A_eq.append(row[0])

    solver = pywraplp.Solver('simple_mip_program',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    infinity = solver.infinity()
    var = []
    var_names = []

    #Defining variables:
    for  i in range(node_number * node_number):
        var_names.append(['x' + str(i)])
        if(edge_flat[i]):
            var.append(solver.IntVar(0.0, 1, 'x'+str(i)))
        else:
            var.append(solver.IntVar(0.0, 0, 'x'+str(i)))

    #Defining constraints:
    for i in range(len(A_eq)):
        condition = 0*var[0]
        for j in range(len(A_eq[i])):
            condition = condition + float(A_eq[i][j]) * var[j]
        solver.Add(condition <= B_eq[i])
        solver.Add(condition >= B_eq[i])
    condition = 0 * var[0]

    #Defining J and solving optimization:
    for j in range(len(f)):
        condition = condition + float(f[j]) * var[j]
    solver.Minimize(condition)
    result_status = solver.Solve()

    #Showing path and some information about path to user:
    print('path:')
    output = []
    point = start
    path = []
    while (point != end):
        for i in range(node_number):
            if( var[i * 21 + point].solution_value() == 1):
                path.append(point)
                print(point + 1, node_names[point])
                point = i
    print(end + 1, node_names[point])
    path.append(point)
    print("Needed time for the suggested path is: ", solver.Objective().Value())
    print(path)
    print("The path on map will appear few seconds later...please wait.")

    #Display path:
    display_path_on_map(path, pixel_position_x, pixel_position_y)
    print("####################")