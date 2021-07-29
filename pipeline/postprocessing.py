import numpy as np
import matplotlib.pyplot as plt
import stimuli.papers.RHS2007 as RHS_stimuli

import stimuli

def calculate_targets_means(pipeline_dict):
    input_stimuli = pipeline_dict['input_stimuli']
    for model_name, outputs in pipeline_dict.items():
        if model_name != 'input_stimuli':
            for stim_name, output in outputs.items():
                mask = input_stimuli[stim_name]().target_mask
                img = output['image']
                masked_outputs = get_all_masked_values(img, mask)
                means = {}
                for i, masked_output in enumerate(masked_outputs):
                    means[i+1] = np.median(masked_output[masked_output.nonzero()])
                    #means[i+1] = np.mean(masked_output[masked_output.nonzero()])

                output['means'] = means
    return pipeline_dict


def get_all_masked_values(img, mask):
    imgs = []
    for i in range(1, int(mask.max())+1):
        m = mask==i
        imgs.append(get_masked_values(img,m))
    return imgs


def get_masked_values(img, mask):
    mask = mask.astype(bool)
    new_img = np.zeros(img.shape)
    new_img[mask] = img[mask]

    return new_img


def calculate_RHS_table_values(means_dict, normalization=None):
    n = len(means_dict)
    if normalization is None:
        normalization = 1

    if n==2:
        patch1 = means_dict[1]
        patch2 = means_dict[2]
        return (patch1-patch2) / normalization
    else:
        return "None"

def sort_target_patches(means_dict):
    return sorted(means_dict.items(), key=lambda kv: kv[1] )

