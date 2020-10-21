def outer_contour(image):
    """ Extract the outer contour of image using Canny.
        
    Args:
        image(numpy.ndarray): RGBA image in cv2 format to be process.
        
    Returns:
        canvas(numpy.ndarray): contours depicted on empty canvas(removed original pixel), in cv2 format.
    """
    edge_output = cv2.Canny(cv2.split(image)[-1], 85, 255)
    canvas = np.ones_like(image).astype(np.uint8)*255
    contours, _ = cv2.findContours(edge_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):
        cv2.drawContours(canvas, contours, i, (220,20,60,255), 1,lineType=cv2.LINE_AA)
    return canvas
