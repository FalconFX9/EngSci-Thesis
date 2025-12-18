import os
import cv2
import math

class BBox:
    def __init__(self, cx, cy, w, h) -> None:
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h

def get_bbox(img) -> BBox:
    y_min, y_max = math.inf, -1
    x_min, x_max = math.inf, -1
    height, width = img.shape
    for y in range(height):
        for x in range(width):
            if img[y, x] != 0:
                if y < y_min:
                    y_min = y
                if y > y_max:
                    y_max = y
                if x < x_min:
                    x_min = x
                if x > x_max:
                    x_max = x
    
    center_x = (x_min + x_max)/2
    center_y = (y_min + y_max)/2

    norm_cx = center_x / width
    norm_cy = center_y / height

    bbox_width = x_max - x_min
    bbox_height = y_max - y_min

    norm_bbw = bbox_width / width
    norm_bbh = bbox_height / height

    bbox = BBox(norm_cx, norm_cy, norm_bbw, norm_bbh)
    return bbox


def write_annotation_file(filename: str, cat_name: str, cat_id: int, bbox: BBox) -> None:
    annotation_path = os.path.join(".\\labels", cat_name)
    if not os.path.exists(annotation_path):
        os.mkdir(annotation_path)

    with open(os.path.join(annotation_path, filename.replace(".png", ".txt")), "w") as f:
        f.write(f"{cat_id} {bbox.cx} {bbox.cy} {bbox.w} {bbox.h}\n")


def write_yaml(cat_ids: list[str]) -> None:
    text = "path: \ntrain: \nval: \ntest: \n\nnames:\n"
    for i, id in enumerate(cat_ids):
        text += f"  {i}: {id}\n"

    with open("dataset.yaml", "w") as f:
        f.write(text)

if __name__ == "__main__":
    cat_ids = []
    IMG_DIR = ".\\binary\\BINARY IMAGES"
    for img_cat in os.listdir(IMG_DIR):
        for img in os.listdir(os.path.join(IMG_DIR, img_cat)):
            if img_cat not in cat_ids:
                cat_ids.append(img_cat)

            cat_id = cat_ids.index(img_cat)
            img_path = os.path.join(IMG_DIR, img_cat, img)
            img_arr = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            #bbox = get_bbox(img_arr)
            #write_annotation_file(img, img_cat, cat_id, bbox)
    
    write_yaml(cat_ids)
