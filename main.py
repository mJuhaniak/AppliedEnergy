from scipy.stats import entropy
import pandas as pd


# Creates a new column in dataset with a desired format,
# set argument to 1 if column´s type is datetime,
# set argument to 2 if column´s type is int,
# coefficient is optional parameter for changing units of int(if argument = 2)
def prepare_data(dataset, column_name, column_name_new, argument, coefficient=1):
    if argument == 1:
        dataset[column_name_new] = pd.to_datetime(dataset[column_name]).dt.hour
    elif argument == 2:
        dataset[column_name_new] = round(dataset[column_name] * coefficient)


# Returns a 2D matrix from 2 columns with number of occurences
def create_sparsity_matrix(dataset, column_name1, column_name2):
    sparsity_matrix = dataset.groupby(column_name1)[column_name2].value_counts().unstack(column_name2,
                                                                                         fill_value=0).reset_index()
    sparsity_matrix.drop(sparsity_matrix.columns[0], axis=1, inplace=True)
    sparsity_matrix.to_csv("sparsityMatrix.csv", sep=';')
    return sparsity_matrix


# Returns sparsity of a matrix
def compute_sparsity(sparsity_matrix):
    matrix_zeros = (sparsity_matrix == 0).sum().sum()
    sparsity = matrix_zeros / (sparsity_matrix.shape[0] * sparsity_matrix.shape[1])
    return sparsity


# Returns entropy of dataset based on sparsity matrix
def compute_entropy(sparsity_matrix):
    counts = sparsity_matrix.to_numpy().flatten(order='C')
    return entropy(counts, base=2)


if __name__ == '__main__':
    dataset_ = pd.read_csv(r"C:\Users\mjuha\Desktop\Prax_data\Data\PaloAlto_modified.csv", low_memory=False)
    column1_name_ = 'Start Date'
    column2_name_ = 'Charging Time (hh:mm:ss)'
    column1_name_new_ = 'NewCol1'
    column2_name_new_ = 'NewCol2'

    prepare_data(dataset_, column1_name_, column1_name_new_, 1)
    prepare_data(dataset_, column2_name_, column2_name_new_, 2, 1/3600)
    sparsity_matrix_ = create_sparsity_matrix(dataset_, column1_name_new_, column2_name_new_)
    sparsity_ = compute_sparsity(sparsity_matrix_)
    entropy_ = compute_entropy(sparsity_matrix_)
    print('SD:')
    print(sparsity_)
    print(entropy_)

    column1_name_ = 'Charging Time (hh:mm:ss)'
    column2_name_ = 'Energy (kWh)'

    prepare_data(dataset_, column1_name_, column1_name_new_, 2, 1/3600)
    prepare_data(dataset_, column2_name_, column2_name_new_, 2)
    sparsity_matrix_ = create_sparsity_matrix(dataset_, column1_name_new_, column2_name_new_)
    sparsity_ = compute_sparsity(sparsity_matrix_)
    entropy_ = compute_entropy(sparsity_matrix_)
    print('DE:')
    print(sparsity_)
    print(entropy_)
