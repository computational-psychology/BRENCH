import matplotlib.pyplot as plt
import main

res = main.main()

fig = plt.figure(figsize=[10, 20])
M = len(res)
N = len(list(res.values())[0])

for i, (model_name, model_output) in enumerate(res.items()):
    for j, (stimulus, output) in enumerate(model_output.items()):
        index = i*N+j+1
        plt.subplot(M, N, index)
        plt.title(model_name + " - " + stimulus)
        plt.imshow(output["image"])
plt.show()