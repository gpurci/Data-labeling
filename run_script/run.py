
def run_detector(detector, image, targetMan, min_score, global_var, local_var):
    tf = local_var['tf']

    image  = tf.image.convert_image_dtype(image, tf.float32)[tf.newaxis, ...]
    print('shape converted_img {}'.format(image.shape))

    _, im_height, im_width, im_channels = image.shape
    print('shape image {}'.format(image.shape))

    result = detector(image)

    result = {key:value.numpy() for key,value in result.items()}

    targetMan.new(im_height, im_width)
    for score, obj_name, coord in zip(result["detection_scores"], result["detection_class_entities"], result["detection_boxes"]) :
        if (score < min_score):
            continue
        obj_name = str(obj_name, 'UTF-8')
        ymin, xmin, ymax, xmax = coord
        x0, y0, x1, y1 = xmin * im_width, ymin * im_height, xmax * im_width, ymax * im_height
        d_new_targets = {'names'       : obj_name,
                         'description' : obj_name,
                         'rating'   : targetMan.get_default_rating(),
                         'coord x0' : x0,
                         'coord x1' : x1,
                         'coord y0' : y0,
                         'coord y1' : y1}
        targetMan.add_object(d_new_targets)

    print("Found %d objects." % len(result["detection_scores"]))
    #print(f'\n\n\n\nRESULT detection_class_entities {result["detection_class_entities"]}')
    #print(f'\n\n\n\nRESULT detection_boxes {result["detection_boxes"]}')
    print(f'\n\n\n\nRESULT {result.keys()}')

