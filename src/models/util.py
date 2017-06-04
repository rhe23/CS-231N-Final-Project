import numpy as np
import random
import pickle

class Data:
    def __init__(self, X_train, y_train, y_train_2, X_val, y_val, y_val_2, X_test, y_test, y_test_2, mean_image):
        self.X_train = X_train
        self.y_train = y_train
        self.y_train_2 = y_train_2
        self.X_val = X_val
        self.y_val = y_val
        self.y_val_2 = y_val_2
        self.X_test = X_test
        self.y_test = y_test
        self.y_test_2 = y_test_2
        self.mean_image = mean_image
        
# Function for permuting and splitting data into training, developement, and test
def import_dataset(address, file_names, train_percent = 80, dev_percent = 10):
    SEED = 455
    random.seed(SEED)
    # Read csv file and create a list of tuples
    images = np.load(address+file_names['images'])
    images = images.astype(float)
    with open(address + file_names['subs'], 'rb') as file_2:
        subs = pickle.load(file_2)
        subs = np.array(subs)
    with open(address + file_names['dict'], 'rb') as file_3:
        dictionary = pickle.load(file_3)
    with open(address + file_names['nsfw'], 'rb') as file_4:
        nsfw = pickle.load(file_4)
        nsfw = np.array(nsfw)
    # Fix dictionary order
    dictionary = {index:subreddit for subreddit, index in dictionary.items()}
    # Mix data and split into tran, dev, and test sets
    N,W,H,C = np.shape(images)
    indices = np.arange(N)
    random.shuffle(indices)
    images = images[indices]
    subs = subs[indices]
    nsfw = nsfw[indices]
    train_end = int(train_percent*N/100)
    dev_end = train_end + int(dev_percent*N/100)
    X_train = images[:train_end]
    y_train = subs[:train_end]
    y_train_2 = nsfw[:train_end]
    X_val = images[train_end:dev_end]
    y_val = subs[train_end:dev_end]
    y_val_2 = nsfw[train_end:dev_end]
    X_test = images[dev_end:]
    y_test = subs[dev_end:]
    y_test_2 = nsfw[dev_end:]
    
    # Normalize the data: subtract the mean image
    mean_image = np.mean(X_train, axis=0)
    X_train -= mean_image
    X_val -= mean_image
    X_test -= mean_image
    
    data = Data(X_train, y_train, y_train_2, X_val, y_val, y_val_2, X_test, y_test, y_test_2, mean_image)
    
    return data, dictionary

# None class name means do not filter by class
def get_class_indices(y, dictionary, sample=5, class_name=None):
    if class_name:
        indices = [i for i in range(len(y)) if dictionary[y[i]] == class_name]
    else:
        indices = list(range(len(y)))
    random.shuffle(indices)
    return indices[:sample]
    
    