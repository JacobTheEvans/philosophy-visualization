import sys
sys.dont_write_bytecode = True
import dbase
import networkx as nx
import matplotlib.pyplot as plotter
import time

def graph(target):
    graph = nx.DiGraph()
    data = dbase.get_works()
    for i in data:
        for x in i.citations:
            graph.add_edge(i.name, x)


    nx.draw(graph, with_labels=True)
    nx.write_gexf(graph, "%s-graph.gexf" % target)

def main():
    print "[+] Starting Grapher"

    graph("Save_1")
    print "[+] Success Data Graph Has Been Saved"

if __name__ == "__main__":
    main()
