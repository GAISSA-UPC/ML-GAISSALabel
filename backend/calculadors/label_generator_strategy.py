import os
import numpy as np
from io import BytesIO

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, white
import qrcode
from PIL import Image

# Canvas size
C_SIZE = (1560, 2411)

# Directory of the label design elements
PARTS_DIR = os.path.join(os.path.dirname(__file__), "../api/label_design")


def get_position(i, total):
    """
    Function to calculate the base position of a metric in the canvas.

    Args:
        i (Integer): Index corresponding to the metric which position is wanted.
        total (Integer): Amount of metrics that will be shown on the label.

    Returns:
        Base position of the metric.
    """
    if total == 1:
        x = 780
        y = 425
    elif total == 2:
        y = 425
        if i == 0:
            x = 520
        else:   # i == 1
            x = 1040
    elif total == 3:
        if i == 0:
            x = 520
            y = 650
        elif i == 1:
            x = 1040
            y = 650
        else:   # i == 2
            x = 780
            y = 200
    elif total == 4:
        if i == 0:
            x = 520
            y = 650
        elif i == 1:
            x = 1040
            y = 650
        elif i == 2:
            x = 520
            y = 200
        else:   # i == 3:
            x = 1040
            y = 200
    elif total == 5:
        if i == 0:
            x = 260
            y = 650
        elif i == 1:
            x = 780
            y = 650
        elif i == 2:
            x = 1300
            y = 650
        elif i == 3:
            x = 520
            y = 200
        else:   # i == 4
            x = 1040
            y = 200
    else:   # total == 6
        if i == 0:
            x = 260
            y = 650
        elif i == 1:
            x = 780
            y = 650
        elif i == 2:
            x = 1300
            y = 650
        elif i == 3:
            x = 260
            y = 200
        elif i == 4:
            x = 780
            y = 200
        else:   # i == 5
            x = 1300
            y = 200

    return x / C_SIZE[0], y / C_SIZE[1]


def create_qr(url):
    """
    Creates a QR code containing a specified URL.

    Returns:
        Image: A QR code image.
    """

    qr = qrcode.QRCode(
        version=1, box_size=1, border=0,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def draw_qr(canvas, qr, x, y, width):
    """
    Draws a QR code on a canvas.

    Args:
        canvas (Canvas): A reportlab canvas.
        qr (Image): A QR code image.
        x (int): X position of the QR code.
        y (int): Y position of the QR code.
        width (int): Width of the QR code.
    """

    qr_pix = np.array(qr)
    width //= qr_pix.shape[0]
    for (i, j), v in np.ndenumerate(qr_pix):
        if v:
            canvas.setFillColor(white)
        else:
            canvas.setFillColor(black)
        canvas.rect(x + (i * width), y + int(width * qr_pix.shape[0]) - ((j + 1) * width), width, width, fill=1, stroke=0)


def generate_efficency_label(results, meanings, frate, model_name, task_type, url):
    """
    Args:
        results: For each metric to be shown on the energy label, contains its name, value, unit and image.
        meanings: Possible result's ratings.
        frate: Final rate (should be one of the meanings)
        model_name: Name of the model to which the label is generated.
        task_type: "Training" or "Inference".
        url: URL to be represented by the QR of the label.

    Returns:
        The energy label generated, in PDF format.
    """
    # Create a new canvas for the PDF
    buffer = BytesIO()
    canvas = Canvas(buffer, pagesize=C_SIZE)

    # Draw the background
    canvas.drawInlineImage(os.path.join(PARTS_DIR, f"bg_new_logo.png"), 0, 0)

    # Definition of text styles
    canvas.setFillColor(black)
    canvas.setLineWidth(3)
    canvas.setStrokeColor(black)
    text = canvas.beginText()
    text.setTextRenderMode(2)
    canvas._code.append(text.getCode())

    # Draw model's name and task type
    canvas.setFont('Helvetica-Bold', 90)
    canvas.drawString(int(C_SIZE[0] * 0.04), int(C_SIZE[1] * 0.855), model_name)
    canvas.setFont('Helvetica', 90)
    canvas.drawString(int(C_SIZE[0] * 0.04), int(C_SIZE[1] * 0.815), task_type)

    # Draw result, name and image of the metrics to the bottom of the canvas
    i = 0
    for metric, info in results.items():
        # Unpack the information of the metric
        value = str(round(info['value'], 2)) if info['value'] else ''
        unit = info['unit'] if info['value'] else ''
        image = info['image']

        # Get the base position of the information to draw
        posx, posy = get_position(i, len(results))

        # Draw result (value + unit)
        canvas.setFont('Helvetica-Bold', 68)
        result = value + ' ' + unit if unit else value
        canvas.drawCentredString(int(C_SIZE[0] * posx), int(C_SIZE[1] * (posy - 0.025)), result)

        # Draw name of the metric
        canvas.setFont('Helvetica', 54)
        canvas.drawCentredString(int(C_SIZE[0] * posx), int(C_SIZE[1] * (posy - 0.05)), metric)

        # Draw image of the metric
        if image is None:
            imageToCanvas = os.path.join(PARTS_DIR, f"nan.png")
        else:
            imageToCanvas = ImageReader(Image.open(BytesIO(image)))
        canvas.drawImage(imageToCanvas, int(C_SIZE[0] * posx - 125), int(C_SIZE[1] * posy))

        i += 1

    # Ratings are converted to images and drawn on the canvas
    # If the rating is null, a "nan" image is drawn
    """for icon, (posx, posy) in ICON_POS.items():
        metric = ICON_NAME_TO_METRIC[icon]
        rating = metric_to_rating[metric]
        if pd.isnull(rating):
            canvas.drawInlineImage(os.path.join(PARTS_DIR, f"nan.png"), posx+50, posy)
        else:
            canvas.drawImage(os.path.join(PARTS_DIR, f"{icon}_{rating}.png"), posx-125, posy)"""

    # ToDo: Refactor --------------------------------------------------------------------------------------------------

    # Position of the rating labels
    POS_RATINGS = {char: (.66, y) for char, y in zip(meanings, reversed(np.linspace(.461, .727, 5)))}

    # Draw the final rating and a QR code
    if frate is None:
        canvas.drawInlineImage(os.path.join(PARTS_DIR, f"nan.png"), POS_RATINGS['C'][0] * C_SIZE[0],
                               POS_RATINGS['C'][1] * C_SIZE[1])
    else:
        canvas.drawInlineImage(os.path.join(PARTS_DIR, f"Rating_{frate}.png"), POS_RATINGS[frate][0] * C_SIZE[0],
                               POS_RATINGS[frate][1] * C_SIZE[1])
    qr = create_qr(url)
    draw_qr(canvas, qr, 0.825 * C_SIZE[0], 0.894 * C_SIZE[1], 200)

    # ToDo: -----------------------------------------------------------------------------------------------------------

    canvas.save()
    pdf = buffer.getvalue()
    return pdf
