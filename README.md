# Zuul-config-generator

## Installation and usage

### Install via pip

1. Use pip to install the project
```
$ pip install git+https://github.com/befeleme/zuul-config-generator@main
```

2. The project contains an executable script, so make sure the installation
destination is in your PATH.
Then run the script with a comma-separated list of FAS maintainers to query
```
$ generate-zuul-config 'ksurma,@python-packagers-sig'
```

3. In the current directory there's `fedora-distgits.yaml` generated.
If there're no packages to add to the config, no new file will be created.

### Clone the repository

1. Create a new virtual environment and install the dependencies 

```
$ python -m pip install -r requirements.txt
```

2. Run the script with a comma-separated list of FAS maintainers to query
```
$ python generate_new_zuul_config.py 'ksurma,@python-packagers-sig'
```

3. In the current directory there's `fedora-distgits.yaml` generated.
If there're no packages to add to the config, no new file will be created.

## Adding to fedora-project-config

The file lives here: https://pagure.io/fedora-project-config/blob/master/f/resources/fedora-distgits.yaml

Get a local copy of that repository.
Replace `resources/fedora-distgits.yaml` with the created file.
Check the diff for correctness and send a Pull Request to `fedora-project-config`.

## Attribution

The project is licensed under MIT license.

`return_if_retired` is derived from https://pagure.io/fedora-misc-package-utilities/blob/master/f/find-orphaned-packages by @hroncok
