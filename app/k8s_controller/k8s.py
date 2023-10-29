from kubernetes import client, config
from config import settings
from jinja2 import Environment, PackageLoader
import yaml
import hashlib


def get_config():
    config.load_kube_config()
    # try:
    #     config.load_kube_config()
    # except:
    #     config.load_incluster_config()


def namespace_exists(namespace):
    get_config()
    namespaces = client.CoreV1Api().list_namespace()
    for entry in namespaces.items:
        if entry.metadata.name == namespace:
            return True
    return False

def create_namespace(namespace):
    get_config()
    if namespace_exists(namespace):
        return "Namespace exists"
    ns = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))
    client.CoreV1Api().create_namespace(ns)
    return "Namespace created"

def delete_namespace(namespace):
    get_config()
    if not namespace_exists(namespace):
        return "Namespace doesn't exists"
    client.CoreV1Api().delete_namespace(namespace)
    return "Namespace deleted"


def list_backchannels(namespace):
    get_config()
    backchannels = []
    deployments = client.AppsV1Api().list_namespaced_deployment(namespace=namespace)
    for deployment in deployments.items:
        if "backchannel" in deployment.metadata.name:
            backchannels.append(deployment.metadata.name.split("-")[-1])
    return backchannels


def deploy_backchannel(
    agent_label, agent_framework, ledger_url, tails_url, namespace
):
    backchannel_id = hashlib.md5(agent_label.encode("utf-8")).hexdigest()
    env = Environment(loader=PackageLoader("app.controller"))
    try:
        get_config()
        client.CoreV1Api().create_namespaced_config_map(
            namespace=namespace,
            body=yaml.load(
                env.get_template("backchannels/configmap.yaml").render(
                    backchannel_id=backchannel_id,
                    agent_label=agent_label,
                    base_domain=settings.DOMAIN,
                    ledger_url=ledger_url,
                    tails_url=tails_url,
                    cloud_agency_url="",
                    aip_config="10",
                ),
                Loader=yaml.Loader,
            ),
        )
        client.AppsV1Api().create_namespaced_deployment(
            namespace=namespace,
            body=yaml.load(
                env.get_template("backchannels/deployment.yaml").render(
                    backchannel_id=backchannel_id,
                    framework=agent_framework,
                    image=settings.BACKCHANNELS[agent_framework]["image"],
                    command=settings.BACKCHANNELS[agent_framework]["command"],
                    args=settings.BACKCHANNELS[agent_framework]["args"],
                ),
                Loader=yaml.Loader,
            ),
        )
        client.CoreV1Api().create_namespaced_service(
            namespace=namespace,
            body=yaml.load(
                env.get_template("backchannels/service.yaml").render(
                    backchannel_id=backchannel_id
                ),
                Loader=yaml.Loader,
            ),
        )
        client.NetworkingV1Api().create_namespaced_ingress(
            namespace=namespace,
            body=yaml.load(
                env.get_template("backchannels/ingress.yaml").render(
                    backchannel_id=backchannel_id,
                    base_domain=settings.DOMAIN,
                ),
                Loader=yaml.Loader,
            ),
        )
    except client.exceptions.ApiException:
        return {"error": "Kubernetes client error, maybe a ressource already exists"}
    return {"success": "Backchannel deployed", "backchannel_id": backchannel_id}


def remove_backchannel(backchannel_id, namespace):
    try:
        get_config()
        client.CoreV1Api().delete_namespaced_config_map(
            namespace=namespace,
            name=f"backchannel-{backchannel_id}-env",
        )
        client.AppsV1Api().delete_namespaced_deployment(
            namespace=namespace,
            name=f"backchannel-{backchannel_id}",
        )
        client.CoreV1Api().delete_namespaced_service(
            namespace=namespace,
            name=f"backchannel-{backchannel_id}-svc",
        )
        client.NetworkingV1Api().delete_namespaced_ingress(
            namespace=namespace,
            name=f"backchannel-{backchannel_id}-ingress",
        )
    except client.exceptions.ApiException:
        return {"error": "Kubernetes client error, maybe a ressource is missing"}

    return {"success": "Backchannel removed"}
