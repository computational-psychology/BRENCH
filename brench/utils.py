import pickle
import csv
import matplotlib.pyplot as plt
import matplotlib
from collections import OrderedDict

def save_dict(res_dict, dic_name):
    f = open(dic_name, 'wb')
    pickle.dump(res_dict, f)
    f.close()

def load_dict(file_name):
    f = open(file_name, 'rb')
    res = pickle.load(f)
    f.close()
    return res


def size_to_px(size, dpi):
    return (size[0]*dpi[0], size[1]*dpi[1])

def px_to_size(pixel_size, dpi):
    return(pixel_size[0]/dpi, pixel_size[1]/dpi)




