class Network:
    def __init__(self, nodes, links, tunnels, pipes):
        self.nodes = []
        self.links = []
        self.tunnels = []
        self.pipes = []

class Link:
    def __init__(self, capacity, total_throughput, pipes_total, pipes_active):
        self.capacity = capacity
        self.total_throughput = 0
        self.set_passing = []
        self.set_active = []

class Tunnel: #pipes travelling along the same path
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

class Pipe:
    def __init__(self, src, dst, tunnel_index, num_connections=0):
        self.src = src
        self.dst = dst
        self.tunnel_index = tunnel_index
        num_connections = 0