import argparse
import asyncio

import aiohttp
import requests
import yaml


def find_packages_by_maintainers(queried_maintainers):
    all_maintainers = requests.get(
        "https://src.fedoraproject.org/extras/pagure_bz.json"
    ).json()

    return {
        pkgname
        for pkgname, maintainers in all_maintainers["rpms"].items()
        for maintainer in maintainers
        if maintainer in queried_maintainers
    }


async def return_if_retired(pkg, semaphore, sleep=1):
    url = f'https://src.fedoraproject.org/rpms/{pkg}/blob/rawhide/f/dead.package'
    async with semaphore, aiohttp.ClientSession() as session:
        try:
            async with session.head(url) as resp:
                if resp.status == 404:
                    return
                elif resp.status == 200:
                    return pkg
                elif resp.status >= 400:
                    raise aiohttp.client_exceptions.ServerConnectionError()
        except (aiohttp.client_exceptions.ClientError, asyncio.TimeoutError):
            if sleep > 15 * 60:
                raise
            await asyncio.sleep(sleep)
            return await return_if_retired(pkg, semaphore, sleep*2)


async def get_active_packages(maintainers):
    packages_by_maintainers = find_packages_by_maintainers(maintainers)
    
    # Check which of the above set are retired
    tasks = []
    semaphore = asyncio.Semaphore(512)
    for pkg in packages_by_maintainers:
        tasks.append(asyncio.create_task(return_if_retired(pkg, semaphore)))
    done = await asyncio.gather(*tasks)
    retired_pkgs = {pkg for pkg in done if pkg}
    
    # Filter only the non-retired package from our list
    return packages_by_maintainers - retired_pkgs


def get_zuul_config():
    resp = requests.get('https://pagure.io/fedora-project-config/raw/master/f/resources/fedora-distgits.yaml')
    return yaml.safe_load(resp.text)


def list_packages_in_zuul(zuul_config):
    all_entries = zuul_config['resources']['projects']['Fedora-Distgits']['source-repositories']

    zuul_pkgnames = set()
    for entry in all_entries:
        for key in entry:
            # hack for `rpms/systemd` is not a dictionary, so it gets parsed by letters
            if len(key) == 1:
                key = entry
            # key is in format `rpms/pkg` or `tests/pkg`
            # we don't strip the prefixes because we'd lost the information down the line
            zuul_pkgnames.add(key)
    return zuul_pkgnames


def create_common_package_set(packages_by_maintainers, all_zuul_pkgs):
     # assume the newly added packages are `rpms/`
    packages_by_maintainers = {'rpms/' + pkg for pkg in packages_by_maintainers}
    common_package_set = packages_by_maintainers | all_zuul_pkgs
    if common_package_set == all_zuul_pkgs:
        # no new packages to add
        return False
    return common_package_set


def create_new_zuul_config(zuul_config, common_package_set):
    new_zuul_pkgs = []
    common_package_list = sorted(common_package_set)
    for pkg in common_package_list:
        new_zuul_pkgs.append({pkg: {'zuul/include': [], 'default-branch': 'main'}})

    zuul_config['resources']['projects']['Fedora-Distgits']['source-repositories'] = new_zuul_pkgs

    with open('new_zuul_config.yaml', 'w') as new_config_file:
        new_config_file.write(yaml.dump(zuul_config))

def generate_zuul_config(packages_by_owners):
    zuul_config = get_zuul_config()
    all_pkgs_in_zuul = list_packages_in_zuul(zuul_config)
    common_pkg_set = create_common_package_set(packages_by_owners, all_pkgs_in_zuul)
    if common_pkg_set:
        create_new_zuul_config(zuul_config, common_pkg_set)
    else:
        print("No new packages to add - no config generated")


async def main(maintainers):
    active_packages_by_owners = await get_active_packages(maintainers)
    generate_zuul_config(active_packages_by_owners)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Provide a comma-separated list of FAS maintainers/groups to bulk add to zuul.'
    )
    parser.add_argument('maintainers', type=str, nargs='+',
                        help='a comma-separated list of FAS maintainers')

    args = parser.parse_args()
    maintainers = [maintainer.strip() for maintainer in args.maintainers[0].split(',')]

    asyncio.run(main(maintainers))
