/* 

***************************

you have to edit your own path about the maze.txt 

***************************

*/

import math

direction = [[1,0],[-1,0],[0,1],[0,-1]]

def is_inside(y,x,numbers):
    if y>=1 and y < len(numbers) and x>=0 and x < len(numbers[1]) :
        return 1
    return 0

def print_maze(numbers,visited,visited_1,s):
    end_x=0
    for i in visited_1[len(visited_1)-1] :
        if i == 0 :
           end_x = end_x +1
        else : break
    cur_y = len(visited_1)-1
    cur_x = end_x
    tmp=1
    
    while tmp == 1 :
        tmp = 0
        for i in range(0,4):
            next_y = cur_y + direction[i][0]
            next_x = cur_x + direction[i][1]
            
            if is_inside(next_y,next_x,numbers) and visited_1[next_y][next_x] == visited_1[cur_y][cur_x] -1:
                cur_y = next_y
                cur_x = next_x
                numbers[cur_y][cur_x] = 5
                tmp=1
   
    while True :
        for i in range(0,4):
            next_y = cur_y + direction[i][0]
            next_x = cur_x + direction[i][1] 
            
            if is_inside(next_y,next_x,numbers) and visited[next_y][next_x] == visited[cur_y][cur_x] -1 :
                cur_y = next_y
                cur_x = next_x
                numbers[cur_y][cur_x] = 5
        if visited[cur_y][cur_x] == 2 :
            break
    
    time = 0
    for i in visited_1:
        for j in i:
            if j is not 0 :
                time = time +1
    for i in visited:
        for j in i:
            if j is not 0 :
                time = time +1
    numbers.pop(0) 
    with open(s, 'w') as file:
        for i in numbers:
            file.write(" ".join([str(j) for j in i]))
            file.write("\n")
        file.write("---")
        file.write("\n")
        file.write("length=")
        file.write(str(visited_1[len(visited_1)-1][end_x]-1))
        file.write("\n")
        file.write("time=")
        file.write(str(time))

def key_end_location(numbers):
    for i in range(1,len(numbers)):
        for j in range(0,len(numbers[1])):
            if numbers[i][j] == "6":
                a=i
                b=j
                break
    c=0
    for i in numbers[len(numbers) -1]:
            if i == "4" :
                break
            c = c+1
    return [a,b,c]

def heu(x,y,x1,y1):
    return math.sqrt((x1-x)*(x1-x) + (y1-y)*(y1-y))

def A_sup(x,y,sx,sy,x1,y1):
    return math.sqrt((y-sy)*(y-sy)+(x-sx)*(x-sx)) + heu(x,y,x1,y1)

def insert_heap(heap,i):
    if i == 0 :
        return heap
    if i%2 == 0:
       a=i-1
    else:
       a=i
    if heap[int(a/2)][2] > heap[i][2]:
        temp = heap[int(a/2)]
        heap[int(a/2)] = heap[i]
        heap[i] = temp
        heap = insert_heap(heap, int(a/2))
    
    return heap

def delete_heap(heap):
    heap[0] = heap[len(heap)-1]
    heap.pop(len(heap)-1)
    parent = 0
    child = 1
    
    while child <= len(heap)-1 : 
        if child < len(heap)-1 and heap[child][2] > heap[child+1][2] :
            child = child + 1
        if heap[parent][2] < heap[child][2] :
            break
        temp = heap[parent]
        heap[parent] = heap[child]
        heap[child] = temp
        parent = child
        child = child*2+1
    return heap

 
