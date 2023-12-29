#land_generator.py
#Written by Zach Girouard

#import modules
import numpy as np
import time
import random
import os

#set size of matrix, 4 corners, and random offset
size = 33 
ESC = "\x1b"
land = np.full((size,size),'11', dtype=int)
land[0][0] = random.randint(0,60) 
land[0][size - 1] = random.randint(0,60)
land[size - 1][size - 1] = random.randint(0,60) 
land[size - 1][0] = random.randint(0,60)
random_offset = random.randint(-6,8)
finished = False

#prints array with corrosponding colors to the values in the matrix
def printArray(size):
    global finished
    for x in range(size):
        for y in range(size):
            #WATER
            if land[y][x] <= 15:
                print(ESC + '[44;1m' + ".'.", end='')

            #BEACH
            elif 15 < land[y][x] <= 30:
                print(ESC + '[43;1m' + ".'.", end='')

            #GRASS
            elif 30 < land[y][x] <= 45:
                print(ESC + '[42;1m' + ".'.", end='')

            #SNOW
            elif 45 < land[y][x] <= 60:
                print(ESC + '[47;1m' + ".'.", end='')

    print()
    time.sleep(0.01)
    if finished == False:
        os.system('cls')
    else:
        time.sleep(1)

#Use four corners to iterate through the matrix and fill in corrosponding values
def recur(top_left, top_right, bottom_left, bottom_right, depth):
    #base case
    if depth > 4:
        return depth

    else:
        #get x and y coordinates for all four corners
        top_left_y = top_left[0]
        top_left_x = top_left[1]

        top_right_y = top_right[0]
        top_right_x = top_right[1]
        
        bottom_right_y = bottom_right[0]
        bottom_right_x = bottom_right[1]
        
        bottom_left_y = bottom_left[0]
        bottom_left_x = bottom_left[1]
        
        #use corner coordinates to get center coordinates
        center_x = int(((top_left_x + top_right_x) / 2))
        center_y = int(((top_left_y + bottom_left_y) / 2))

        #set center equal to the values of the four corners (x-step)
        center_value = int((((land[top_right] + land[top_left] + land[bottom_left] + land[bottom_right]) / 4) + random_offset))
        land[center_y, center_x] = center_value

        #get the values of the top middle, bottom middle, left middle, and right middle (+-step)
        top_middle_value = int((((land[top_right] + land[top_left] + center_value) / 3) + random_offset))
        bottom_middle_value = int((((land[bottom_right] + land[bottom_left] + center_value) / 3) + random_offset))
        left_middle_value = int((((land[top_left] + land[bottom_left] + center_value) / 3) + random_offset))
        right_middle_value = int((((land[top_right] + land[bottom_right] + center_value) / 3) + random_offset))

        #set the values of the top middle, bottom middle, left middle, and right middle (+-step)
        land[top_left_y, int(((top_left_x + top_right_x) / 2))] = top_middle_value   
        land[bottom_left_y, int(((bottom_left_x + bottom_right_x) / 2))] = bottom_middle_value
        land[int(((top_left_y + bottom_left_y) / 2)), bottom_left_x] = left_middle_value
        land[int(((top_right_y + bottom_right_y) / 2)), bottom_right_x] = right_middle_value
        
        #print array after x-step and +-step
        printArray(size)

        #recur using different values for the four corners in order to fill in the matrix
        recur(top_left, (top_left_y, int(((top_left_x + top_right_x) / 2))), (int(((top_left_y + bottom_left_y) / 2)), bottom_left_x), (center_y, center_x), depth + 1)
        recur((top_left_y, int(((top_left_x + top_right_x) / 2))), top_right, (center_y, center_x), (int(((top_right_y + bottom_right_y) / 2)), bottom_right_x), depth + 1) 
        recur((int(((top_left_y + bottom_left_y) / 2)), bottom_left_x),  (center_y, center_x), bottom_left, (bottom_left_y, int(((bottom_left_x + bottom_right_x) / 2))), depth + 1)
        recur((center_y, center_x), (int(((top_right_y + bottom_right_y) / 2)), bottom_right_x), (bottom_left_y, int(((bottom_left_x + bottom_right_x) / 2))), bottom_right, depth + 1)

#initial call to recur function
recur((0,0), (0,size-1), (size - 1, 0), (size - 1, size - 1), 0)
finished = True      
printArray(size)
print(ESC + '[0m')