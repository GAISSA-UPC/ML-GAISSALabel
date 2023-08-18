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

# Positions for specific elements on the label, calculated as ratios of the overall canvas size
top_x, top_y = 260/1560, 650/2411
co2_x, co2_y = 780/1560, 650/2411
downloads_x, downloads_y = 1300/1560, 650/2411
parameters_x, parameters_y = 520/1560, 200/2411
dataset_x, dataset_y = 1040/1560, 200/2411


# Mapping of icon names to their associated metrics
ICON_NAME_TO_METRIC = {
    'CO2': 'co2_eq_emissions',
    'parameters': 'size_efficency',
    'downloads': 'downloads',
    'top': 'performance_score',
    'dataset': 'datasets_size_efficency'
}

ICON_NAMES = {
    'size_efficency': 'Size efficiency',
    'datasets_size_efficency': 'Dataset size efficency',
    'downloads': 'Descàrregues',
    'performance_score': 'Performance score',
    'co2_eq_emissions': 'CO2 emissions'
}


# Positions of the icons on the label, calculated as ratios of the overall canvas size
ICON_POS = {
    'downloads': (downloads_x*1560, downloads_y*2411),
    'top': (top_x*1560, top_y*2411),
    'CO2': (co2_x*1560, co2_y*2411),
    'parameters': (parameters_x*1560, parameters_y*2411),
    'dataset': (dataset_x*1560, dataset_y*2411)
}


# Directory of the label design elements
PARTS_DIR = os.path.join(os.path.dirname(__file__), "label_design")


def get_position(i, total):
    if i == 0:
        return 260 / 1560, 650 / 2411
    elif i == 1:
        return 780 / 1560, 650 / 2411
    elif i == 2:
        return 1300 / 1560, 650 / 2411
    elif i == 3:
        return 520 / 1560, 200 / 2411
    else:
        return 1040 / 1560, 200 / 2411


def create_qr():
    """
    Creates a QR code containing a specified URL.

    Returns:
        Image: A QR code image.
    """

    url = 'https://gaissa.upc.edu/en'
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


def generate_efficency_label(results, meanings, frate, model_name, task_type):
    """
    Args:
        summary (dict): Summary dictionary containing information about the model.
        metrics_ref (dict): Reference metrics.
        boundaries (dict): Boundaries for the metrics.
        meanings (array): Possible result's ratings.
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
        value = str(round(info['value'], 2))
        unit = info['unit']
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
        canvas.drawImage(ImageReader(Image.open(BytesIO(image))), int(C_SIZE[0] * posx - 125), int(C_SIZE[1] * posy))

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
    qr = create_qr()
    draw_qr(canvas, qr, 0.825 * C_SIZE[0], 0.894 * C_SIZE[1], 200)

    # ToDo: -----------------------------------------------------------------------------------------------------------

    canvas.save()
    pdf = buffer.getvalue()
    return pdf
