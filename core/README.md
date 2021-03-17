The pipeline is very basic at the moment, but it kinda works. You can specify the names of models you want to run (they have to be exactly the same as the names of classes in multyscale/models.py) and the input stimuli.  
The input stimuli are located in /stimuli directory. At the moment only example_stimulus.png is working because the others (Lynn's ones) have uncompatible resolution with the multyscale models.  
You can specify the models and the stimuli in main() function inside core/main.py and you can run the whole thing with by running the `core/main.py` file.
