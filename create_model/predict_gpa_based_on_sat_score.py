import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


# Load the dataset
def load_dataset(file_path):
    # Load the dataset using pandas
    data = pd.read_csv(file_path)
    x_dependent = data['SAT']
    y_independent = data['GPA']
    return x_dependent, y_independent

def create_model(train_data, target_data):
    # Create a model using linear regression
    gpa_model = LinearRegression()
    print("Training data shape: ", train_data.shape)
    reshape_train_data = train_data.values.reshape(-1, 1)
    print("Reshaped training data shape: ", reshape_train_data.shape)

    x_train, x_test, y_train, y_test = train_test_split(reshape_train_data, target_data, test_size=0.2, random_state=42)
    # Fit the model with the training data and target data
    gpa_model.fit(x_train, y_train)
    score = gpa_model.score(x_test, y_test)

    # print the coefficients of the model
    print("Coefficients: ", gpa_model.coef_)
    print(f"Intercept: {gpa_model.intercept_:.2f}")
    print(f"R^2 Score: {score:.2f}")
    return gpa_model

if __name__ == '__main__':
    X_training_data, y_target_data = load_dataset('/home/shiva/PycharmProjects/mathematics_zero_to_hero/create_model/simple_linear_regression.csv')
    gpa_model = create_model(X_training_data, y_target_data)
    predictions = gpa_model.predict([[1500], [1600], [1700], [1714]])
    for prediction in predictions:
        print(f"Predicted GPA: {prediction:.2f}")
    print(f"Predicted GPA for SAT score 1714: {predictions[3]:.2f}")