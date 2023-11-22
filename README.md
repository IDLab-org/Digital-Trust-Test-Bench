# Digital-Trust-Test-Bench
## Getting started
Install required packages
- Python 3.11
- tmux
- kubectl
```
add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
apt install -y \
    python3.11 \
    tmux
```
[kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
Clone and open this repo in a terminal
```
git clone git@github.com:IDLab-org/Digital-Trust-Test-Bench.git
cd Digital-Trust-Test-Bench
```
Load the dtt k8s environment and test the k8s connectivity
```
export KUBECONFIG=~/.kube/dtt-dev.conf
kubectl get nodes
```
You should have a response like the following:
```
NAME    STATUS   ROLES           AGE    VERSION
node1   Ready    control-plane   245d   v1.26.2
node2   Ready    control-plane   245d   v1.26.2
node3   Ready    control-plane   245d   v1.26.2
node4   Ready    <none>          245d   v1.26.2
node5   Ready    <none>          245d   v1.26.2
node6   Ready    <none>          245d   v1.26.2
```
(Optional) Select your user's workspace
*If you never connected, you won't have a workspace availiable*
```
kubectl get ns workspace-private-{workspace_id}
```
Ensure you have the following ports availiable: **5000 5050 5432 6379 8000**

You are now ready to launch a local instance of the DTT platform!
In your terminal, launch the `start.sh` script
```
./start.sh
```

This script will do the following:
- Port-forward k8s services:
    - redis
    - postgres
    - allure server of the selected workspace
- Launch the [frontend](http://localhost:5000) & [backend](http://localhost:8000) locally

You can visit the services in your browser.
