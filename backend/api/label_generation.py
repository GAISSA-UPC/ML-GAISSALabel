import os
import pandas as pd
import numpy as np
from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, white
import qrcode

# List of all metrics to be included in the energy label
METRIC = [
    'co2_eq_emissions',
    'size_efficency',
    'downloads',
    'datasets_size_efficency',
    'performance_score',
]

COMPOUND_METRIC = [
    'co2_eq_emissions',
    'size_efficency',
    'datasets_size_efficency',
    'downloads',
    'performance_score',
]

C_SIZE = (1560, 2411)

# Positions for specific elements on the label, calculated as ratios of the overall canvas size
co2_x, co2_y = 650/1560, 725/2655
downloads_x, downloads_y = 1150/1560, 725/2655  
top_x, top_y = 150/1560, 725/2655  
parameters_x, parameters_y = 400/1560, 200/2655
dataset_x, dataset_y = 950/1560, 200/2655

# Mapping of label position keys to their respective attributes
# Each entry is a tuple containing: the drawing method for the text, font size, font style, x position, y position, and formatting instructions
POS_TEXT = {
    # infos that are directly taken from summary via keys
    "modelId":                                  ('drawString',        90, '-Bold', .04,  .855, None),
    "task_type":                                ('drawString',        90, '',      .04,  .815, None),
    "datasets":                                 ('drawRightString',   90, '',      .95,  .815, None),
    "downloads":                                ('drawRightString',   68, '-Bold',  downloads_x+0.11,  downloads_y-0.025,  None),
    "size_efficency":                           ('drawRightString',   68, '-Bold',  parameters_x+0.16,  parameters_y-0.025,  ''),
    "datasets_size_efficency":                  ('drawRightString',   68, '-Bold',  dataset_x+0.15,  dataset_y-0.025,  ''),
    "co2_eq_emissions":                         ('drawRightString',   68, '-Bold',  co2_x+0.16,  co2_y-0.025,  ''),
    "performance_score":                        ('drawRightString',   68, '-Bold',  top_x+0.1, top_y-0.025, None),

    # static infos, depending on $task
    "$CO2e per Training":                       ('drawCentredString', 56, '',       co2_x+0.09,  co2_y-0.05,  None),
    "$Downloads":                               ('drawCentredString', 56, '',       downloads_x+0.07,  downloads_y-0.05,  None),
    "$Performance score":                       ('drawCentredString', 56, '',       top_x+0.06,  top_y-0.05,  None),
    "$Model Size":                              ('drawCentredString', 56, '',       parameters_x+0.075,  parameters_y-0.05,  None),
    "$Dataset Size":                            ('drawCentredString', 56, '',       dataset_x+0.075,  dataset_y-0.05,  None),

}


# Mapping of icon names to their associated metrics
ICON_NAME_TO_METRIC = {
    'CO2': 'co2_eq_emissions',
    'parameters': 'size_efficency',
    'downloads': 'downloads',
    'top': 'performance_score',
    'dataset': 'datasets_size_efficency'
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


def generate_efficency_label(summary, meanings, frate, metric_to_rating):
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

    # Draw the background and the pictograms for the metrics
    # Ratings are converted to images and drawn on the canvas
    # If the rating is null, a "nan" image is drawn
    canvas.drawInlineImage(os.path.join(PARTS_DIR, f"bg_new_logo.png"), 0, 0)
    for icon, (posx, posy) in ICON_POS.items():
        metric = ICON_NAME_TO_METRIC[icon]
        rating = metric_to_rating[metric]
        if pd.isnull(rating):
            canvas.drawInlineImage(os.path.join(PARTS_DIR, f"nan.png"), posx+50, posy)
        else:
            canvas.drawImage(os.path.join(PARTS_DIR, f"{icon}_{rating}.png"), posx, posy)

    # Position of the rating labels
    POS_RATINGS = {char: (.66, y) for char, y in zip(meanings, reversed(np.linspace(.461, .727, 5)))}

    # Draw the final rating and a QR code
    if frate is None:
        canvas.drawInlineImage(os.path.join(PARTS_DIR, f"nan.png"), POS_RATINGS['C'][0] * C_SIZE[0], POS_RATINGS['C'][1] * C_SIZE[1])
    else:
        canvas.drawInlineImage(os.path.join(PARTS_DIR, f"Rating_{frate}.png"), POS_RATINGS[frate][0] * C_SIZE[0], POS_RATINGS[frate][1] * C_SIZE[1])
    qr = create_qr()
    draw_qr(canvas, qr, 0.825 * C_SIZE[0], 0.894 * C_SIZE[1], 200)

    # Text parts are created and added to the canvas
    # If the metric is not available, it is represented as 'n.a.'
    canvas.setFillColor(black)
    canvas.setLineWidth(3)
    canvas.setStrokeColor(black)
    text = canvas.beginText()
    text.setTextRenderMode(2)
    canvas._code.append(text.getCode())

    # Continue adding text to the canvas
    for key, (draw_method, fsize, style, x, y, fmt) in POS_TEXT.items():
        draw_method = getattr(canvas, draw_method)
        canvas.setFont('Helvetica' + style, fsize)

        if key.startswith(f"$"): # Static text on label depending on the task type
            text = key.replace(f"$", "")
        elif key in summary: # Dynamic text that receives content from summary
            if key in METRIC:
                text = 'n.a.' if summary[key] is None else f'{summary[key]:4.2f}'
                if text.endswith('.'):
                    text = text[:-1]
            else:
                text = summary[key]
        else:
            text = None
        if text is not None: # Draw the text on the canvas
            if fmt is not None:
                units = summary['units']
                if key in units:
                    if units[key] in ['kg', 'kB']: # Convert units
                        text = round(float(summary[key]) / 1000,2)
                    if units[key] in ['t', 'MB']:
                        text = round(float(summary[key]) / 1000000,2)
                    if units[key] == 'GB':
                        text = round(float(summary[key]) / 1000000000,2)
                    text = f'{text} {units[key]}'
                else:
                    text = fmt.format(text)

            draw_method(int(C_SIZE[0] * x), int(C_SIZE[1] * y), text)

    canvas.save()
    pdf = buffer.getvalue()
    return pdf
