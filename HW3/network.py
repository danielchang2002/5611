import sys
import math
import random

num_networks = 10
random.seed(42)

class Network:
  def __init__(self, layers):
    self.layers = layers

  def forward(self, x):
    """
    Forward propagates the input through the network 
    Returns the network output
    """
    output = x
    for layer in self.layers:
      output = layer.forward(output)
    return output

  def backward(self, dL_dOutput):
    """
    Backpropagates the loss derivative through the network
    Returns the partial derivative of the loss with respect to the input
    """
    dL_dx = dL_dOutput
    for layer in reversed(self.layers):
      dL_dx = layer.backward(dL_dx)
    return dL_dx

class Layer:
  def __init__(self, w, b, relu):
    self.w = Matrix(w)
    self.b = Matrix(b)
    self.relu = relu
    self.last_z = None
  
  def forward(self, x):
    z = (self.w * x) + self.b
    self.last_z = z
    output = z
    if self.relu: 
      output = output.relu()
    return output

  def backward(self, dL_dOutput):
    assert(self.last_z is not None)
    dL_dz = None
    if self.relu:
      dL_dz = dL_dOutput.times(self.last_z.relu_derivative().transpose())
    else:
      dL_dz = dL_dOutput
    dz_dx = self.w
    back = dL_dz * dz_dx
    return back


class Matrix:
  def __init__(self, data):
    assert(type(data) == list and 
      type(data[0]) == list and 
      (type(data[0][0]) == float or type(data[0][0]) == int))
    self.data = data
    self.shape = (len(data), len(data[0]))

  def __mul__(self, b):
    assert(self.shape[1] == b.shape[0])
    new_data = [[0] * b.shape[1] for i in range(self.shape[0])]
    for i in range(len(new_data)):
      for j in range(len(new_data[0])):
        new_data[i][j] = sum([tup[0] * tup[1] for tup in zip(self.data[i], [b.data[row][j] for row in range(b.shape[0])])])
    return Matrix(new_data)

  def is_finite(self):
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        if math.isnan(self.data[i][j]) or math.isinf(self.data[i][j]):
          return False
    return True
  

  def scale(self, val):
    new_data = [[-1 for j in range(self.shape[1])] for i in range(self.shape[0])]
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        new_data[i][j] = self.data[i][j] * val
    return Matrix(new_data)

  def apply(self, func):
    new_data = [[-1 for j in range(self.shape[1])] for i in range(self.shape[0])]
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        new_data[i][j] = func(self.data[i][j])
    return Matrix(new_data)

  def times(self, b):
    assert(self.shape == b.shape)
    new_data = [[-1 for j in range(self.shape[1])] for i in range(self.shape[0])]
    for i in range(len(new_data)):
      for j in range(len(new_data[0])):
        new_data[i][j] = self.data[i][j] * b.data[i][j]
    return Matrix(new_data)


  def transpose(self):
    new_data = [[-1 for j in range(self.shape[0])] for i in range(self.shape[1])]
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        new_data[j][i] = self.data[i][j]
    return Matrix(new_data)

  def relu(self):
    new_data = [[-69 for j in range(self.shape[1])] for i in range(self.shape[0])]
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        new_data[i][j] = max(0, self.data[i][j])
    return Matrix(new_data)

  def relu_derivative(self):
    new_data = [[-1 for j in range(self.shape[1])] for i in range(self.shape[0])]
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        new_data[i][j] = 0 if self.data[i][j] < 0 else 1
    return Matrix(new_data)
    
  def abs_derivative(self):
    new_data = [[-1 for j in range(self.shape[1])] for i in range(self.shape[0])]
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        new_data[i][j] = -1 if self.data[i][j] < 0 else 1
    return Matrix(new_data)


  def __add__(self, b):
    # only support (broadcast) adding of matrix w/ single column matrix
    assert(self.shape[0] == b.shape[0] and b.shape[1] == 1)
    new_data = [[self.data[i][j] + b.data[i][0] for j in range(len(self.data[0]))] for i in range(len(self.data))]
    return Matrix(new_data)

  def plus(self, b):
    # only support subtraction w/ same shape
    assert(self.shape == b.shape)
    new_data = [[self.data[i][j] + b.data[i][j] for j in range(len(self.data[0]))] for i in range(len(self.data))]
    return Matrix(new_data)

  def __str__(self):
    return str(self.data)

  @staticmethod
  def random(shape):
    data = [[random.random() for j in range(shape[1])] for i in range(shape[0])]
    return Matrix(data)

  def sum(self):
    return sum([sum([abs(d) for d in row]) for row in self.data])

def parse_matstring(matstring, num_rows, num_cols):
  vals = [float(s) for s in matstring.split()]
  mat = [vals[r * num_cols : (r + 1) * num_cols] for r in range(num_rows)]
  return mat

def load_layer(f):
  num_rows = int(f.readline().split(":")[-1].strip())
  num_cols = int(f.readline().split(":")[-1].strip())
  weight_str = f.readline().split(":")[-1].replace("[", " ").replace("]", " ").replace(",", " ")
  bias_str = f.readline().split(":")[-1].replace("[", " ").replace("]", " ").replace(",", " ")
  weight = parse_matstring(weight_str, num_rows, num_cols)
  bias = parse_matstring(bias_str, num_rows, 1)
  use_relu = f.readline().split(":")[-1].strip() == "true"
  return Layer(weight, bias, use_relu)


