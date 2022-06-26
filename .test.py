
if __name__=="__main__":
    from Pgraph.Pgraph import Pgraph
    import matplotlib.pyplot as plt
    import networkx as nx
    import os
    ### Prepare Network Structure #############
    G = nx.DiGraph()
    G.add_node("M1",type='product',flow_rate_lower_bound=100)
    G.add_node("M2",type='raw_material',price=200,flow_rate_lower_bound=1)
    G.add_node("M3",type='raw_material',price=100,flow_rate_lower_bound=2)
    G.add_node("O1",fix_cost=2000, proportional_cost=400)
    G.add_node("O2",fix_cost=1000, proportional_cost=400)
    G.add_edge("O1","M1", weight = 3) 
    G.add_edge("O2","M1", weight = 1) 
    G.add_edge("M2","O1", weight = 2)
    G.add_edge("M3","O2", weight = 4)
    ME=[["O1","O2"]]
    P=Pgraph(problem_network=G, mutual_exclusion=ME, solver="INSIDEOUT",max_sol=100)
    ax1=P.plot_problem()
    plt.show()
    P.run()
    total_sol_num=P.get_sol_num()
    for i in range(total_sol_num): #show all solutions in plot
        ax=P.plot_solution(sol_num=i)
        plt.show()
    
    P.to_studio(verbose=True)
    import platform
    print(platform.system()=="Windows")
    