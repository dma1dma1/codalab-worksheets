from typing import Tuple
from xmlrpc.client import Boolean
from codalab.common import BundleRuntime
from .kubernetes_runtime import KubernetesRuntime
from ..docker_utils import DEFAULT_RUNTIME, DockerRuntime


def get_runtime(runtime_name: str):
    """Gets the appropriate runtime."""
    if runtime_name == BundleRuntime.KUBERNETES.value:
        return KubernetesRuntime
    else:
        return DockerRuntime


class Runtime:
    """Base class for a runtime."""

    def get_nvidia_devices(self, use_docker=True):
        """
        Returns a Dict[index, UUID] of all NVIDIA devices available to docker

        Arguments:
            use_docker: whether or not to use a docker container to run nvidia-smi.

        Raises docker.errors.ContainerError if GPUs are unreachable,
            docker.errors.ImageNotFound if the CUDA image cannot be pulled
            docker.errors.APIError if another server error occurs
        """
        raise NotImplementedError

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
        memory_bytes=0,
        detach=True,
        tty=False,
        runtime=DEFAULT_RUNTIME,
        shared_memory_size_gb=1,
    ):
        raise NotImplementedError

    def get_container_stats(self, container):
        raise NotImplementedError

    def get_container_stats_with_docker_stats(self, container: docker.models.containers.Container):
        """Returns the cpu usage and memory limit of a container using the Docker Stats API."""
        raise NotImplementedError

    def container_exists(self, container) -> Boolean:
        raise NotImplementedError

    def check_finished(self, container) -> Tuple[Boolean, str, str]:
        """Returns (finished boolean, exitcode or None of bundle, failure message or None)"""
        raise NotImplementedError

    @wrap_exception('Unable to check Docker container running time')
    def get_container_running_time(self, container) -> int:
        raise NotImplementedError
