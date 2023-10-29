from fastapi.templating import Jinja2Templates
from kubernetes import client, config
from config import settings
from jinja2 import Environment, PackageLoader
import yaml, json
import hashlib

def deploy_init(namespace):
    config.load_kube_config()
    env = Environment(loader=PackageLoader("app.k8s_controller"))
    client.CoreV1Api().create_namespaced_config_map(
        namespace=namespace,
        body=yaml.load(
            env.get_template("vc-test-suite/send_results_secure.yaml").render(),
            Loader=yaml.Loader,
        ),
    )

def run_vc_validator(verifiable_credential, sections_not_suppored):
    config.load_kube_config()
    env = Environment(loader=PackageLoader("app.k8s_controller"))
    namespace = "module-w3c"
    test_config = {
      "generator":"cat",
      "presentationGenerator":"cat",
      "generatorOptions":"input.jsonld",
      "sectionsNotSupported": sections_not_suppored
    }
    configmap = yaml.load(
            env.get_template("vc-test-suite/configmap.yaml").render(
                test_config=json.dumps(test_config),
                test_input=json.dumps(verifiable_credential)
            ),
            Loader=yaml.Loader,
        )
    print(configmap)
    # client.CoreV1Api().create_namespaced_config_map(
    #     namespace=namespace,
    #     body=yaml.load(
    #         env.get_template("vc-test-suite/configmap.yaml").render(
    #             sections_not_suppored=sections_not_suppored,
    #             verifiable_credential=verifiable_credential
    #         ),
    #         Loader=yaml.Loader,
    #     ),
    # )
    # client.CoreV1Api().create_namespaced_config_map(
    #     namespace=namespace,
    #     body=yaml.load(
    #         env.get_template("vc-test-suite/configmap.yaml").render(
    #             sections_not_suppored=sections_not_suppored,
    #             verifiable_credential=verifiable_credential
    #         ),
    #         Loader=yaml.Loader,
    #     ),
    # )