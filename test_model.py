import pickle
from models import NN_with_CategoryEmbedding
import math
import numpy
import sys
sys.setrecursionlimit(10000)

num_networks = 1
train_ratio = 0.97

with open('feature_train_data.pickle', 'rb') as f:
    X, y = pickle.load(f)
    num_records = len(y)

models = []
for i in range(num_networks):
    print("Fitting NN_with_CategoryEmbedding...")
    models.append(NN_with_CategoryEmbedding(train_ratio))


def evaluate_models(models, num_records):
    model0 = models[0]
    total_sqe = 0
    num_real_test = 0
    if model0.train_ratio == 1:
        return 0
    for i in range(model0.train_size, num_records):
        record = X[i]
        sales = y[i]
        if sales == 0:
            continue
        guessed_sales = numpy.mean([model.guess(record) for model in models])
        sqe = ((sales - guessed_sales) / sales) ** 2
        total_sqe += sqe
        num_real_test += 1
        if num_real_test % 1000 == 0:
            print("{}/{}".format(num_real_test, num_records - model0.train_size))
            print(sales, guessed_sales)
    result = math.sqrt(total_sqe / num_real_test)
    return result

print("Evaluate combined models...")
r = evaluate_models(models, num_records)
print(r)


with open('feature_test_data.pickle', 'rb') as f:
    test_X = pickle.load(f)

test_index = 1
with open('predictions.csv', 'w') as f:
    f.write('Id,Sales\n')
    for record in test_X:
        store_open = record[0]
        if store_open == 0:
            f.write(str(test_index) + "," + str(0) + '\n')
        else:
            guessed_sales = numpy.mean([model.guess(record) for model in models])
            f.write(str(test_index) + "," + str(guessed_sales) + '\n')
        test_index += 1
