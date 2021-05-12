import matplotlib.pyplot as plt
import main
import matplotlib

res = main.main()

fig = plt.figure(figsize=[10, 20])
M = len(res)
N = len(list(res.values())[0])

matplotlib.rcParams.update({'font.size': 8})
plt.figure(figsize=(25, 15))

for i, (model_name, model_output) in enumerate(res.items()):
    for j, (stimulus, output) in enumerate(model_output.items()):
        index = i+j*M+1
        plt.subplot(N, M, index)
        plt.title(model_name + " - " + stimulus)
        plt.imshow(output["image"], cmap='coolwarm')
        plt.colorbar()
plt.show()
