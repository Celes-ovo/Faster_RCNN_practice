import os
import glob
import json
import copy
import random
random.seed(0)

path_to_annotation = "./annotations"
path_to_images = "./val2014"
with open(os.path.join(path_to_annotation, "instances_val2014.json"), "r") as json_file:
    annotation = json.load(json_file)
test_annotation = copy.deepcopy(annotation)

# shuffle_order = list(range(0, len(annotation['annotations'])))
# random.shuffle(shuffle_order)

# img_ids = [int(ann['image_id']) for ann in annotation['annotations']] + [int(ann['image_id']) for ann in test_annotation['annotations']]

sampling_ids = []
for img_path in glob.glob(os.path.join(path_to_images, "*")):
    if len(sampling_ids) < 100:
        tmp_id = int(img_path.split('\\')[-1].replace('.jpg', '').replace('COCO_val2014_', ''))
        sampling_ids.append(tmp_id)
        continue
    else:
        os.remove(img_path)
        print(f"deleting {img_path}")

train_ann = []
test_ann = []
for ids in sampling_ids[:50]:
    for i, ann in enumerate(annotation['annotations']):
        if ann['image_id'] == ids:
            train_ann.append(annotation['annotations'][i])
            break
for ids in sampling_ids[50:]:
    for i, ann in enumerate(annotation['annotations']):
        if ann['image_id'] == ids:
            test_ann.append(annotation['annotations'][i])
            break


annotation['annotations'] = train_ann
test_annotation['annotations'] = test_ann

with open(os.path.join(path_to_annotation, "sampled_ann_train.json"), "w") as json_file:
    json.dump(annotation, json_file)

with open(os.path.join(path_to_annotation, "sampled_ann_test.json"), "w") as json_file:
    json.dump(test_annotation, json_file)

