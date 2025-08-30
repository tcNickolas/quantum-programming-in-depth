# Quantum Programming In Depth Samples
Code samples for the book ["Quantum Programming In Depth: Solving Problems with Q# and Qiskit"](https://www.manning.com/books/quantum-programming-in-depth) by Mariia Mykhailova.

<img width="600" height="600" alt="Quantum Programming in Depth book cover" src="https://github.com/user-attachments/assets/4cf8153c-183b-4fb0-bc3f-9fe2110f6c95" />

### [Chapter 2. Prepare Quantum States](./2_state_preparation/)

### [Chapter 3. Implement Quantum Operations](./3_unitary_implementation/)

### [Chapter 4. Analyze Quantum States](./4_analyze_states/)

### [Chapter 5. Analyze Quantum Operations](./5_analyze_operations/)

### [Chapter 6. Evaluate Classical Functions on a Quantum Computer](./6_reversible_computing/)

### [Chapter 7. Grover's Search Algorithm](./7_grovers_search/)

### [Chapter 8. Solve N Queens Puzzle Using Grover's Algorithm](./8_n_queens/)

### [Chapter 9. Evaluate Performance of Quantum Algorithms](./9_evaluate_performance/)

## Setting up your environment

The recommended setup for running the samples from this book is based on [Visual Studio Code](https://code.visualstudio.com/).

### Qiskit

Originally I used Python 3.12, Qiskit 1.3.1, and qiskit-aer 0.15.1 to develop the Qiskit code for this book. 
Once you have a Python environment set up, you can install these packages using pip:

    pip install qiskit==1.3.1 qiskit-aer==0.15.1

The latest versions of packages used to test the code is **Qiskit 2.1.2** and **qiskit-aer 0.17.1**.

### Q#

Originally I used Python 3.12 and Q# 1.11.1 to develop the Q# code for this book. 
Once you have a Python environment set up, you can install this package using pip:

    pip install qsharp==1.11.1

The latest version of the package used to test the code is **Q# 1.20.0**.

Additionally, [Azure Quantum Development Kit extension](https://marketplace.visualstudio.com/items?itemName=quantum.qsharp-lang-vscode) for Visual Studio Code provides Q# language support in the editor. 

### pytest

Unit tests in this book are Python-based and use the pytest testing framework. Once you have a Python environment set up, you can install the latest version of pytest using pip:

    pip install pytest

## Running the samples

The project folder for most sections includes the complete tests for the code developed in this section, even if they are omitted from the book itself. 
To run the tests for the project, navigate to the folder that corresponds to the section and run pytest.

Sections 2.1–2.3, 3.1–3.2, and 6.2 are the exception to this rule, since I don’t introduce the ways to test the code written in these sections until later. The code for these sections can be executed either as a Python script or as a Q# script using the Azure Quantum Development Kit extension. Please refer to the text of corresponding sections for details.
