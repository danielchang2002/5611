class Network:
  def __init__(self, layers):
    self.layers = layers

  def forward(self, x):
    output = x
    for layer in self.layers:
      output = layer.forward(output)
    return output

class Layer:
  def __init__(self, w, b, relu):
    self.w = Matrix(w)
    self.b = Matrix(b)
    self.relu = relu
  
  def forward(self, x):
    z = (self.w * x) + self.b
    if self.relu: z.relu()
    return z

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

  def relu(self):
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        self.data[i][j] = max(0, self.data[i][j])

  def __add__(self, b):
    # only support (broadcast) adding of matrix w/ single column matrix
    assert(self.shape[0] == b.shape[0] and b.shape[1] == 1)
    new_data = [[self.data[i][j] + b.data[i][0] for j in range(len(self.data[0]))] for i in range(len(self.data))]
    return Matrix(new_data)

  def __str__(self):
    return str(self.data)

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


def evaluate_network(f):
  num_layers = int(f.readline().split(":")[-1].strip())
  layers = [load_layer(f) for i in range(num_layers)]
  net = Network(layers)
  input_str = f.readline().split(":")[-1].replace("[", " ").replace("]", " ").replace(",", " ")
  input_mat = Matrix(parse_matstring(input_str, layers[0].w.shape[1], 1))
  output = net.forward(input_mat)
  # print(f.readline()[:-1])
  print("implementation output:", output)
  print()


def main():
  with open("quiz_networks.txt") as f:
    while True:
      try:
        evaluate_network(f)
        f.readline()
      except Exception as e:
        break

if __name__ == "__main__":
  main()