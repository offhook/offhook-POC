import json
from os.path import join, abspath, dirname
import docker
from docker.types import Mount


HOST_CURRENT_DIR = abspath(dirname(__file__))
CONTAINER_BASE_DIR = '/opt/offhook'
ENVIRONMENTS_FILE_PATH = join(HOST_CURRENT_DIR, 'download_environments.json')
CONTAINER_DL_DIR_KEY = 'DOWNLOAD_DIR'
CONTAINER_DL_DIR_VALUE = CONTAINER_BASE_DIR + '/packages'
CONTAINER_ENV = {CONTAINER_DL_DIR_KEY: CONTAINER_DL_DIR_VALUE}
HOST_DL_DIR = join(HOST_CURRENT_DIR, 'packages')
DL_DIR_MOUNT = Mount(CONTAINER_DL_DIR_VALUE, HOST_DL_DIR, type='bind', read_only=False)

HOST_DL_SCRIPTS_PATH = join(HOST_CURRENT_DIR, 'download_scripts')
CONTAINER_DL_SCRIPT_PATH = CONTAINER_BASE_DIR + '/download'


def read_environments(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def build_mounts_list(env_details):
    mounts = [
        Mount(CONTAINER_BASE_DIR + '/' + file,
              join(HOST_DL_SCRIPTS_PATH, file),
              type='bind',
              read_only=True)
        for file
        in env_details['additional_files']
    ]

    mounts.append(DL_DIR_MOUNT)
    mounts.append(
        Mount(CONTAINER_DL_SCRIPT_PATH,
              join(HOST_DL_SCRIPTS_PATH, env_details['script']),
              type='bind',
              read_only=True)
    )

    return mounts


def download_packages(packages, env_details):
    # TODO: Sanitize "packages" input
    client = docker.from_env()
    client.containers.run(
        image=env_details['image'],
        command=CONTAINER_DL_SCRIPT_PATH + ' ' + packages,
        auto_remove=False,  # TODO: Later change to saving the logs and then deleting the container
        environment=CONTAINER_ENV,
        mounts=build_mounts_list(env_details),
        working_dir=CONTAINER_BASE_DIR,
    )


dl_envs = read_environments(ENVIRONMENTS_FILE_PATH)
download_packages('nano', dl_envs['centos7'])
