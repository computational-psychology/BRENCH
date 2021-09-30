import pickle
import os


def save_raw_model_output(model_output, out):
    # TODO use pathlib
    head, tails = os.path.split(out)
    if not os.path.isdir(head) and head != "":
        os.makedirs(head)
    save_dict(model_output, out)


def save_dict(res_dict, dic_name):
    f = open(dic_name, "wb")
    pickle.dump(res_dict, f)
    f.close()


def load_dict(file_name):
    f = open(file_name, "rb")
    res = pickle.load(f)
    f.close()
    return res


def size_to_px(size, dpi):
    return (size[0] * dpi[0], size[1] * dpi[1])


def px_to_size(pixel_size, dpi):
    return (pixel_size[0] / dpi, pixel_size[1] / dpi)
