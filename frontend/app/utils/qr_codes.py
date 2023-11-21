import qrcode
import qrcode.image.svg
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.svg import SvgPathCircleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask


def generate(data):
    qr = qrcode.QRCode(
        image_factory=qrcode.image.svg.SvgPathImage,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr = qr.make_image(module_drawer=SvgPathCircleDrawer())
    return qr.to_string(encoding="unicode")
