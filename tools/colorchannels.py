import numpy as np
from PIL import Image

def split_cmyk(rgb_array, threshhold=1):
    data = rgb_array.astype(float) / 255
    threshold = threshhold / 255

    channel_max = data.max(2)
    channel_max[channel_max < threshold] = threshold

    k = 1 - channel_max
    c = (1 - data[:, :, 0] - k) / channel_max
    m = (1 - data[:, :, 1] - k) / channel_max
    y = (1 - data[:, :, 2] - k) / channel_max

    result = 1 - np.array([c, m, y, k])

    return tuple([(_ * 255).round().astype(np.uint8) for _ in result])


def image_to_cmyk_parts(image):
    data = np.asarray(image.convert("RGB"))
    cmyk = split_cmyk(data)

    return (Image.fromarray(_) for _ in cmyk)