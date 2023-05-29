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

3. Explore the generated file `new_zuul_config.yaml`. If there're no packages to add to the config, no new file will be created.

## Adding to fedora-project-config

The file lives here: https://pagure.io/fedora-project-config/blob/master/f/resources/fedora-distgits.yaml

To commit to fedora-project-config edit the generated file to match the formatting of the actual config.

I do this: open `fedora-distgits.yaml` in another tab of my editor and:
- fix indentation of the rpms
- fix ordering of the dictionary entries
- fix `rpms/systemd` - remove `:` and:
```
         zuul/include: []
         default-branch: main
```

Then I run `meld` on the two files and eyball whether they visually match - only the new entries should be in the diff


## Attribution

`return_if_retired` is derived from https://pagure.io/fedora-misc-package-utilities/blob/master/f/find-orphaned-packages by @hroncok
