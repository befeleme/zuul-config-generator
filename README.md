# Zuul-config-generator

## Usage

1. Create a new virtual environment and install the dependencies 

```
$ python -m pip install -r requirements.txt
```

2. Run the script with a comma-separated list of FAS maintainers to query
```
$ python generate_new_zuul_config.py 'ksurma,@python-packagers-sig'
```

3. Explore the generated file `fedora-distgits.yaml`. If there're no packages to add to the config, no new file will be created.

## Adding to fedora-project-config

The file lives here: https://pagure.io/fedora-project-config/blob/master/f/resources/fedora-distgits.yaml

Get a local copy of that repository.
Replace `resources/fedora-distgits.yaml` with the created file.
Check the diff for correctness and send a Pull Request to `fedora-project-config`.

## Attribution

`return_if_retired` is derived from https://pagure.io/fedora-misc-package-utilities/blob/master/f/find-orphaned-packages by @hroncok
