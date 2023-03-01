'''

The code snippet is used to transfer annotation file from coco format to VIA generate format

'''

import json

with open('coco_format_ann', 'r') as f:
    coco_data = json.load(f)

via_data = {}

for image in coco_data['images']:
    image_annotations = {
        'filename': image['file_name'],
        'size': -1,
        'regions': {},
        'file_attributes': {}
    }

    for annotation in coco_data['annotations']:
        if annotation['image_id'] == image['id']:
            if 'segmentation' in annotation:
                x = []
                y = []
                for i in range(0, len(annotation['segmentation'][0]), 2):
                    x.append(annotation['segmentation'][0][i])
                    y.append(annotation['segmentation'][0][i+1])
                region_attributes = {}
                if annotation['category_id'] in [category['id'] for category in coco_data['categories']]:
                    category = [category for category in coco_data['categories'] if category['id'] == annotation['category_id']][0]
                    region_attributes = {'class': category['name']}
                image_annotations['regions'][str(annotation['id'])] = {
                    'shape_attributes': {
                        'name': 'polygon',
                        'all_points_x': x,
                        'all_points_y': y
                    },
                    'region_attributes': region_attributes
                }
            else:
                x = annotation['bbox'][0]
                y = annotation['bbox'][1]
                width = annotation['bbox'][2]
                height = annotation['bbox'][3]
                region_attributes = {}
                if annotation['category_id'] in [category['id'] for category in coco_data['categories']]:
                    category = [category for category in coco_data['categories'] if category['id'] == annotation['category_id']][0]
                    region_attributes = {'class': category['name']}
                image_annotations['regions'][str(annotation['id'])] = {
                    'shape_attributes': {
                        'name': 'rect',
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height
                    },
                    'region_attributes': region_attributes
                }

    via_data[image['file_name']] = image_annotations

with open('via_format_ann.json', 'w') as f:
    json.dump(via_data, f)


# the code above has generated a new annotation file
# the code below is used to make the file more readable, and for each level key value, give it 4 indent
with open('via_format_ann.json', 'r') as f:
    data = json.load(f)

with open('readable_via_ann.json', 'w') as f:
    json.dump(data, f, indent=4)

