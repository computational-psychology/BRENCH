import pickle

def save_dict(res_dict, dic_name):
    f = open(dic_name, 'wb')
    pickle.dump(res, f)
    f.close()

def load_dict(file_name):
    f = open(file_name, 'rb')
    res = pickle.load(f)
    f.close()
    return res