from cartoon_filter import apply_cartoon_filter
import io
from PIL import Image

def cartoonise_using_cartoonfilter(ndarray):
    cartoonize_image_in_nympy_array = apply_cartoon_filter(ndarray)
    # chande numpy array to image format
    cartoonize_image_in_image_format = Image.fromarray(cartoonize_image_in_nympy_array)
    # change image format to bytes
    image_in_bytes_format = io.BytesIO()
    cartoonize_image_in_image_format.save(image_in_bytes_format, format='JPEG')
    image_in_bytes_format = image_in_bytes_format.getvalue()
    # load bytes into ram, so bot can send it
    user_cartoonize_image = io.BytesIO(image_in_bytes_format)
    return user_cartoonize_image