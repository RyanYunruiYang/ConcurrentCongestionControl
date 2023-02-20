import numpy as np

class Network:
    def __init__(self, nodes, links = [], pipes = [], incidence_matrix = [], tunnels= []):
        self.nodes = nodes
        self.links = links
        self.pipes = pipes
        self.incidence_matrix = incidence_matrix
        self.tunnels = tunnels
        
        self.active_links = []
        self.active_pipes = []
        self.active_mat = -1
        self.num_links = 0
        self.num_pipes = 0


    def activate_active_lists(self):
        self.active_links = [True for i in range(len(self.links))]
        self.active_pipes = [True for i in range(len(self.pipes))]


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
    

    def update_links(self): #update throughput
        for l in range(self.num_links):
            total_throughput, total_con, total_active_con = 0, 0, 0
            for p in range(self.num_pipes):
                num = self.incidence_matrix[l][p] * self.pipes[p].num_connections
                total_throughput += num * self.pipes[p].tput
                total_con += num
                total_active_con += num * self.active_pipes[p] #multiples by 1 if active, 0 if dead

            self.links[l].total_throughput = total_throughput
            self.links[l].total_con = total_con
            self.links[l].total_active_con = total_active_con


    def show_inc_matrix(self): #showing the incidence matrix (each row is a link's vector)
        print("inc mat:")
        for row in self.incidence_matrix:
            print(row)

    def init_actives(self):
        self.active_mat = self.incidence_matrix

    def show_active_mat(self):
        print("active mat:")
        for row in self.active_mat:
            print(row)
    
    def print_network(self, abridged=False):
        for l in range(len(self.links)): # a lot of printing
            print(self.links[l])
            print(f"total usage so far: {self.links[l].total_throughput} on {l} through {self.links[l].total_active_con}/{self.links[l].total_con} connections")

            if(not abridged):
                print("total pipes:")
                for p in range(self.num_pipes):
                    if(self.incidence_matrix[l][p]==1):
                        print(self.pipes[p])
            print()
            # print("active pipes")
            # for p in range(self.num_pipes):
            #     if(self.active_mat[l][p]==1 and self.pipes[p].active):
            #         print(self.pipes[p])
        if(not abridged):
            print(self.active_links)
            print(self.active_pipes)        

class Link:
    def __init__(self, index, capacity, start, stop, total_throughput = 0): #, pipes_active = [] 
        self.index = index
        self.capacity = capacity
        self.start = start
        self.stop = stop
        self.total_throughput = total_throughput
        self.total_links = 0
        self.total_active_con = 0
        # self.pipes_active = pipes_active #was too buggy. screw this list.
    def __str__(self):
        return f"link {self.index} (cap: {self.capacity}, from {self.start} to {self.stop})"
    
class Tunnel: #pipes travelling along the same path
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

class Pipe:
    def __init__(self, index, src, dst, path, num_connections=0,tput=0, tunnel_index=-1):
        # self.active = True
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


def naive_water_filling(network1, tcp_ass, printing=False):
    for p in range(len(network1.pipes)):
        network1.pipes[p].num_connections = tcp_ass[p]

    network1.init_actives()
    if(printing):
        network1.show_active_mat()

    while(sum(network1.active_links)>0 and sum(network1.active_pipes)>0):
        network1.update_links() #updates link values for total number of connections, tput, and active conn
        if(printing):
            network1.print_network()

        legal_jumps = []
        min_jump = (10000,-1)
        for l in range(len(network1.links)): #actual code
            if(network1.active_links[l]): #if the link is active
                link = network1.links[l]
                total_legal_jump = link.capacity - link.total_throughput
                legal_jump = total_legal_jump / link.total_active_con #maximum capacity we can add
                legal_jumps.append(legal_jump)

                if(legal_jump < min_jump[0]):
                    min_jump = (legal_jump, l)
        
        #add the throughputs
        network1.active_links[min_jump[1]] = False #deactivate link
        for p in range(len(network1.pipes)): #update throughputs
            if(network1.active_pipes[p]):
                network1.pipes[p].tput+=min_jump[0]
                #deactivate pipes                
                if(network1.incidence_matrix[min_jump[1]][p]==1):
                    network1.active_pipes[p] = False
        
        if(printing):
            print(legal_jumps)
            print(min_jump)
            print("-------one round done------")
    
    print("The final configuration is")
    network1.update_links()
    network1.print_network(True) #abridged=True

    print("\n ------ \n So the final mapping is")
    print(tcp_ass)
    print("to")
    print([p.tput for p in network1.pipes])
    return [p.tput for p in network1.pipes]



    
def main():
    network1 = Network([0,1,2,3]) #, [link1, link2, link3],[pipe1, pipe2] 

    network1.add_link(Link(0,10,0,1))
    network1.add_link(Link(1,20,1,2))
    network1.add_link(Link(2,14,2,3))

    network1.add_pipe(Pipe(0,0,2,[0,1]))#index 0, src 0, dst 2, path [1,2], connections=1
    network1.add_pipe(Pipe(1,1,3,[1,2]))

    network1.activate_active_lists()
    network1.show_inc_matrix()


    print("\n waterfilling \n")
    naive_water_filling(network1, [100,1])



if __name__ == "__main__":
    main()
