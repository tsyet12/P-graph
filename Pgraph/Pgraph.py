import subprocess
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
from networkx.drawing.nx_pydot import pydot_layout
from lxml import etree
import networkx as nx

class Pgraph():
    def __init__(self, problem_network, mutual_exclusion, solver="INSIDEOUT",max_sol=100):
        self.G=problem_network
        self.ME=mutual_exclusion
        self.solver=solver
        self.max_sol=max_sol
        self.path=os.path.dirname(os.path.realpath(__file__))+r"/solver/"
        self.gmatlist=[]
        self.goplist=[]
        self.goolist=[]
    def plot_problem(self):
        G=self.G.copy()
        for n in G.nodes():
            if n[0]=="O":
                G.nodes[n]['s']=mpl.markers.MarkerStyle(marker='s', fillstyle='top')
            else:
                G.nodes[n]['s']='o'
        plt.rc('figure',figsize=(5,10))
        label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
        edges=G.edges()
        weights = [G[u][v]['weight'] for u,v in edges]
        labels = nx.get_edge_attributes(G,'weight')
        labels={k:round(v,2) for k,v in labels.items()}
        nodeShapes = set((aShape[1]["s"] for aShape in G.nodes(data = True)))
        pos=pydot_layout(G,prog='dot')
        pos2=pydot_layout(G,prog='dot')
        for key, (v1,v2) in pos2.items():
            if key[0]=="O":
                pos2[key]=(v1,v2-3)
        nx.draw(G, pos=pos, node_color='white',alpha=0.9,node_shape="o", edge_color='black', with_labels = True,node_size=3000,bbox=label_options,width=weights,font_size=12)
        for aShape in nodeShapes:
            nx.draw_networkx_nodes(G,pos=pos2,node_color='black',node_shape = aShape, nodelist = [sNode[0] for sNode in filter(lambda x: x[1]["s"]==aShape,G.nodes(data = True))],node_size=3000)
        nx.draw_networkx_edge_labels(G, pos=pos,edge_labels=labels)
        ax= plt.gca()
        plt.axis('off')
        ax.autoscale()
        ax.set_xlim([0.75*ax.get_xlim()[0],1.1*ax.get_xlim()[1]])
        ax.set_ylim([0.75*ax.get_ylim()[0],1.1*ax.get_ylim()[1]])
        return ax
    
    def convert_problem(self):
        G=self.G
        ME=self.ME
        path=self.path
        ### MAKE INPUT FILE #############
        prelines=[
        'file_type=PNS_problem_v1','\n',
        'file_name=Graph_1','\n',
        '\n',
        'measurement_units:','\n',
        'mass_unit=t','\n',
        'time_unit=y','\n',
        'money_unit=USD','\n',
        '\n',
        'defaults:','\n',
        'material_type=raw_material','\n',
        'material_flow_rate_lower_bound=0','\n',
        'material_flow_rate_upper_bound=10000','\n',
        'material_price=0','\n',
        'operating_unit_capacity_lower_bound=0','\n',
        'operating_unit_capacity_upper_bound=10000','\n',
        'operating_unit_fix_cost=0','\n',
        'operating_unit_proportional_cost=0','\n',
        '\n',
        'materials:','\n'
        ]

        for n in G.nodes():
            if n[0]=="M":
                add_list=[n+": "]
                for k,v in G.nodes[n].items():
                    if k=='type':
                        add_list[0]=add_list[0]+v
                    else:
                        add_list.append(str(k)+"="+str(v))
                n_=", ".join(add_list)
                prelines.append(n_)
                prelines.append('\n')

        prelines.append('\n')
        prelines.append('operating_units:')
        prelines.append('\n')

        for n in G.nodes():
            if n[0]=="O":        
                add_list=[n+": "]
                first=True
                for k,v in G.nodes[n].items():
                    if k=='type':
                        add_list[0]=add_list[0]+v
                    elif len(add_list)==1 and first:
                        add_list[0]=add_list[0]+str(k)+"="+str(v)
                        first=False
                    else:
                        add_list.append(str(k)+"="+str(v))
                n_=", ".join(add_list)
                prelines.append(n_)
                prelines.append('\n')

        prelines.append('\n')
        prelines.append('material_to_operating_unit_flow_rates:')
        prelines.append('\n')

        for n in G.nodes():
            if n[0]=="O": 
                add_str=n+": "
                for x1, x2 in G.in_edges(n):
                    add_str=add_str+str(G[x1][x2]["weight"])+" "+x1
                    add_str=add_str+" + "
                add_str=add_str[:-3]
                add_str=add_str+" => "
                for x1, x2 in G.out_edges(n):
                    add_str=add_str+str(G[x1][x2]["weight"])+" "+x2
                    add_str=add_str+" + "
                add_str=add_str[:-3]
                prelines.append(add_str)
                prelines.append("\n")
        if ME!=[]:
            prelines.append("\n")

        if ME !=[]:
            prelines.append("mutually_exlcusive_sets_of_operating_units:")
            prelines.append("\n")
        for i in range(len(ME)):
            MEstring="ME"+str(i)+": "
            for x in ME[i]:
                MEstring=MEstring+x+", "
            MEstring=MEstring[:-2]  
            prelines.append(MEstring)
            prelines.append("\n")
                
        prelines.append("\n")        
                
        with open(path+'input.in', 'w') as f:
            for line in prelines:
                f.write(line)

    def solve(self):
        ###RUN SOLVER##########
        '''
        Arguments:
        solver (int): 0:"MSG",1:"SSG",2:"SSGLP",3:"INSIDEOUT"
        max_sol (int): Maximum number of solutions from solver (default=100)
        '''
        path=self.path
        max_sol=self.max_sol
        solver=self.solver
        solver_dict={0:"MSG",1:"SSG",2:"SSGLP",3:"INSIDEOUT"}
        rc=subprocess.run([path+"pgraph_solver.exe",solver, path+"input.in", path+"test_out.out", str(max_sol)])
        ################
    
    def read_solution(self):
        path=self.path
        
        ### READ SOLUTION ##########
        #clean strings
        with open(path+"test_out.out","r") as f:
            lines = f.readlines()
        for i in range(len(lines)-1,0,-1):
            if lines[i][0]==" ":
                if lines[i-1][-3:]!="\n":
                    lines[i-1]=lines[i-1].strip()+" "+lines[i].strip()
                    lines[i]=""
                else:
                    lines[i-1]=lines[i-1][:-3].strip()+" "+lines[i].strip()
                    lines[i]=""
        lines=list(map(lambda x:x.strip(),lines))
        lines=list(filter(None, lines))
        mat_list=lines[1]
        op_list=lines[3]
        used_mat_list=lines[6] 

        #Find solutions
        sol_start_index=[]
        for i in range(len(lines)):
            if lines[i][:18]=="Feasible structure":
                sol_start_index.append(i)
                print(lines[i][19:-1])

        sol_start_index.append(len(lines)-1)

        sol_list=[]
        for i in range(1,len(sol_start_index)):
            sol_list.append(lines[sol_start_index[i-1]:sol_start_index[i]])

        comp=["Materials:","Operating units:","Total annual cost="]

        gmatlist=[]
        goplist=[]
        goolist=[]
        for i in range(len(sol_list)): #loop through solution number
            comp_ind=-1
            s=False
            
            tmatlist=[]
            toplist=[]
            for j in range(len(sol_list[i])):
                #print(sol_list[i][j])
                if sol_list[i][j][:len(comp[0])]==comp[0]:
                    comp_ind=0
                    s=True
                elif sol_list[i][j][:len(comp[1])]==comp[1]:   
                    comp_ind=1
                    s=True
                elif sol_list[i][j][:len(comp[2])]==comp[2]:   
                    comp_ind=2
                    s=True
                if s==False:
                    if comp_ind==0:
                        tlist=sol_list[i][j].replace('(',' ')
                        tlist=tlist.replace(')','')
                        tlist=tlist.split()
                        if tlist[0][-1]==":":
                            tlist[0]=tlist[0][:-1] #correct for semicolon  
                        if tlist[1]=="balanced": #correct for balanced
                            tlist=[tlist[0],0,0,0]
                        tmatlist.append(tlist)
                    elif comp_ind==1:
                        #print(sol_list[i][j])
                        glist=sol_list[i][j].split(')')
                        glist=glist[0].replace('*',' ')
                        glist=glist.replace('(', ' ')
                        glist=glist.split()
                        toplist.append(glist)
                if comp_ind==2:
                    print(sol_list[i][j])
                    goolist.append(sol_list[i][j].split()[3])
                s=False
            goplist.append(toplist)
            gmatlist.append(tmatlist)        
        self.goplist=goplist
        self.gmatlist=gmatlist
        self.goolist=goolist
    def plot_solution(self,sol_num=0):
        sol_num=sol_num
        H=self.G.copy()
        gmatlist=self.gmatlist
        goplist=self.goplist
        goolist=self.goolist  
        for n in H.nodes():
            if n[0]=="O":
                H.nodes[n]['s']=mpl.markers.MarkerStyle(marker='s', fillstyle='top')
            else:
                H.nodes[n]['s']='o'
        attr_op={x[1]:{"Capacity":x[0],"Cost":x[2]} for x in goplist[sol_num]}
        attr_mat={x[0]:{"Flow":x[3],"Cost":x[1]} for x in gmatlist[sol_num]}
        nx.set_node_attributes(H,attr_op)
        nx.set_node_attributes(H,attr_mat)
        plt.rc('figure',figsize=(5,10))
        label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
        edges=H.edges()
        weights = [H[u][v]['weight'] for u,v in edges]
        labels = nx.get_edge_attributes(H,'weight')
        labels={k:round(v,2) for k,v in labels.items()}
        labels_flow=nx.get_node_attributes(H,'Flow')
        labels_cap=nx.get_node_attributes(H,'Capacity')
        labels_cost=nx.get_node_attributes(H,'Cost')
        all_node=list(set(list(labels_flow.keys())+list(labels_cap.keys())+list(labels_cost.keys())))
        labels1={}
        for x in all_node:
            string=x
            if labels_flow.get(x) is not None:
                string=string+"\nFlow="+str(labels_flow.get(x))
            
            if labels_cap.get(x) is not None:
                string=string+"\nCap.="+str(labels_cap.get(x))
                
            if labels_cost.get(x) is not None:    
                string=string+"\nCost="+str(labels_cost.get(x))
            
            labels1.update({x:string})

        for e in H.edges():
            if e[0] in all_node and e[1] in all_node:
                H[e[0]][e[1]]['color']='black'
            else:
                H[e[0]][e[1]]['color']='lightgrey'
                
        for n in H.nodes():
            if n in all_node:
                H.nodes()[n]['color']='black'
            else:
                H.nodes()[n]['color']='lightgrey'
            if n[0]=='M':
                H.nodes()[n]['shape']='o'
            elif n[0]=='O':
                H.nodes()[n]['shape']='s'

        shape_list=[H.nodes()[n]['shape'] for n in H.nodes()]  
        node_color_list=[H.nodes()[n]['color'] for n in H.nodes()]        
        edge_color_list=[H[e[0]][e[1]]['color'] for e in H.edges()]    
        
        nodeShapes = set((aShape[1]["s"] for aShape in H.nodes(data = True)))

        pos=pydot_layout(H,prog='dot')
        pos2=pydot_layout(H,prog='dot')
        for key, (v1,v2) in pos2.items():
            if key[0]=="O":
                pos2[key]=(v1,v2-3)

            
        nx.draw(H, pos=pos,labels=labels1, node_color='white',alpha=0.9,node_shape='o', edge_color=edge_color_list, with_labels = True,node_size=3000,bbox=label_options,width=weights,font_size=10)
        for aShape in nodeShapes:
            node_list=[sNode[0] for sNode in filter(lambda x: x[1]["s"]==aShape,H.nodes(data = True))]
            for node in node_list:
                nx.draw_networkx_nodes(H,pos=pos2,node_color=H.nodes()[node]['color'],node_shape = aShape, nodelist =[node] ,node_size=3000) 
        nx.draw_networkx_edge_labels(H, pos=pos,edge_labels=labels)
        ax= plt.gca()
        plt.axis('off')
        ax.autoscale()

        ax.set_xlim([0.75*ax.get_xlim()[0],1.1*ax.get_xlim()[1]])
        ax.set_ylim([0.75*ax.get_ylim()[0],1.1*ax.get_ylim()[1]])
        ax.set_aspect('equal', adjustable='box')
        ax.set_title("Solution #"+str(sol_num+1)+" Total Costs="+str(goolist[sol_num]),y=0.95)
        return ax
    
    def to_studio(self, path=None,verbose=False):
        
        G=self.G
        gmatlist=self.gmatlist
        goplist=self.goplist
        goolist=self.goolist
        ME= self.ME
        if path==None:
            path= os.path.dirname(__file__)+"/"
        header=r'<?xml version="1.0" encoding="utf-16"?>'+"\n"
        xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsd="http://www.w3.org/2001/XMLSchema"
        Type="PNS"
        Visible="true"
        PeriodExtension="true"
        NSMAP={"xsi":xsi,"xsd":xsd}
        attrib={"Type":Type,"Visible":Visible,"PeriodExtension":PeriodExtension}
        PG="PGraph"

        PGraph=etree.Element(PG,nsmap=NSMAP,attrib=attrib)

        #Default
        Default=etree.SubElement(PGraph,"Default")

        ##Default Material
        Def_Material=etree.SubElement(Default,"Material")
        DM_FRLB=etree.SubElement(Def_Material,"FlowRateLowerBound")
        DM_FRLB.text="0"
        DM_FRUP=etree.SubElement(Def_Material,"FlowRateUpperBound")
        DM_FRUP.text="1000000000"
        DM_Price=etree.SubElement(Def_Material,"Price")
        DM_Price.text="0"
        DM_Type=etree.SubElement(Def_Material,"Type")
        DM_Type.text="1"
        DM_Deadline=etree.SubElement(Def_Material,"Deadline")
        DM_Deadline.text="31536000"
        DM_EA=etree.SubElement(Def_Material,"EarliestAvability")
        DM_EA.text="0"
        DM_Storage=etree.SubElement(Def_Material,"StorageStrategy")
        DM_Storage.text="default"


        ## Operating Unit
        Def_Op=etree.SubElement(Default,"OperatingUnit")
        DO_OFC=etree.SubElement(Def_Op,"OperatingFixCost")
        DO_OFC.text="0"
        DO_IFC=etree.SubElement(Def_Op,"InvestmentFixCost")
        DO_IFC.text="0"
        DO_OpFC=etree.SubElement(Def_Op,"OpUnitFixCost")
        DO_OpFC.text="0"
        DO_OPC=etree.SubElement(Def_Op,"OperatingPropCost")
        DO_OPC.text="0"
        DO_IPC=etree.SubElement(Def_Op,"InvestmentPropCost")
        DO_IPC.text="0"
        DO_OpUPC=etree.SubElement(Def_Op,"OpUnitPropCost")
        DO_OpUPC.text="0"
        DO_CLB=etree.SubElement(Def_Op,"CapacityLowerBound")
        DO_CLB.text="0"
        DO_CUB=etree.SubElement(Def_Op,"CapacityUpperBound")
        DO_CUB.text="1000000000"
        DO_PP=etree.SubElement(Def_Op,"PaybackPeriod")
        DO_PP.text="10"
        DO_WHPY=etree.SubElement(Def_Op,"WorkingHoursPerYear")
        DO_WHPY.text="8000"
        DO_FOT=etree.SubElement(Def_Op,"FixOperTime")
        DO_FOT.text="0"
        DO_POT=etree.SubElement(Def_Op,"PropOperTime")
        DO_POT.text="0"
        DO_EA=etree.SubElement(Def_Op,"EarliestAvability")
        DO_EA.text="0"
        DO_LA=etree.SubElement(Def_Op,"LatestAvability")
        DO_LA.text="31536000"
        DO_RM=etree.SubElement(Def_Op,"RelaxMode")
        DO_RM.text="strong"

        ## Edge
        Def_E=etree.SubElement(Default,"Edge")
        DE_FR=etree.SubElement(Def_E,"FlowRate")
        DE_FR.text="1"

        ## Quantity
        Def_Q=etree.SubElement(Default,"Quantity")
        DQ_DM=etree.SubElement(Def_Q,"default_mes")
        DQ_DM.text="gram (g)"
        DQ_TM=etree.SubElement(Def_Q,"time_mu")
        DQ_TM.text="y"
        DQ_QT=etree.SubElement(Def_Q,"quant_type")
        DQ_QT.text="Mass"
        DQ_MM=etree.SubElement(Def_Q,"money_mu")
        DQ_MM.text="EUR"

        ## SolverParameter
        DEF_SP=etree.SubElement(Default,"SolverParameter")
        DS_MC=etree.SubElement(DEF_SP,"MakespanCoefficient")
        DS_MC.text="0"
        DS_CC=etree.SubElement(DEF_SP,"CostCoefficient")
        DS_CC.text="1"
        DS_TC=etree.SubElement(DEF_SP,"TimeCoefficient")
        DS_TC.text="0"
        DS_TCLB=etree.SubElement(DEF_SP,"TotalCostLowerBound")
        DS_TCLB.text="-1000000000"
        DS_TCUB=etree.SubElement(DEF_SP,"TotalCostUpperBound")
        DS_TCUB.text="1000000000"

        # Materials
        Materials=etree.SubElement(PGraph,"Materials")

        ## Material
        type_converter={"raw_material":0,"intermediate":1,"product":2}

        Mats_list=[]
        MPar_list=[]
        for n in G.nodes():
            if n[0]=="M":
                Mats_list.append(n)
                if 'type' in G.nodes()[n]:
                    type_ind=type_converter[G.nodes()[n]['type']]
                    attr={"ID":str(list(G.nodes()).index(n)+1),"Name":n,"Type":str(type_ind)}
                    Mats_list.append(etree.SubElement(Materials,'Material',attrib=attr))
                    MPar_list.append(etree.SubElement(Mats_list[-1],'ParameterList'))
                    if 'price' in G.nodes()[n]:
                        price=G.nodes()[n]['price']
                    else:
                        price=-1
                    if 'flow_rate_lower_bound' in G.nodes()[n]:
                        flow_rate_lower_bound=G.nodes()[n]['flow_rate_lower_bound']
                    else:
                        flow_rate_lower_bound=-1            
                    
                    if 'flow_rate_upper_bound' in G.nodes()[n]:
                        flow_rate_upper_bound=G.nodes()[n]['flow_rate_upper_bound']
                    else:
                        flow_rate_upper_bound=-1             
                    
                    etree.SubElement(MPar_list[-1],'Parameter',attrib={"Name":"price", "Prefix":"Price: ", "Value":str(price), "Visible":"false"})
                    etree.SubElement(MPar_list[-1],'Parameter',attrib={"Name":"reqflow", "Prefix":"Required flow: ", "Value":str(flow_rate_lower_bound), "Visible":"false"})
                    etree.SubElement(MPar_list[-1],'Parameter',attrib={"Name":"maxflow", "Prefix":"Maximum flow: ", "Value":str(flow_rate_upper_bound), "Visible":"false"})
                    etree.SubElement(MPar_list[-1],'Parameter',attrib={"Name":"quantitytype", "Prefix":"Quantity type: ", "Value":"Mass", "Visible":"false"})
                    etree.SubElement(MPar_list[-1],'Parameter',attrib={"Name":"measurementunit", "Prefix":"Measurement unit: ", "Value":"gram (g)", "Visible":"false"})

        # Edges
        Edges=etree.SubElement(PGraph,"Edges")

        ## Edge
        global_edge_count=len(list(G.nodes()))+1
        edge_list=[]
        nodes_list=[]
        label_list=[]
        offset_list=[]
        X_list=[]
        Y_list=[]
        for n in G.nodes():
            if n[0]=="O":
                ee=G.in_edges(n)
                for e in ee:
                    ratio=G[e[0]][e[1]]['weight']
                    attr={"ID":str(global_edge_count),"BeginID":str(list(G.nodes()).index(e[0])+1),"EndID":str(list(G.nodes()).index(e[1])+1),"Title":str(ratio), "ArrowOnCenter":"true","ArrowPosition":"50"}
                    edge_list.append(etree.SubElement(Edges,'Edge', attrib=attr))
                    nodes_list.append(etree.SubElement(edge_list[-1],'Nodes')) #Hanging
                    label_list.append(etree.SubElement(edge_list[-1],'Label',attrib={"Text":str(ratio)}))
                    offset_list.append(etree.SubElement(label_list[-1],'Offset'))
                    X_list.append(etree.SubElement(offset_list[-1],"X"))
                    Y_list.append(etree.SubElement(offset_list[-1],"Y"))
                    X_list[-1].text="0"
                    Y_list[-1].text="0"
                    etree.SubElement(label_list[-1],"FontSize").text="-1"
                    etree.SubElement(label_list[-1],"Color").text="-16777216"
                    etree.SubElement(edge_list[-1],'Color').text="-16777216"
                    etree.SubElement(edge_list[-1],'LongFormat').text="false"
                    etree.SubElement(edge_list[-1],'Comment') #hanging
                    etree.SubElement(edge_list[-1],'CommentVisible').text="false"
                    
                    global_edge_count+=1
                ff=G.out_edges(n)
                for f in ff:
                    ratio=-G[f[0]][f[1]]['weight']
                    attr={"ID":str(global_edge_count),"BeginID":str(list(G.nodes()).index(f[0])+1),"EndID":str(list(G.nodes()).index(f[1])+1),"Title":str(ratio), "ArrowOnCenter":"true","ArrowPosition":"50"}
                    edge_list.append(etree.SubElement(Edges,'Edge', attrib=attr))
                    nodes_list.append(etree.SubElement(edge_list[-1],'Nodes')) #Hanging
                    label_list.append(etree.SubElement(edge_list[-1],'Label',attrib={"Text":str(ratio)}))
                    offset_list.append(etree.SubElement(label_list[-1],'Offset'))
                    X_list.append(etree.SubElement(offset_list[-1],"X"))
                    Y_list.append(etree.SubElement(offset_list[-1],"Y"))
                    X_list[-1].text="0"
                    Y_list[-1].text="0"
                    etree.SubElement(label_list[-1],"FontSize").text="-1"
                    etree.SubElement(label_list[-1],"Color").text="-16777216"
                    etree.SubElement(edge_list[-1],'Color').text="-16777216"
                    etree.SubElement(edge_list[-1],'LongFormat').text="false"
                    etree.SubElement(edge_list[-1],'Comment') #hanging
                    etree.SubElement(edge_list[-1],'CommentVisible').text="false"
                    global_edge_count+=1

        # Operating Units
        OperatingUnits=etree.SubElement(PGraph,"OperatingUnits")
         
        ## Operating Unit
        opu_list=[]
        OPar_list=[]
        for n in G.nodes():
            if n[0]=="O":
                attr={"ID":str(list(G.nodes()).index(n)+1),"Name":n,"Title":""}
                opu_list.append(etree.SubElement(OperatingUnits,'OperatingUnit', attrib=attr))
                OPar_list.append(etree.SubElement(opu_list[-1],'ParameterList'))
                if 'capacity_lower_bound' in G.nodes()[n]:
                    capacity_lower_bound=G.nodes()[n]['capacity_lower_bound']
                else:
                    capacity_lower_bound=-1
                if 'capacity_upper_bound' in G.nodes()[n]:
                    capacity_upper_bound=G.nodes()[n]['capacity_upper_bound']
                else:
                    capacity_upper_bound=-1                
                if 'fix_cost' in G.nodes()[n]:
                    fix_cost=G.nodes()[n]['fix_cost']
                else:
                    fix_cost=-1 
                if 'proportional_cost' in G.nodes()[n]:
                    proportional_cost=G.nodes()[n]['proportional_cost']
                else:
                    proportional_cost=-1 
                
                etree.SubElement(OPar_list[-1],'Parameter',attrib={"Name":"caplower", "Prefix":"Capacity, lower bound: ", "Value":str(capacity_lower_bound), "Visible":"false"})
                etree.SubElement(OPar_list[-1],'Parameter',attrib={"Name":"capupper", "Prefix":"Capacity, upper bound: ", "Value":str(capacity_upper_bound), "Visible":"false"})
                etree.SubElement(OPar_list[-1],'Parameter',attrib={"Name":"investcostfix", "Prefix":"Investment cost, fix: ", "Value":str(fix_cost), "Visible":"false"})
                etree.SubElement(OPar_list[-1],'Parameter',attrib={"Name":"investcostprop", "Prefix":"Investment cost, proportional: ", "Value":str(proportional_cost), "Visible":"false"})
                etree.SubElement(OPar_list[-1],'Parameter',attrib={"Name":"opercostfix", "Prefix":"Operating cost, fix: ", "Value":"-1", "Visible":"false"})
                etree.SubElement(OPar_list[-1],'Parameter',attrib={"Name":"opercostprop", "Prefix":"Operating cost, proportional: ", "Value":"-1", "Visible":"false"})
                etree.SubElement(OPar_list[-1],'Parameter',attrib={"Name":"workinghour", "Prefix":"Working hours per year: ", "Value":"-1", "Visible":"false"})
                etree.SubElement(OPar_list[-1],'Parameter',attrib={"Name":"payoutperiod", "Prefix":"Payout Period: ", "Value":"-1", "Visible":"false"})

        # MutualExclusions
        MutualExclusions=etree.SubElement(PGraph,"MutualExclusions")

        ## MutualExclusion
        ME_list=[]
        MOP_list=[]
        for M in ME:
            Name="_".join(M)
            attr={"ID":str(global_edge_count),"Name":Name}
            ME_list.append(etree.SubElement(MutualExclusions,"MutualExclusion",attrib=attr))
            MOP_list.append(etree.SubElement(ME_list[-1],"OperatingUnits"))
            for x in M:
                etree.SubElement(MOP_list[-1],"OperatingUnit").text=x
            global_edge_count+=1

        # Solutions
        Solutions=etree.SubElement(PGraph,"Solutions")

        ## Solution 
        ssol_list=[]
        smats_list=[]
        sops_list=[]
        sop_list=[]

        for i in range(len(goolist)):
            snum=i+1
            attr={"Index":str(i), "Title":"Solution #"+str(snum), "OptimalValue":str(goolist[i]),"TotalTime":"0", "TotalMakespan":"0", "ObjectiveValue":str(goolist[i]), "AlgorithmUsed":"INSIDEOUT"}
            ssol_list.append(etree.SubElement(Solutions,"Solutions",attrib=attr))
            smats_list.append(etree.SubElement(ssol_list[-1],"Materials"))
            for x in gmatlist[i]:
                attr={"Name":x[0],"Flow":str(x[3]),"Cost":str(x[1]), "MU":""}
                etree.SubElement(smats_list[-1],"Material",attrib=attr)
            
            sops_list.append(etree.SubElement(ssol_list[-1],"OperatingUnits"))
            for x in goplist[i]:
                attr={"Name":x[1],"Size":str(x[0]),"Cost":str(x[2]),"MU":""}
                sop_list.append(etree.SubElement(sops_list[-1],"OperatingUnit",attrib=attr))
                etree.SubElement(sop_list[-1],"Input")
                etree.SubElement(sop_list[-1],"Output")
                
        xml=etree.tostring(PGraph,pretty_print=True,encoding='unicode', method='xml')

        with open(path+"studio_file.pgsx","w") as f:
            f.write(header)
            f.write(xml)
        if verbose:
            print(header+xml)
            print("Generated P-graph Studio File at ", path)
        return header+xml    
        
    def run(self):
        self.convert_problem()
        self.solve()
        self.read_solution()
        
    def get_info(self):
        return self.gmatlist,self.goplist,self.goolist
    def get_sol_num(self):
        return len(self.goolist)
if __name__=="__main__":
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
    