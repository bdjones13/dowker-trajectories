

Getting Started
=======================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Installation
************
If you have a system compatible with any of the compiled binary wheels listed `here <https://pypi.org/project/dowker-trajectories/>`_, you can just install via ``pip install dowker-trajectories``.

From Source
************

Clone the repository from GitHub and pip install locally::

   git clone https://github.com/bdjones13/dowker-trajectories.git
   cd dowker-trajectories
   pip install .


Dependencies
************

All of these are installed automatically:

* pytest
* gudhi
* numpy
* networkx
* scipy (dependency for networkx adjacency matrix)
* matplotlib
* plotly
* nbformat>=4.2.0 (dependency for plotly)