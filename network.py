class Network:
    def __init__(self, nodes, links = [], pipes = [], tunnels= []):
        self.nodes = nodes
        self.links = links
        self.pipes = pipes
        self.tunnels = tunnels
    
    def add_link(self, new_link):
        self.links.append(new_link)
    
    def add_pipe(self, new_pipe):
        self.pipes.append(new_pipe)
        for l in new_pipe.path:
            link = self.links[l]
            link.add_pipe("pipe ") #new_pipe

class Link:
    def __init__(self, index, capacity, start, stop, total_throughput = 0, pipes_total = [], pipes_active = []):
        self.index = index
        self.capacity = capacity
        self.start = start
        self.stop = stop
        self.total_throughput = total_throughput
        self.pipes_total = pipes_total
        self.pipes_active = pipes_active
    def __str__(self):
        return f"cap: {self.capacity}, from {self.start} to {self.stop}"
    
    def add_pipe(self, new_pipe):
        self.pipes_total.append(new_pipe)
        self.pipes_active.append(new_pipe)


class Tunnel: #pipes travelling along the same path
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

class Pipe:
    def __init__(self, src, dst, path, num_connections=0,tput=0, tunnel_index=-1):
        self.src = src
        self.dst = dst
        self.path = path
        self.tput = tput
        self.tunnel_index = tunnel_index
        self.num_connections = num_connections
    
    def links_passed():
        return []

    def __str__(self):
        return f"src: {self.src}, dst: {self.dst}, {self.num_connections} connections at {self.tput} each"


def naive_water_filling(network1):
    for k in range(len(network1.pipes)):
        print(network1.pipes[k])

    for l in range(len(network1.links)):
        print(f"\n link {l}")
        print(network1.links[l])
        print(f"total usage so far: {network1.links[l].total_throughput} on {network1.links[l].index} = {l}")
        print("active pipes:")
        print(len(network1.links[l].pipes_total))
        for p in network1.links[l].pipes_total:
            print(p)
        # # print(link.pipes_active[0])
        # cur_active = sum([pipe.num_connections for pipe in link.pipes_active])
        # print(f"total number of connections: {cur_active}")
        # print(f"legal jump: {(link.capacity - link.total_throughput)/(cur_active) }")
    
def main():
    network1 = Network([0,1,2,3]) #, [link1, link2, link3],[pipe1, pipe2] 

    network1.add_link(Link(0,10,0,1))
    network1.add_link(Link(1,20,1,2))
    network1.add_link(Link(2,15,2,3))

    network1.add_pipe(Pipe(0,2,[0,1],1))
    # network1.add_pipe(Pipe(1,3,[1,2],3))

    print("\n waterfilling \n")
    naive_water_filling(network1)



if __name__ == "__main__":
    main()
