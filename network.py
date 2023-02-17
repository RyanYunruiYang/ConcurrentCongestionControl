import numpy as np

class Network:
    def __init__(self, nodes, links = [], pipes = [], incidence_matrix = [], tunnels= []):
        self.nodes = nodes
        self.links = links
        self.pipes = pipes
        self.incidence_matrix = incidence_matrix
        self.tunnels = tunnels
        self.num_links = 0
        self.num_pipes = 0

    def show_inc_matrix(self): #showing the incidence matrix (each row is a link's vector)
        for row in self.incidence_matrix:
            print(row)

    def add_link(self, new_link):
        self.num_links +=1 #one more link
        self.links.append(new_link) #adding link to list of links
        self.incidence_matrix.append([]) #adding row to inc_matrix
    
    def add_pipe(self, new_pipe):
        self.num_pipes +=1 # one more pipe
        self.pipes.append(new_pipe)
        for l in range(self.num_links):
            if(l in new_pipe.path): #if it's on the path, add a 1
                self.incidence_matrix[l].append(1)
            else: #if it's not, add 0!
                self.incidence_matrix[l].append(0)
    
    def update_links(self):
        for l in range(self.num_links):
            #first, update throughputs
            total_throughput = 0
            total_links = 0
            for p in range(self.num_pipes):
                total_throughput += self.incidence_matrix[l][p] * self.pipes[p].tput
                total_links += self.incidence_matrix[l][p] * self.pipes[p].num_connections

            self.links[l].total_throughput = total_throughput
            self.links[l].total_links = total_links
class Link:
    def __init__(self, index, capacity, start, stop, total_throughput = 0, pipes_active = []):
        self.index = index
        self.capacity = capacity
        self.start = start
        self.stop = stop
        self.total_throughput = total_throughput
        self.pipes_active = pipes_active
    def __str__(self):
        return f"link {self.index} (cap: {self.capacity}, from {self.start} to {self.stop})"
    

class Tunnel: #pipes travelling along the same path
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

class Pipe:
    def __init__(self, index, src, dst, path, num_connections=0,tput=0, tunnel_index=-1):
        self.active = True
        self.index = index
        self.src = src
        self.dst = dst
        self.path = path
        self.tput = tput
        self.tunnel_index = tunnel_index
        self.num_connections = num_connections
    # def links_passed():
    #     return []
    def __str__(self):
        return f"src: {self.src}, dst: {self.dst}, {self.num_connections} connections at {self.tput} each"


def naive_water_filling(network1):
    network1.update_links() #updates link values for total number of connections, tput, and active conn

    for k in range(len(network1.pipes)):
        print(network1.pipes[k])

    for l in range(len(network1.links)):
        print("\n")
        print(network1.links[l])
        print(f"total usage so far: {network1.links[l].total_throughput} on {l} through {network1.links[l].total_links} connections")
        print("active pipes:")
        for p in range(network1.num_pipes):
            if(network1.incidence_matrix[l][p]==1):
                print(network1.pipes[p])



        # # print(link.pipes_active[0])
        # cur_active = sum([pipe.num_connections for pipe in link.pipes_active])
        # print(f"total number of connections: {cur_active}")
        # print(f"legal jump: {(link.capacity - link.total_throughput)/(cur_active) }")
    
def main():
    network1 = Network([0,1,2,3]) #, [link1, link2, link3],[pipe1, pipe2] 

    network1.add_link(Link(0,10,0,1))
    network1.add_link(Link(1,20,1,2))
    network1.add_link(Link(2,15,2,3))

    network1.add_pipe(Pipe(0,0,2,[0,1],1))#index 0, src 0, dst 2, path [1,2], connections=1
    network1.add_pipe(Pipe(1,1,3,[1,2],3))

    network1.show_inc_matrix()


    print("\n waterfilling \n")
    naive_water_filling(network1)



if __name__ == "__main__":
    main()
