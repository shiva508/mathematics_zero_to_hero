import numpy as np
from sklearn.linear_model import LinearRegression

# Create training data target data
def creating_train_and_target_date(min_value, max_value, size, seed):
    # NumPy's random numbers repeatable on each run
    np.random.seed(seed)

    # Create array of size 2000X2 values ranges between -1000 to 1000
    x_train = np.random.randint(min_value, max_value, size=(size, 2))

    # Create target data by adding the two columns of x_train
    y_target = x_train[:,0] + x_train[:,1]


    return x_train, y_target

# Create a model using linear regression
def create_model(train_data, target_data):

    # Create a model using linear regression
    model = LinearRegression()

    # Fit the model with the training data and target data
    model.fit(train_data, target_data)
    score = model.score(train_data, target_data)

    # print the coefficients of the model
    print("Coefficients: ", model.coef_)
    print(f"Intercept: {model.intercept_:.2f}")
    print(f"R^2 Score: {score:.2f}")
    return model

# Predict the output using the model
def predict_addition_numbers(model, validation_input_data):
    # Predict the output using the model
    prediction = model.predict(validation_input_data)
    return prediction

if __name__ == '__main__':

  X_train, Y_target =  creating_train_and_target_date(min_value=-100, max_value=100, size=2500, seed=42)
  addition_model = create_model(X_train, Y_target)
  # Create a new input data for prediction
  validation_data = np.array([[10, 20],
                              [-5, 15],
                              [30, -10],
                              [0, 0]])
  predictions = predict_addition_numbers(addition_model, validation_data)
  print("Predictions: ", predictions)
  for input_data, prediction_output in zip(validation_data, predictions):
      print(f"Input:({input_data[0]} + {input_data[1]}), Predicted Sum: {prediction_output:.2f}")


'''
"""
    Linear regression equation: y = w_1*x_1 + w_2*x_2 + b
    Where:
    (x_1, x_2) → input values
    (w_1, w_2) → weights the model learns
    (b) → bias/intercept
    (y) → predicted output

    For addition, we want:
    y = x_1 + x_2
    This means we want the model to learn:
    w_1 = 1, w_2 = 1, b = 0
    then equation becomes:
    y = 1*x_1 + 1*x_2 + 0

    What is the model actually doing?
    Suppose initially the model has randomly chosen:
    w_1 = 0.5, w_2 = 0.5, b = 2
    for x_1 = 10, x_2 = 20

    y = (0.5)*10 + (0.5)*20 + 2
      = 5 + 10 + 2
      = 17
    But the correct answer is: y = 10 + 20 = 30
    So the model is wrong.

    Calculate how bad the prediction is
    loss = (y - y_target)^2
         = (17 - 30)^2
         = (-13)^2
         = 169
    Figure out which direction to change the weights
    1. If we increase w_1, the prediction will increase
    2. If we increase w_2, the prediction will increase
    3. If we increase b, the prediction will increase
    So we need to increase w_1, w_2, and b to make the prediction closer to the target value.

    Update the parameters
    1. w_1 = w_1 + learning_rate * (y_target - y) * x_1
    2. w_2 = w_2 + learning_rate * (y_target - y) * x_2
    3. b = b + learning_rate * (y_target - y)
    Repeat the process until the loss is small enough.

    """
'''