def first_floor():
    f = "/home/uchihe/2018_CSE4007_2013011640/assignment1/first_floor_input.txt"
    with open(f) as data:
        numbers = [[i for i in line.split()] for line in data.readlines()]
    cur_y=1 
    cur_x=numbers[1].index("3")
    sy=cur_y
    sx=cur_x
    key=0
    visited = [[0]*len(numbers[1]) for i in range(len(numbers))]  
    visited_1 = [[0]*len(numbers[1]) for i in range(len(numbers))]
    
    tmp=key_end_location(numbers)
    ky=tmp[0]
    kx=tmp[1]
    end_x=tmp[2]
   
    P_Queue = []
    P_Queue.append((cur_y,cur_x,A_sup(cur_x,cur_y,sx,sy,kx,ky)))
 
    visited[cur_y][cur_x] = 1

    while True:
        if not P_Queue : break
        a = P_Queue[0]
        P_Queue = delete_heap(P_Queue)
        cur_y = a[0]
        cur_x = a[1]

        if numbers[cur_y][cur_x] == "6":
            key = 1
            visited_1[cur_y][cur_x] = visited[cur_y][cur_x]
            while P_Queue:
                P_Queue.pop(0)

        if key == 1 and numbers[cur_y][cur_x] == "4":
            break

        for i in range(0,4):
            next_y = cur_y + direction[i][0]
            next_x = cur_x + direction[i][1]
      
            if key == 1 and is_inside(next_y,next_x,numbers) and visited_1[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1":
                visited_1[next_y][next_x] = visited_1[cur_y][cur_x]+1
                P_Queue.append((next_y,next_x,A_sup(next_x,next_y,kx,ky,end_x,len(numbers)-1)))
                P_Queue = insert_heap(P_Queue,len(P_Queue)-1)

            if key == 0 and is_inside(next_y,next_x,numbers) and visited[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1" :
                visited[next_y][next_x] = visited[cur_y][cur_x] + 1
                P_Queue.append((next_y,next_x,A_sup(next_x,next_y,sx,sy,kx,ky)))
                P_Queue = insert_heap(P_Queue,len(P_Queue)-1)

    print_maze(numbers,visited,visited_1,'first_floor_output.txt') 

def second_floor():
    i=1
    while True:
        if dfs(i) == 1:
            break
        else:
            i=i+1

def dfs(depth):
    f="/home/uchihe/2018_CSE4007_2013011640/assignment1/second_floor_input.txt"
    with open(f) as data:
        numbers = [[i for i in line.split()] for line in data.readlines()]
    cur_y=1 
    cur_x=numbers[1].index("3")
   
    visited = [[0]*len(numbers[1]) for i in range(len(numbers))]  
    visited_1 = [[0]*len(numbers[1]) for i in range(len(numbers))]

    Stack = []
    Stack.append((cur_y,cur_x))
    visited[cur_y][cur_x] = 1
    key = 0
    find = 0
    while True:
        if not Stack: break
        a = Stack.pop()
        
        cur_y = a[0]
        cur_x = a[1]
        
        if numbers[cur_y][cur_x] == "6": 
            key = 1
            visited_1[cur_y][cur_x] = visited[cur_y][cur_x]
            while Stack:
                Stack.pop(0)
 
        if key == 1 and numbers[cur_y][cur_x] == "4": 
            find = 1
            break
 
        if key == 1 :
            if visited_1[cur_y][cur_x]==depth : continue
        else:
            if visited[cur_y][cur_x] ==depth : continue
 
        for i in range(0,4):
            next_y = cur_y + direction[i][0]
            next_x = cur_x + direction[i][1]
               
            if key == 1 and is_inside(next_y,next_x,numbers) and visited_1[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1":
                visited_1[next_y][next_x] = visited_1[cur_y][cur_x]+1
                Stack.append((next_y,next_x))               
            if key == 0 and is_inside(next_y,next_x,numbers) and visited[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1" :
                visited[next_y][next_x] = visited[cur_y][cur_x] + 1
                Stack.append((next_y,next_x))
 
    if find == 0:
        return 0
    else :
        print_maze(numbers,visited,visited_1,'second_floor_output.txt')
        return 1

def third_floor():
    f="/home/uchihe/2018_CSE4007_2013011640/assignment1/third_floor_input.txt"
    with open(f) as data:
        numbers = [[i for i in line.split()] for line in data.readlines()]
    cur_y=1 
    cur_x=numbers[1].index("3")
    sy=cur_y
    sx=cur_x
    key=0
    visited = [[0]*len(numbers[1]) for i in range(len(numbers))]  
    visited_1 = [[0]*len(numbers[1]) for i in range(len(numbers))]
    
    tmp=key_end_location(numbers)
    ky=tmp[0]
    kx=tmp[1]
    end_x=tmp[2]
   
    P_Queue = []
    P_Queue.append((cur_y,cur_x,A_sup(cur_x,cur_y,sx,sy,kx,ky)))
 
    visited[cur_y][cur_x] = 1

    while True:
        if not P_Queue : break
        a = P_Queue[0]
        P_Queue = delete_heap(P_Queue)
        cur_y = a[0]
        cur_x = a[1]

        if numbers[cur_y][cur_x] == "6":
            key = 1
            visited_1[cur_y][cur_x] = visited[cur_y][cur_x]
            while P_Queue:
                P_Queue.pop(0)

        if key == 1 and numbers[cur_y][cur_x] == "4":
            break

        for i in range(0,4):
            next_y = cur_y + direction[i][0]
            next_x = cur_x + direction[i][1]
      
            if key == 1 and is_inside(next_y,next_x,numbers) and visited_1[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1":
                visited_1[next_y][next_x] = visited_1[cur_y][cur_x]+1
                P_Queue.append((next_y,next_x,A_sup(next_x,next_y,kx,ky,end_x,len(numbers)-1)))
                P_Queue = insert_heap(P_Queue,len(P_Queue)-1)

            if key == 0 and is_inside(next_y,next_x,numbers) and visited[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1" :
                visited[next_y][next_x] = visited[cur_y][cur_x] + 1
                P_Queue.append((next_y,next_x,A_sup(next_x,next_y,sx,sy,kx,ky)))
                P_Queue = insert_heap(P_Queue,len(P_Queue)-1)

    print_maze(numbers,visited,visited_1,'third_floor_output.txt')

def fourth_floor():
    f="/home/uchihe/2018_CSE4007_2013011640/assignment1/fourth_floor_input.txt"
    with open(f) as data:
        numbers = [[i for i in line.split()] for line in data.readlines()]
    cur_y=1 
    cur_x=numbers[1].index("3")
    sy=cur_y
    sx=cur_x
    key=0
    visited = [[0]*len(numbers[1]) for i in range(len(numbers))]  
    visited_1 = [[0]*len(numbers[1]) for i in range(len(numbers))]
    
    tmp=key_end_location(numbers)
    ky=tmp[0]
    kx=tmp[1]
    end_x=tmp[2]
   
    P_Queue = []
    P_Queue.append((cur_y,cur_x,A_sup(cur_x,cur_y,sx,sy,kx,ky)))
 
    visited[cur_y][cur_x] = 1

    while True:
        if not P_Queue : break
        a = P_Queue[0]
        P_Queue = delete_heap(P_Queue)
        cur_y = a[0]
        cur_x = a[1]

        if numbers[cur_y][cur_x] == "6":
            key = 1
            visited_1[cur_y][cur_x] = visited[cur_y][cur_x]
            while P_Queue:
                P_Queue.pop(0)

        if key == 1 and numbers[cur_y][cur_x] == "4":
            break

        for i in range(0,4):
            next_y = cur_y + direction[i][0]
            next_x = cur_x + direction[i][1]
      
            if key == 1 and is_inside(next_y,next_x,numbers) and visited_1[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1":
                visited_1[next_y][next_x] = visited_1[cur_y][cur_x]+1
                P_Queue.append((next_y,next_x,A_sup(next_x,next_y,kx,ky,end_x,len(numbers)-1)))
                P_Queue = insert_heap(P_Queue,len(P_Queue)-1)

            if key == 0 and is_inside(next_y,next_x,numbers) and visited[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1" :
                visited[next_y][next_x] = visited[cur_y][cur_x] + 1
                P_Queue.append((next_y,next_x,A_sup(next_x,next_y,sx,sy,kx,ky)))
                P_Queue = insert_heap(P_Queue,len(P_Queue)-1)

    print_maze(numbers,visited,visited_1,'fourth_floor_output.txt')

def fifth_floor():
    f="/home/uchihe/2018_CSE4007_2013011640/assignment1/fifth_floor_input.txt"
    with open(f) as data:
        numbers = [[i for i in line.split()] for line in data.readlines()]
    cur_y=1 
    cur_x=numbers[1].index("3")
    sy=cur_y
    sx=cur_x
    key=0
    visited = [[0]*len(numbers[1]) for i in range(len(numbers))]  
    visited_1 = [[0]*len(numbers[1]) for i in range(len(numbers))]
    
    tmp=key_end_location(numbers)
    ky=tmp[0]
    kx=tmp[1]
    end_x=tmp[2]
   
    P_Queue = []
    P_Queue.append((cur_y,cur_x,A_sup(cur_x,cur_y,sx,sy,kx,ky)))
 
    visited[cur_y][cur_x] = 1

    while True:
        if not P_Queue : break
        a = P_Queue[0]
        P_Queue = delete_heap(P_Queue)
        cur_y = a[0]
        cur_x = a[1]

        if numbers[cur_y][cur_x] == "6":
            key = 1
            visited_1[cur_y][cur_x] = visited[cur_y][cur_x]
            while P_Queue:
                P_Queue.pop(0)

        if key == 1 and numbers[cur_y][cur_x] == "4":
            break

        for i in range(0,4):
            next_y = cur_y + direction[i][0]
            next_x = cur_x + direction[i][1]
      
            if key == 1 and is_inside(next_y,next_x,numbers) and visited_1[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1":
                visited_1[next_y][next_x] = visited_1[cur_y][cur_x]+1
                P_Queue.append((next_y,next_x,A_sup(next_x,next_y,kx,ky,end_x,len(numbers)-1)))
                P_Queue = insert_heap(P_Queue,len(P_Queue)-1)

            if key == 0 and is_inside(next_y,next_x,numbers) and visited[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1" :
                visited[next_y][next_x] = visited[cur_y][cur_x] + 1
                P_Queue.append((next_y,next_x,A_sup(next_x,next_y,sx,sy,kx,ky)))
                P_Queue = insert_heap(P_Queue,len(P_Queue)-1)

    print_maze(numbers,visited,visited_1,'fifth_floor_output.txt')

def gbfs():
    f="/home/uchihe/2018_CSE4007_2013011640/assignment1/first_floor_input.txt"
    with open(f) as data:
        numbers = [[i for i in line.split()] for line in data.readlines()]
    cur_y=1 
    cur_x=numbers[1].index("3")
    key=0
    visited = [[0]*len(numbers[1]) for i in range(len(numbers))]  
    visited_1 = [[0]*len(numbers[1]) for i in range(len(numbers))]
    
    tmp=key_end_location(numbers)
    ky=tmp[0]
    kx=tmp[1]
    end_x=tmp[2]
   
    P_Queue = []
    P_Queue.append((cur_y,cur_x,heu(cur_x,cur_y,kx,ky)))
 
    visited[cur_y][cur_x] = 1

    while True:
       if not P_Queue : break
       a = P_Queue[0]
       P_Queue = delete_heap(P_Queue)
       cur_y = a[0]
       cur_x = a[1]
       if numbers[cur_y][cur_x] == "6":
           key = 1
           visited_1[cur_y][cur_x] = visited[cur_y][cur_x]
           while P_Queue:
               P_Queue.pop(0)


       if key == 1 and numbers[cur_y][cur_x] == "4":
           break

       for i in range(0,4):
           next_y = cur_y + direction[i][0]
           next_x = cur_x + direction[i][1]
      
           if key == 1 and is_inside(next_y,next_x,numbers) and visited_1[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1":
               visited_1[next_y][next_x] = visited_1[cur_y][cur_x]+1
               P_Queue.append((next_y,next_x,heu(next_x,next_y,end_x,len(numbers)-1)))
               P_Queue = insert_heap(P_Queue,len(P_Queue)-1)

           if key == 0 and is_inside(next_y,next_x,numbers) and visited[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1" :
               visited[next_y][next_x] = visited[cur_y][cur_x] + 1
               P_Queue.append((next_y,next_x,heu(next_x,next_y,kx,ky)))
               P_Queue = insert_heap(P_Queue,len(P_Queue)-1)

    print_maze(numbers,visited,visited_1,'gbfs_sample_output.txt')

def bfs():
    f="/home/uchihe/2018_CSE4007_2013011640/assignment1/first_floor_input.txt"
    with open(f) as data:
        numbers = [[i for i in line.split()] for line in data.readlines() ]

    visited = [[0]*len(numbers) for i in range(len(numbers))] 
    visited_1 = [[0]*len(numbers) for i in range(len(numbers))]
    cur_x = 1
    cur_y = 1
    key = 0
    Queue = []  
    Queue.append((cur_y,cur_x))

    visited[cur_y][cur_x] = 1
    
    while True:
        if not Queue: break

        cur_y = Queue[0][0]
        cur_x = Queue[0][1]
        Queue.pop(0)

        if numbers[cur_y][cur_x] == "6": 
            key = 1
            visited_1[cur_y][cur_x] = visited[cur_y][cur_x]
            while Queue :
                Queue.pop(0)

        if key == 1 and numbers[cur_y][cur_x] == "4":
            break
   
        for i in range(0,4):
            next_y = cur_y + direction[i][0]
            next_x = cur_x + direction[i][1]
            
            if key == 1 and is_inside(next_y,next_x,numbers) and visited_1[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1":
                visited_1[next_y][next_x] = visited_1[cur_y][cur_x] + 1
                Queue.append((next_y,next_x))
            elif key == 0 and is_inside(next_y,next_x,numbers) and visited[next_y][next_x] == 0 and numbers[next_y][next_x] is not "1" :
                visited[next_y][next_x] = visited[cur_y][cur_x] +1
                Queue.append((next_y,next_x))

    print_maze(numbers,visited,visited_1,'bfs_sample_output.txt')

first_floor()
second_floor()
third_floor()
fourth_floor()
fifth_floor()
