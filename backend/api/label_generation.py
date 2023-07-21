import os
import base64
import pandas as pd
import numpy as np
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, white
from energy_label import assign_energy_label
import fitz  # PyMuPDF
import qrcode

# List of all metrics to be included in the energy label
METRIC = [
    'co2_eq_emissions',
    'size',
    'downloads',
    'datasets_size'
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
parameters_x, parameters_y  = 400/1560, 200/2655
dataset_x, dataset_y  = 950/1560, 200/2655

# Mapping of label position keys to their respective attributes
# Each entry is a tuple containing: the drawing method for the text, font size, font style, x position, y position, and formatting instructions
POS_TEXT = {
    # infos that are directly taken from summary via keys
    "modelId":                                  ('drawString',        90, '-Bold', .04,  .855, None),
    "task_type":                                ('drawString',        90, '',      .04,  .815, None),
    "datasets":                                  ('drawRightString',   90, '',      .95,  .815, None),
    "downloads":                                ('drawRightString',   68, '-Bold',  downloads_x+0.11,  downloads_y-0.025,  None),
    "size":                                     ('drawRightString',   68, '-Bold',  parameters_x+0.16,  parameters_y-0.025,  ''),
    "datasets_size":                            ('drawRightString',   68, '-Bold',  dataset_x+0.15,  dataset_y-0.025,  ''),

    "co2_eq_emissions":                         ('drawRightString',   68, '-Bold',  co2_x+0.16,  co2_y-0.025,  ''),
    # infos that are extracted via methods
    'format_co2_sources':                       ('drawCentredString', 56, '',       co2_x+0.09,  co2_y-0.075,  None),
    # static infos, depending on $task
    "$CO2e per Training":                       ('drawCentredString', 56, '',       co2_x+0.09,  co2_y-0.05,  None),
    "$Downloads":                               ('drawCentredString', 56, '',       downloads_x+0.07,  downloads_y-0.05,  None),
    "format_metrics":                           ('drawCentredString', 56, '',       top_x+0.06,  top_y-0.05,  None),
    # "$Kg":                            ('drawString',        56, '',      .28,  .26,  None),
    "$Model Size":                              ('drawCentredString', 56, '',       parameters_x+0.075,  parameters_y-0.05,  None),
    "$Dataset Size":                             ('drawCentredString', 56, '',      dataset_x+0.075,  dataset_y-0.05,  None),

}


# Position of the rating labels (A, B, C, D, E)
POS_RATINGS = { char: (.66, y) for char, y in zip('ABCDE', reversed(np.linspace(.461, .727, 5))) }

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
PARTS_DIR = os.path.join(os.path.dirname(__file__), "label_design", "parts")


def format_co2_sources(summary):
    """
    Formats the CO2 sources for the energy label.

    Args:
        summary (dict): Summary dictionary containing information about the model.

    Returns:
        str: Formatted string of CO2 sources.
    """

    sources = f'Sources: {summary["source"]}'

    return sources


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


def assign_performance_metrics(summary):
    """
    Assigns the performance metrics to the label.

    Args:
        summary (dict): Summary dictionary containing information about the model.

    Returns:
        tuple: A tuple of the performance metrics.
    """

    f1, accuracy = summary['performance_metrics']['f1'], summary['performance_metrics']['accuracy']
    if not pd.isnull(accuracy) and not pd.isnull(f1):
        return 'accuracy', 'f1'
    
    if summary['performance_metrics'] is None:
        return None

    other_metrics =  {k: v for k, v in summary['performance_metrics'].items() if not pd.isnull(v) and k not in ['accuracy', 'f1']}

    metrics = list(other_metrics.items())

    if len(metrics) == 0:
        if pd.isnull(accuracy) and pd.isnull(f1):
            return 'NullMetric', 'NullMetric'
        
        return 'accuracy' if accuracy is not None else 'f1', 'NullMetric'

    if pd.isnull(accuracy) and not pd.isnull(f1) and len(metrics) > 0:
        return metrics[0][0], 'f1'
    elif not pd.isnull(accuracy) and pd.isnull(f1) and len(metrics) > 0:
        return 'accuracy', metrics[0][0]
    elif pd.isnull(accuracy) and pd.isnull(f1):
        if len(metrics) == 1:
            return metrics[0][0], 'NullMetric'
        elif len(metrics) > 1:
            return metrics[0][0], metrics[1][0]


class EnergyLabel(fitz.Document):
    """
    Class for creating an energy label.
    """

    def __init__(self, summary, metrics_ref, boundaries):
        """
        Initializes the energy label.

        Args:
            summary (dict): Summary dictionary containing information about the model.
            metrics_ref (dict): Reference metrics.
            boundaries (dict): Boundaries for the metrics.
        """
        # Make a copy of the summary
        summary = summary.copy()

        # Get the units from the summary
        units = summary['units']

        # Add task_type and datasets to the summary
        summary['task_type'] = 'Training'
        summary['datasets'] = ','.join(summary['datasets'])

        # Create a new canvas for the PDF
        canvas = Canvas("result.pdf", pagesize=C_SIZE)

        # Get the keys from the performance metrics
        keys_to_delete = list(summary['performance_metrics'].keys())

        # Remove keys from POS_TEXT to avoid overlapping text
        for key in keys_to_delete:
            if key in POS_TEXT:
                del POS_TEXT[key]

        # Get the metrics that are in COMPOUND_METRIC
        metrics = {key:value for key,value in summary.items() if key in COMPOUND_METRIC}

        # Assign energy labels and performance metrics
        frate, metric_to_rating = assign_energy_label(metrics, metrics_ref, boundaries, 'ABCDE', 'mean')
        metric1, metric2 = assign_performance_metrics(summary)

        # Add separator between metrics
        separator = ' / ' if metric1 != 'NullMetric' and metric2 != 'NullMetric' else ''
        POS_TEXT[metric1] = ('drawRightString', 68, '-Bold', top_x+0.1, top_y-0.025, '{}' + separator)
        POS_TEXT[metric2] = ('drawRightString', 68, '-Bold', top_x+0.185, top_y-0.025, '{}')

        # Add metrics to the METRIC list
        METRIC.extend([metric1, metric2])

        # Merge performance_metrics with the summary
        summary = {**summary, **summary.pop('performance_metrics')}

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
                canvas.drawInlineImage(os.path.join(PARTS_DIR, f"{icon}_{rating}.png"), posx, posy)

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
        text=canvas.beginText()
        text.setTextRenderMode(2)
        canvas._code.append(text.getCode())

        # Continue adding text to the canvas
        for key, (draw_method, fsize, style, x, y, fmt) in POS_TEXT.items():
            draw_method = getattr(canvas, draw_method)
            canvas.setFont('Helvetica' + style, fsize)

            if key in globals() and callable(globals()[key]):
                text = globals()[key](summary)

            elif key.startswith(f"format_metrics"): # Manual format for the performance metrics
                if metric1 != 'NullMetric' and metric2 != 'NullMetric':
                    text = f'{metric1} / {metric2}'
                elif metric1 == 'NullMetric' and metric2 == 'NullMetric':
                    text = '  No Performance'
                elif metric1 != 'NullMetric' or metric2 != 'NullMetric':
                    if metric1 != 'NullMetric':
                        text = metric1.replace('NullMetric', '').replace(' ', '').replace('/', '')
                    else:
                        text = metric2.replace('NullMetric', '').replace(' ', '').replace('/', '')
                      
                if metric1 == 'accuracy' and metric2 == 'f1':
                    text += '  [%]'
            elif key.startswith(f"$"): # Static text on label depending on the task type
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
                    if key in units:
                        match units[key]: # Convert units
                            case 'kg' | 'kB': 
                                text = round(float(summary[key]) / 1000,2)
                            case 't' | 'MB':
                                text = round(float(summary[key]) / 1000000,2)
                            case 'GB':
                                text = round(float(summary[key]) / 1000000000,2)
                        text = f'{text} {units[key]}'
                    else:
                        text = fmt.format(text)

                draw_method(int(C_SIZE[0] * x), int(C_SIZE[1] * y), text)
        super().__init__(stream=canvas.getpdfdata(), filetype='pdf')


    def to_encoded_image(self):
        label_bytes = self.load_page(0).get_pixmap().tobytes()
        base64_enc = base64.b64encode(label_bytes).decode('ascii')
        return 'data:image/png;base64,{}'.format(base64_enc)

