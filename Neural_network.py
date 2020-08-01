# use numpy array to store the arrays
x = np.array(([3,5], [5,1], [10,2], dtype = float)
y = np.array(([75], [82], [93], dtype = float)
# how to interface with python adding and retreiving ouputs from the code
x = x/np.amax(x, axis = 0)
y = y/100

class Neural_Network(object):
	def _init_(self)
	#Define HyperParameters
	self.inputLayerSize = 2
	self.outputLayerSize = 1
	self.hiddenLayerSize = 3

	def forward(self, x):
	#propagate inputs through network
		self.z2 = np.dot(x, self.w1)
		self.a2 = self.sigmoid(self.z2)
		self.z3 = np.dot(self.a2, self.w2)
		yHat = self.sigmoid(self.z3)

	def sigmoid(self, z):
		return 1/(1+np.exp(-z))

	def sigmoidPrime(z):
		#derivative of Sigmoid Function
		return np.exp(-z)/((1+np.exp(-z))**2)

	def costFunction(self, y , yHat)
		cost = sum(0.5*(y-yHat)**2)

		return cost 

	def costFunctionPrime(self, x, y):
		#Compute derivative with respect to W1 and W2
		self.yHat = self.forward(x)
		delta3 = np.multiply(-y - self.yhat), self.sigmoidPrime(self.z3))
		dJdW2 = np.dot(self.a2.T, delta3)
		delta2 = np.dot(delta3, self.W2.T)*self.sigmoidPrime(self.z2)
		dJdW1 = np.dot(X.T, delta2)
		return dJdW1, dJdW2


#testInput = np.arrange(-6,6,0.01)
#plot(testInput, sigmoid(testInput), LineWidth = 2)
#grid(1)
#you can pass directy the array in numpy and i will apply the function on each input and it will return the result also in form of as an array
formula for propagation in a neural network
z(2) = XW(1)    
#z is an array having the different of scalar product of weight and input of each node(neuron) of the neural network
a(2) = f(z(2))  #a is the result of applying the sigmoid function to each element of z matrix
## Part2

from videoSupport import *
from scipy import optimize

class trainer(object):

	def _init_(self, N):
		#Make local reference to Neural Network
		self.N = N

	def costFunctionWrapper(self, params, x, y):
		self.N.setParams(params)
		cost = self.N.costFunction(x,y)
		grad = self.N.computeGradients(x,y)
		return cost, grad

	def callbackF(self, params):
		self.N.getParams(params)
		self.J.append(self.N.costFunction(self.x, self.y))


	def train(self, x, y):
		self.x = x
		self.y = y 
		self.J =[]
		params0 = self.N.getParams()
		options = {'maxiter': 200, 'disp' : True}
		_res =  optimize.minimize(self.costFunctionWrapper, params0, jac = True, method = 'BFGS', args =(X,y), options = options, callback = self.callBackF)
		self.N.setParams(_res.x)
		self.optimizationResults = _res

