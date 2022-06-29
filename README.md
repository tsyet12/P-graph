# Pgraph : Process Graphs for Process Network Synthesis (PNS)

![Pgraphlogo](https://user-images.githubusercontent.com/19692103/176261331-5ec5fd1d-eec6-467c-b79c-ed48691eecfb.png)
[![DOI](https://zenodo.org/badge/507569838.svg)](https://zenodo.org/badge/latestdoi/507569838)

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
* [Example Code](#usage-examples)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [References](#references)


<!-- ABOUT THE PROJECT -->
## About The Project
This project aims at enabling the classical P-graph Framework (www.p-graph.org) to interface with modern Python programming ecosystems. The backend solver is the original executable from P-graph, staying true to the original implementation of P-graph. For manual network manipulation, the P-graph studio can be downloaded from this link: https://p-graph.org/downloads/. 



<!-- GETTING STARTED -->
## Getting Started

Install this library either from the official pypi or from this Github repository:

## Install a Stable Version (pypi)
```bat
pip install ProcessGraph
```
## Install most updated version from Github

In a environment terminal or CMD:
```bat
pip install git+https://github.com/tsyet12/Pgraph
```


<!-- USAGE EXAMPLES -->
## Example Code

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
#############################
```
![example](https://user-images.githubusercontent.com/19692103/176265167-3e41b536-9f2b-48df-b559-9290277065e7.png)

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

Distributed under the Open Sourced BSD-2-Clause License. See [`LICENSE`](https://github.com/tsyet12/Chemsy/blob/main/LICENSE) for more information.


<!-- CONTACT -->
## Contact
Main Developer:

Sin Yong Teng sinyong.teng@ru.nl or tsyet12@gmail.com
Radboud University Nijmegen

<!-- References -->
## References

Friedler, F., Tarjan, K., Huang, Y.W. and Fan, L.T., 1992. Graph-theoretic approach to process synthesis: axioms and theorems. Chemical Engineering Science, 47(8), pp.1973-1988.

Friedler, F., Tarjan, K., Huang, Y.W. and Fan, L.T., 1992. Combinatorial algorithms for process synthesis. Computers & chemical engineering, 16, pp.S313-S320.

Friedler, F., Tarjan, K., Huang, Y.W. and Fan, L.T., 1993. Graph-theoretic approach to process synthesis: polynomial algorithm for maximal structure generation. Computers & Chemical Engineering, 17(9), pp.929-942.
