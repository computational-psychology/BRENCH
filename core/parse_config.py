import importlib

"""
If the model you want to run is not part of a python package, you need to add it to the path, so python can see it.
If the main function of your model is at location /foo/bar/my_model/main.py, then the `project_dir` should point to `/foo/bar`
and you need to specify `my_model` as package name inside the config file.

project_dir = os.path.abspath(__file__ + "/../..") -> specify the parent dir of your model (`/foo/bar` from the example above)
sys.path.append(project_dir) -> append this parent dir to path
"""

def get_main(package_name):
    # if package is in the namespace, get the main function
    try:
        main = eval(f"{package_name}.main.main")

    # otherwise, import package first and then get the main function
    except NameError:
        package = importlib.import_module(package_name)
        main = package.main.main

    return main
