import numpy;
import scipy.special;


class NeuralNetwork:

    # initialise the neural network
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # set number of nodes in each input, hidden, output layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        # w11 w21
        # w12 w22 etc
        self.wih = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        # learning rate
        self.lr = learningrate

        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

        pass

    # train the neural network
    def train(self, inputs_list, targets_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = numpy.dot(self.who.T, output_errors)

        # update the weights for the links between the hidden and output layers
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                        numpy.transpose(hidden_outputs))

        # update the weights for the links between the input and hidden layers
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)),
                                        numpy.transpose(inputs))

        pass

    # query the neural network
    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs


def main():

    # number of input, hidden and output nodes
    input_nodes = 784;
    hidden_nodes = 100;
    output_nodes = 10;

    # learning rate is 0.3
    learning_rate = 0.3;

    # create instance of neural network
    nn = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate);

    # load the mnisst training data CSV file into a list
    data_file = open("./mnist_train_100.csv", "r");
    data_list = data_file.readlines();
    data_file.close();

    # Iterate the training data and train the network appropriately
    for record in data_list:
        all_values = record.split(",");
        # scale and shift the inputs
        inputs = (numpy.asfarray(all_values[1:]) / 255 * 0.9) + 0.01;
        # create the target output values (all 0.01, except the desired label which is  0.99)
        targets = numpy.zeros(output_nodes) + 0.01;
        targets[int(all_values[0])] = 0.99;
        nn.train(inputs, targets)


    # Load the mnis test data
    test_data = open("./mnist_test_10.csv", "r");
    test_data_list = test_data.readlines();
    test_data.close();

    testNumber = 4

    all_values = test_data_list[testNumber].split(",");
    correct_label = int(all_values[0]);
    print("trying to guess: " + str(correct_label));
    inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01;
    outputs = nn.query(inputs);
    print("Network guessed: " + str(numpy.argmax(outputs)))


main();


def runSigmoid(number):

    return scipy.special.expit(number);