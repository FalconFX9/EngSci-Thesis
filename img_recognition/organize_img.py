import shutil
import os


def move_img_cat(img_path: str, label_path: str, img_dest_path: str, label_dest_path:str, cat_name: str, img_num: int) -> int:
    category_img_src_path = os.path.join(img_path, cat_name)
    category_label_src_path = os.path.join(label_path, cat_name)

    # if not os.path.exists(category_img_dest_path):
    #     os.mkdir(category_img_dest_path)
    # if not os.path.exists(category_label_dest_path):
    #     os.mkdir(category_label_dest_path)

    files = os.listdir(category_img_src_path)
    for i, filename in enumerate(files):
        if i < len(files) * 0.85:
            subset = "train"
        else:
            subset = "val"

        img_file = os.path.join(category_img_src_path, filename)
        label_file = os.path.join(category_label_src_path, filename.replace(".jpg", ".txt").replace("raw", "binary"))
        if os.path.isfile(img_file) and os.path.isfile(label_file):
            shutil.copyfile(img_file,
                        os.path.join(img_dest_path, subset, f"{img_num}.jpg".zfill(12)))

            shutil.copyfile(label_file,
                    os.path.join(label_dest_path, subset, f"{img_num}.txt".zfill(12)))
        
            img_num += 1
    
    return img_num

if __name__ == "__main__":
    IMG_DIR = ".\\raw\\RAW IMAGES"
    img_num = 0
    for img_cat in os.listdir(IMG_DIR):
        
        img_num = move_img_cat(IMG_DIR, ".\\labels\\", ".\\images", ".\\labels", img_cat, img_num)