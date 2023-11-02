from fastapi.templating import Jinja2Templates
from kubernetes import client, config, stream
from config import settings
from jinja2 import Environment, PackageLoader
import yaml
import hashlib
import time


def get_config():
    if settings.LOCAL:
        config.load_kube_config()
    else:
        config.load_incluster_config()


def namespace_exists(namespace):
    get_config()
    namespaces = client.CoreV1Api().list_namespace()
    for entry in namespaces.items:
        if entry.metadata.name == namespace:
            return True
    return False


def list_namespaces():
    get_config()
    namespaces = client.CoreV1Api().list_namespace()
    namespaces = [entry.metadata.name for entry in namespaces.items]
    return namespaces

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


# def create_namespace(namespace):
#     namespace = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))
#     client.CoreV1Api().create_namespace(namespace)


# def delete_namespace(namespace):
#     client.CoreV1Api().delete_namespace(namespace)

def create_configmap(namespace, configmap_body):
    config.load_kube_config()
    client.CoreV1Api().create_namespaced_config_map(
        namespace=namespace,
        body=configmap_body,
    )

def patch_configmap(namespace, configmap_body, configmap_name):
    config.load_kube_config()
    client.CoreV1Api().patch_namespaced_config_map(
        name=configmap_name, namespace=namespace, body=configmap_body
        )


def create_deployment(namespace, deployment_body):
    try:
        client.AppsV1Api().create_namespaced_deployment(
            namespace=namespace,
            body=deployment_body,
        )
    except:
        pass

def restart_deployment(namespace, deployment_body, deployment_name):
    try:
        client.AppsV1Api().create_namespaced_deployment(
            namespace=namespace,
            body=deployment_body,
        )
    except:
        deployment = client.AppsV1Api().read_namespaced_deployment(
            name=deployment_name, namespace=namespace
        )
        deployment.spec.replicas = 0
        client.AppsV1Api().patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=deployment,
        )
        time.sleep(1)
        deployment.spec.replicas = 1
        client.AppsV1Api().patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=deployment,
        )

def create_service(namespace, service_body):
    client.CoreV1Api().create_namespaced_service(
        namespace=namespace,
        body=service_body,
    )

def create_ingress(namespace, ingress_body):
    client.NetworkingV1Api().create_namespaced_ingress(
        namespace=namespace,
        body=ingress_body,
    )

def create_secret():
    pass

# def read_service_port():
#     core_v1 = client.CoreV1Api()
#     pf = stream.portforward(
#         core_v1.connect_get_namespaced_pod_portforward,
#         name, 'default',
#         ports='8000',
#     )


def deploy_allure_server(
    namespace
):
    try:
        env = Environment(loader=PackageLoader("app.controllers"))
        get_config()
        client.CoreV1Api().create_namespaced_config_map(
            namespace=namespace,
            body=yaml.load(
                env.get_template("allure/send_results.yaml").render(),
                Loader=yaml.Loader,
            ),
        )
        client.CoreV1Api().create_namespaced_config_map(
            namespace=namespace,
            body=yaml.load(
                env.get_template("allure/send_results_secure.yaml").render(),
                Loader=yaml.Loader,
            ),
        )
        client.CoreV1Api().create_namespaced_config_map(
            namespace=namespace,
            body=yaml.load(
                env.get_template("allure/environment.yaml").render(
                    SECURITY_USER="admin",
                    SECURITY_PASS="admin_password",
                    SECURITY_VIEWER_USER="viewer",
                    SECURITY_VIEWER_PASS="viewer_password",
                ),
                Loader=yaml.Loader,
            ),
        )
        client.AppsV1Api().create_namespaced_deployment(
            namespace=namespace,
            body=yaml.load(
                env.get_template("allure/deployment.yaml").render(),
                Loader=yaml.Loader,
            ),
        )
        client.CoreV1Api().create_namespaced_service(
            namespace=namespace,
            body=yaml.load(
                env.get_template("allure/service.yaml").render(
                    namespace=namespace
                ),
                Loader=yaml.Loader,
            ),
        )
    except client.exceptions.ApiException:
        pass
    return {"success": "Allure deployed"}

def launch_vc_test_suite(namespace, verifiable_credential, unsupported_features):
    get_config()
    env = Environment(loader=PackageLoader("app.controllers"))
    configmap_body = yaml.load(
        env.get_template("vc-test-suite/configmap.yaml").render(
            unsupported_features=unsupported_features,
            verifiable_credential=verifiable_credential
        ),
        Loader=yaml.Loader,
    )
    job_body = yaml.load(
        env.get_template("vc-test-suite/job.yaml").render(
            image="idlaborg/vc-test-suite:positive-0.0.3",
            ALLURE_SERVER="http://allure:5050",
            PROJECT_ID="vc-test-suite",
        ),
        Loader=yaml.Loader,
    )
    try:
        try:
            client.CoreV1Api().create_namespaced_config_map(
                namespace=namespace,
                body=configmap_body,
            )
        except:
            client.CoreV1Api().patch_namespaced_config_map(
                name="vc-test-suite",
                namespace=namespace,
                body=configmap_body,
            )
        client.BatchV1Api().create_namespaced_job(
            namespace=namespace,
            body=job_body,
        )
    except client.exceptions.ApiException:
        return False
    return True

def check_vc_test_suite(namespace):
    pass