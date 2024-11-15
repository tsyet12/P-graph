# Pgraph : Process Graphs for Process Network Synthesis (PNS)

![Pgraphlogo](https://user-images.githubusercontent.com/19692103/176261331-5ec5fd1d-eec6-467c-b79c-ed48691eecfb.png)
[![DOI](https://zenodo.org/badge/507569838.svg)](https://zenodo.org/badge/latestdoi/507569838)

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
* [Usage Examples](#usage-examples)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [References](#references)


<!-- ABOUT THE PROJECT -->
## About The Project
This project aims at enabling the classical P-graph Framework (www.p-graph.org) to interface with modern Python programming ecosystems. The backend solver is the original executable from P-graph, staying true to the original implementation of P-graph. For manual network manipulation, the P-graph studio can be downloaded from this link: https://p-graph.org/downloads/. 

# Changelog

15/11/2024: Custom solvers can now be properly selected for advanced users under the P.run() function via 'solver_name' and 'path' arguments. Merged output error fixes for 1 operating unit (by Alma).

14/11/2024: Due to update of P-graph studio, mutual exclusion is not properly processed. This is now fixed. Custom solvers can now also be selected for advanced users.

18/10/2024: Due to update of networkx draw, older versions of Pgraph crashes when it draws the graph. This has now been fixed. Users now need to adjust axis size themselves.


<!-- GETTING STARTED -->
## Getting Started

Install this library either from the official PyPI or from this Github repository:

## Install a Stable Version (PyPI)
```bat
pip install ProcessGraph
```
## Install most updated version from Github

In a environment terminal or CMD:
```bat
pip install git+https://github.com/tsyet12/Pgraph
```


<!-- USAGE EXAMPLES -->
## Usage Examples

See [`examples`](https://github.com/tsyet12/Pgraph/tree/main/examples) for all code examples.

### Simple Example
```python
from Pgraph.Pgraph import Pgraph #This is our Pgraph library
import networkx as nx
import matplotlib.pyplot as plt
##### STEP 1 : Problem Specification ######
G = nx.DiGraph()
G.add_node("M1",names="Product D",type='product',flow_rate_lower_bound=100, flow_rate_upper_bound=100)
G.add_node("M2",names="Chemical A",type='raw_material',price=200,flow_rate_lower_bound=0)
G.add_node("M3",names="Chemical B", type='raw_material',price=100,flow_rate_lower_bound=0)
G.add_node("M4",names="Chemical C", type='raw_material',price=10,flow_rate_lower_bound=0)
G.add_node("O1",names="Reactor 1",fix_cost=2000, proportional_cost=400)
G.add_node("O2", names="Reactor 2",fix_cost=1000, proportional_cost=400)
G.add_edge("M2","O1", weight = 1)
G.add_edge("M3","O2", weight = 1)
G.add_edge("M4","O2", weight = 2)
G.add_edge("O1","M1", weight = 0.7) 
G.add_edge("O2","M1", weight = 0.9) 
ME=[["O1","O2"]]  #Reactor 1 and Reactor 2 are mutually excluded. Only one can be chosen as solution.

#### Step 2:  Setup Solver ####
P=Pgraph(problem_network=G, mutual_exclusion=ME, solver="INSIDEOUT",max_sol=100)

#### Step 2.1:  Plot Problem #####
ax1=P.plot_problem(figsize=(5,5))
ax1.set_xlim(0,200)
plt.show()
##################################
```

![fullnetwork](https://user-images.githubusercontent.com/19692103/176417558-2506be4e-5283-4c7c-9dd7-d271e52555d0.png)

```python
#### Step 3: Run ####
P.run()
#### Step 3.1: Plot Solution########
total_sol_num=P.get_sol_num() 
for i in range(total_sol_num): # Here we loop through all the solutions to plot everything
    ax=P.plot_solution(sol_num=i) #Plot Solution Function
    ax.set_xlim(0,200)
    plt.show()
```

![example](https://user-images.githubusercontent.com/19692103/176265167-3e41b536-9f2b-48df-b559-9290277065e7.png)
![sol2](https://user-images.githubusercontent.com/19692103/176417706-dd2817eb-a6e0-4804-9c86-5d443d4567e6.png)

```python
#### Step 3.2: Export to P-graph Studio ####
from google.colab import files #This is only for google colab
string = P.to_studio(path='./',verbose=False) #export to p-graph studio
files.download("./studio_file.pgsx") #download for google colab
#Note: Please be reminded to press "Generate Layout" button in P-graph Studio after opening
```

Press "Generate Layout" Button:

![layout](https://user-images.githubusercontent.com/19692103/176418041-e970a0bd-1b93-4a64-9cdb-544ae8c6a88b.PNG)


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b testbranch/prep`)
3. Commit your Changes (`git commit -m 'Improve testbranch/prep'`)
4. Push to the Branch (`git push origin testbranch/prep`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the Open Sourced BSD-2-Clause License. See [`LICENSE`](https://github.com/tsyet12/Pgraph/blob/main/LICENSE) for more information.


<!-- CONTACT -->
## Contact
Main Developer:

Sin Yong Teng sinyong.teng@ru.nl or tsyet12@gmail.com
Radboud University Nijmegen

<!-- References -->
## References

Teng, S.Y., Orosz, Á., How, B.S., Pimentel, J., Friedler, F. and Jansen, J.J., 2022. Framework to Embed Machine Learning Algorithms in P-graph: Communication from the Chemical Process Perspectives. Chemical Engineering Research and Design. (Paper explaining the software)

Friedler, F., Tarjan, K., Huang, Y.W. and Fan, L.T., 1992. Graph-theoretic approach to process synthesis: axioms and theorems. Chemical Engineering Science, 47(8), pp.1973-1988.

Friedler, F., Tarjan, K., Huang, Y.W. and Fan, L.T., 1992. Combinatorial algorithms for process synthesis. Computers & chemical engineering, 16, pp.S313-S320.

Friedler, F., Tarjan, K., Huang, Y.W. and Fan, L.T., 1993. Graph-theoretic approach to process synthesis: polynomial algorithm for maximal structure generation. Computers & Chemical Engineering, 17(9), pp.929-942.


## Acknowledgements
The research contribution from S.Y. Teng is supported by the European Union's Horizon Europe Research and Innovation Program, under Marie Skłodowska-Curie Actions grant agreement no. 101064585 (MoCEGS).


## How to cite this software

S.Y. Teng (2022). tsyet12/Pgraph: Process Graphs for Process Network Synthesis (PNS), Zenodo Release 2 (v1.0-zenodo-2). Zenodo. https://doi.org/10.5281/zenodo.6778354
