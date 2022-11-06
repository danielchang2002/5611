# 5611 HW3: Optimization-Based Animation 
Daniel Chang

## Methods
I used gradient descent with momentum based gradient updates, and gradient scaling (with momentum updates).
I implemented a Matrix class that implements basic matrix operations and basic matrix calculus. Using this matrix class, I implemented a Network/Layer class that handles the forward and backward propagation.

For each network, I tested a bunch of hyperparameters and kept the best performing ones.
For some of the trickier networks, I copied the sample inputs and used them as the initialization values for the inputs, then applied gradient descent.

## Usage

To compute the output of a neural network, please run:
```bash
python3 network.py networks.txt sample_inputs.txt -test
```
where networks.txt is the list of network weights/biases, and sample_inputs.txt is the file containing the inputs of the network

To find the optimal inputs, please run:
```bash
python3 network.py networks.txt solution.txt -test
```
where networks.txt is the list of network weights/biases, and solution.txt is the file to be created that will contain the optimal inputs