def evaluate_network(f, solution_file):
  num_layers = int(f.readline().split(":")[-1].strip())
  layers = [load_layer(f) for i in range(num_layers)]
  net = Network(layers)

  # -----------For testing---------------------
  # input_str = f.readline().split(":")[-1].replace("[", " ").replace("]", " ").replace(",", " ")
  # input_mat = Matrix(parse_matstring(input_str, layers[0].w.shape[1], 1))
  # output = net.forward(input_mat)
  # print(f.readline()[:-1])
  # print("implementation output:", output)
  # print()
  f.readline()
  f.readline()
  # -----------For testing---------------------

  input_str = solution_file.readline().replace(",", " ")
  input_mat = Matrix(parse_matstring(input_str, layers[0].w.shape[1], 1))
  output = net.forward(input_mat)
  print(output.sum())

def find_best_input(f, solution_file, params):
  alpha = params["alpha"]
  gradient_scaling = params["gradient_scaling"]
  beta = params["beta"]
  beta2 = params["beta2"]
  iters = params["iters"]

  num_layers = int(f.readline().split(":")[-1].strip())
  layers = [load_layer(f) for i in range(num_layers)]
  net = Network(layers)
  f.readline()
  f.readline()

  if "init" in params:
    input_ = Matrix(params["init"]).transpose()
  else:
    input_ = Matrix.random((layers[0].w.shape[1], 1))

  output = net.forward(input_)
  dL_dOutput = output.transpose()
  if "abs_loss" in params:
    dL_dOutput = dL_dOutput.abs_derivative()
  grad = net.backward(dL_dOutput)
  grad_scale = grad.times(grad).transpose().apply(lambda x : 1 / math.sqrt(x + 0.00001))

  for i in range(iters):

    # forward pass
    output = net.forward(input_)

    # backward pass
    dL_dOutput = output.transpose()
    if "abs_loss" in params:
      dL_dOutput = dL_dOutput.abs_derivative()
    cur_grad = net.backward(dL_dOutput)

    # Compute gradient w/ momentum
    grad = grad.scale(beta).plus(cur_grad.scale(1 - beta))

    # Compute gradient scaling factor w/ momentum
    cur_grad_scale = grad.times(grad).transpose().apply(lambda x : 1 / math.sqrt(x + 0.00001))
    grad_scale = grad_scale.scale(beta2).plus(cur_grad_scale.scale(1 -  beta2))

    update = grad.transpose().scale(-alpha)

    if gradient_scaling:
      update = update.times(grad_scale)

    input_ = input_.plus(update)

  assert(input_.is_finite())
  solution_file.write(str(input_).replace("[", "").replace("]", "").replace(" ", "") + "\n")

  output = net.forward(input_)
  print(output.sum())

def main():
  if len(sys.argv) != 4:
    print("Usage: python3 network.py networks.txt solution.txt -train|-test")
    return
  if sys.argv[-1] == "-test":
    print("Network output:")
    with open(sys.argv[1]) as network_file:
      with open(sys.argv[2]) as solution_file:
        for i in range(num_networks):
          evaluate_network(network_file, solution_file)
          network_file.readline()
  elif sys.argv[-1] == "-train":
    params = [
      {
        # cost = very small 
        "iters" : 1000,
        "alpha" : 0.1,
        "gradient_scaling" : False,
        "beta": 0,
        "beta2" : 0
      },
      {
        # cost = very small 
        "iters" : 10000,
        "alpha" : 0.0001,
        "gradient_scaling" : True,
        "beta": 0.99,
        "beta2" : 0.5
      },
      {
        # cost = very small 
        "iters" : 100000,
        "alpha" : 0.00001,
        "gradient_scaling" : False,
        "beta": 0.999,
        "beta2" : 0.1,
        "init" : [[0.4623862,0.1853604,1.5853058,2.0497122,0.87354726,0.08244722]]
      },
      {
        # cost = very small 
        "iters" : 20000,
        "alpha" : 0.0001,
        "gradient_scaling" : True,
        "beta": 0.99,
        "beta2" : 0.8
      },
      {
        # cost = 838
        "iters" : 20000,
        "alpha" : 0.000000001,
        "gradient_scaling" : False,
        "beta": 0.5,
        "beta2" : 0
      },
      {
        # cost = very small 
        "iters" : 9999,
        "alpha" : 0.000001,
        "gradient_scaling" : True,
        "beta": 0.99,
        "beta2" : 0.1
      },
      {
        # cost = very small 
        "iters" : 10000,
        "alpha" : 0.00001,
        "gradient_scaling" : False,
        "beta": 0.99,
        "beta2" : 0.1
      },
      {
        # cost = 848
        "iters" : 9999,
        "alpha" : 0.000000001,
        "gradient_scaling" : False,
        "beta": 0.4,
        "beta2" : 0
      },
      {
        # cost = 18974
        "iters" : 9999,
        "alpha" : 0.0001,
        "gradient_scaling" : True,
        "beta": 0.99,
        "beta2" : 0
      },
      {
        # cost = 320
        "iters" : 11999,
        "alpha" : 0.0001,
        "gradient_scaling" : True,
        "beta": 0.6,
        "beta2" : 0.99,
        "abs_loss" : True,
      },
    ]
    with open(sys.argv[1]) as network_file:
      with open(sys.argv[2], "w") as solution_file:
        for i in range(num_networks):
          print(f"Network {i + 1}:")
          find_best_input(network_file, solution_file, params[i])
          print()
          network_file.readline()
  else:
    print("Usage: python3 network.py solution.txt -train|-test")

if __name__ == "__main__":
  main()