#! /bin/bash

# apt install -y tmux

tmux kill-session -t dtt
tmux new-session -d -s dtt

# tmux rename-window 'Allure'
# tmux send-keys 'kdtt-dev && \
#                 kubectl port-forward svc/allure 5050:5050' 'C-m'

# tmux split-window -v
tmux rename-window 'Redis'
tmux send-keys 'kdtt-dev && \
                kubectl port-forward -n dtt-storage svc/redis 6379:6379' 'C-m'

tmux split-window -v
tmux rename-window 'Frontend'
tmux send-keys 'cd DTT-Frontend && \
                . venv/bin/activate && \
                python start.py' 'C-m'

tmux split-window -v
tmux rename-window 'Backend'
tmux send-keys 'kdtt-dev && \
                cd DTT-Service && \
                . venv/bin/activate && \
                uvicorn main:app --reload --host 0.0.0.0 --port 8000' 'C-m'

tmux attach -t dtt