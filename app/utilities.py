import qrcode
from qrcode.image.styles.moduledrawers.svg import SvgPathCircleDrawer
import json, requests, secrets, hashlib


def check_workspace(workspace_id):
    pass
# Create workspace
# Provision secrets
# Provision reporting
# Provision backchannels

def generate_qrcode(data):
    qr = qrcode.QRCode(image_factory=qrcode.image.svg.SvgPathImage, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)
    qr.make(fit=True)
    qr = qr.make_image(module_drawer=SvgPathCircleDrawer())
    return qr.to_string(encoding='unicode')

def generate_workspace_id(label, type):
    if type not in ["private", "shared", "public"]:
        return None
    workspace_id = f'workspace-{type}-{label}'
    return workspace_id