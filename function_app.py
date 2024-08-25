import azure.functions as func
import logging
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials


# Create a Computer Vision client
cv_endpoint = os.environ["COMPUTER_VISION_ENDPOINT"]
cv_key = os.environ["COMPUTER_VISION_KEY"]
credentials = CognitiveServicesCredentials(cv_key)
computer_vision_client = ComputerVisionClient(cv_endpoint, credentials)

app = func.FunctionApp()


def log_description(description):
    if description.captions:
        for caption in description.captions:
            logging.info(
                f"Description: {caption.text} (confidence: {caption.confidence * 100:.2f}%)"
            )
    else:
        logging.info("No description available for this image.")


def log_tags(tags):
    if tags:
        tags = ", ".join([tag.name for tag in tags])
        logging.info(f"Tags: {tags}")
    else:
        logging.info("No tags available for this image.")


def log_objects(objects):
    if objects:
        objects = ", ".join([obj.object_property for obj in objects])
        logging.info(f"Objects: {objects}")
    else:
        logging.info("No objects detected in this image.")


def log_colors(colors):
    if colors:
        dominant_colors = ", ".join(color for color in colors.dominant_colors)
        accent_color = colors.accent_color
        background_color = colors.dominant_color_background
        foreground_color = colors.dominant_color_foreground
        logging.info(
            f"Color story: dominant colors: {dominant_colors}, accent color: {accent_color}, background color: {background_color}, foreground color: {foreground_color}"
        )
    else:
        logging.info("No color analysis available for this image.")


def log_image_type(image_type):
    if image_type:
        clip_art = image_type.clip_art_type
        line_art = image_type.line_drawing_type
        logging.info(f"Image type results: clip art: {clip_art}, line art: {line_art}")
    else:
        logging.info("No image type analysis available for this image.")


@app.blob_trigger(
    arg_name="myblob", path="imageanalysis/{name}", connection="AzureWebJobsStorage"
)
def image_blob_trigger(myblob: func.InputStream):
    logging.info(
        f"Python blob trigger function processed blob"
        f"Name: {myblob.name}"
        f"Blob Size: {myblob.length} bytes"
    )

    try:
        # Analyze image for visual features
        image_analysis = computer_vision_client.analyze_image_in_stream(
            myblob,
            visual_features=[
                VisualFeatureTypes.description,
                VisualFeatureTypes.tags,
                VisualFeatureTypes.objects,
                VisualFeatureTypes.color,
                VisualFeatureTypes.image_type,
            ],
        )
        log_description(image_analysis.description)
        log_tags(image_analysis.tags)
        log_objects(image_analysis.objects)
        log_colors(image_analysis.color)
        log_image_type(image_analysis.image_type)

    except Exception as e:
        logging.error(f"Error processing blob: {str(e)}")
