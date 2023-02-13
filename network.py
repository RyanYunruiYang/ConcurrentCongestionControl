class Network:
    def __init__(self, nodes, links, pipes, tunnels=-1):
        self.nodes = nodes
        self.links = links
        self.pipes = pipes
        self.tunnels = tunnels

class Link:
    def __init__(self, capacity, start, stop, total_throughput = 0, pipes_total = [], pipes_active = []):
        self.capacity = capacity
        self.start = start
        self.stop = stop
        self.total_throughput = total_throughput
        self.pipes_total = pipes_total
        self.pipes_active = pipes_active

class Tunnel: #pipes travelling along the same path
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

class Pipe:
    def __init__(self, src, dst, tunnel_index=-1, num_connections=0):
        self.src = src
        self.dst = dst
        self.tunnel_index = tunnel_index
        self.num_connections = num_connections


def naive_water_filling():


def main():
    #doing two pipes for now - ryan (1pm)
    link1 = Link(capacity = 10, 0, 1)
    link2 = Link(capacity = 20, 1, 2)
    link3 = Link(capacity = 15, 2, 3)

    pipe1 = Pipe(0, 2)
    pipe2 = Pipe(1,3)
    network1 = Network([0,1,2,3], [link1, link2, link3],[pipe1, pipe2] )
    naive_water_filling(network1)



if __name__ == "__main__":
    main()
