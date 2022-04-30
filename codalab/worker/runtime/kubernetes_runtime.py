import logging
from typing import Any, Dict, Tuple
from kubernetes import client, utils  # type: ignore
from kubernetes.utils.create_from_yaml import FailToCreateError  # type: ignore
from urllib3.exceptions import MaxRetryError, NewConnectionError  # type: ignore

from codalab.worker.docker_utils import DEFAULT_RUNTIME
from codalab.common import BundleRuntime
from codalab.worker.runtime import Runtime

logger: logging.Logger = logging.getLogger(__name__)

# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#create-pod-v1-core

removeprefix = lambda l, p: l[len(p) :]


class KubernetesRuntime(Runtime):
    """Runtime that launches Kubernetes pods."""

    @property
    def name(self) -> str:
        return BundleRuntime.KUBERNETES.value

    def __init__(self, work_dir: str, auth_token: str, cluster_host: str, cert_path: str):
        # Configure and initialize Kubernetes client
        self.work_dir = work_dir

        # TODO: Unify this code with the client setup steps in kubernetes_worker_manager.py
        configuration: client.Configuration = client.Configuration()
        configuration.api_key_prefix['authorization'] = 'Bearer'
        configuration.api_key['authorization'] = auth_token
        configuration.host = cluster_host
        configuration.ssl_ca_cert = cert_path
        if configuration.host == "https://codalab-control-plane:6443":
            # Don't verify SSL if we are connecting to a local cluster for testing / development.
            configuration.verify_ssl = False
            configuration.ssl_ca_cert = None
            del configuration.api_key_prefix['authorization']
            del configuration.api_key['authorization']
            configuration.debug = False

        self.k8_client: client.ApiClient = client.ApiClient(configuration)
        self.k8_api: client.CoreV1Api = client.CoreV1Api(self.k8_client)

    def get_nvidia_devices(self, use_docker=True):
        """
        Returns a Dict[index, UUID] of all NVIDIA devices available to docker

        Arguments:
            use_docker: whether or not to use a docker container to run nvidia-smi.

        Raises docker.errors.ContainerError if GPUs are unreachable,
            docker.errors.ImageNotFound if the CUDA image cannot be pulled
            docker.errors.APIError if another server error occurs
        """
        return {}

    def get_container_ip(self, network_name, container):
        raise NotImplementedError

    def start_bundle_container(
        self,
        bundle_path,
        uuid,
        dependencies,
        command,
        docker_image,
        network=None,
        cpuset=None,
        gpuset=None,
        request_cpus=0,
        request_gpus=0,
        memory_bytes=0,
        detach=True,
        tty=False,
        runtime=DEFAULT_RUNTIME,
        shared_memory_size_gb=1,
    ):
        if not command.endswith(';'):
            command = '{};'.format(command)
        # Explicitly specifying "/bin/bash" instead of "bash" for bash shell to avoid the situation when
        # the program can't find the symbolic link (default is "/bin/bash") of bash in the environment
        command = ['/bin/bash', '-c', '( %s ) >stdout 2>stderr' % command]
        working_directory = '/' + uuid
        container_name = 'codalab_run_%s' % uuid
        config: Dict[str, Any] = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {'name': container_name},
            'spec': {
                'containers': [
                    {
                        'name': container_name,
                        'image': docker_image,
                        'command': command,
                        'workingDir': working_directory,
                        'env': [
                            {'name': 'HOME', 'value': working_directory},
                            {'name': 'CODALAB', 'value': 'true'},
                        ],
                        'resources': {
                            'limits': {
                                'cpu': request_cpus,
                                'memory': memory_bytes,
                                # 'nvidia.com/gpu': request_gpus,  # Configure NVIDIA GPUs
                            }
                        },
                        # Mount only the needed dependencies as read-only and the working directory of the bundle,
                        # rather than mounting all of self.work_dir.
                        'volumeMounts': [
                            {
                                'name': 'workdir',
                                'mountPath': working_directory,
                                'subPath': removeprefix(bundle_path, self.work_dir),
                            }
                        ]
                        + [
                            {
                                'name': 'workdir',
                                'mountPath': mounted_dep_path,
                                'subPath': removeprefix(dep_path, self.work_dir),
                            }
                            for dep_path, mounted_dep_path in dependencies
                        ],
                    }
                ],
                'volumes': [{'name': 'workdir', 'hostPath': {'path': self.work_dir}},],
                'restartPolicy': 'Never',  # Only run a job once
            },
        }
        print("config", config)
        logger.warn('Starting job {} with image {}'.format(container_name, docker_image))
        try:
            output = utils.create_from_dict(self.k8_client, config)
            print(output)
        except (client.ApiException, FailToCreateError, MaxRetryError, NewConnectionError) as e:
            logger.error(f'Exception when calling Kubernetes utils->create_from_dict: {e}')

    def get_container_stats(self, container):
        raise NotImplementedError

    def get_container_stats_with_docker_stats(self, container):
        """Returns the cpu usage and memory limit of a container using the Docker Stats API."""
        raise NotImplementedError

    def container_exists(self, container) -> bool:
        raise NotImplementedError

    def check_finished(self, container) -> Tuple[bool, str, str]:
        """Returns (finished boolean, exitcode or None of bundle, failure message or None)"""
        raise NotImplementedError

    def get_container_running_time(self, container) -> int:
        raise NotImplementedError
