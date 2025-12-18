import cv2

def display_yolo_bbox(image_path, bbox_path, output_path=None):
    """
    Display bounding boxes in YOLO format on an image.
    
    Args:
        image_path: Path to the image file
        bbox_path: Path to the YOLO format annotation file (.txt)
        output_path: Optional path to save the annotated image
    """
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image from {image_path}")
        return
    
    h, w = image.shape[:2]
    
    # Read YOLO format bounding boxes
    with open(bbox_path, 'r') as f:
        lines = f.readlines()
    
    # Draw bounding boxes
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        
        class_id = int(parts[0])
        x_center = float(parts[1]) * w
        y_center = float(parts[2]) * h
        bbox_w = float(parts[3]) * w
        bbox_h = float(parts[4]) * h
        
        # Convert center coordinates to top-left and bottom-right
        x1 = int(x_center - bbox_w / 2)
        y1 = int(y_center - bbox_h / 2)
        x2 = int(x_center + bbox_w / 2)
        y2 = int(y_center + bbox_h / 2)
        
        # Draw rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"Class {class_id}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Display image
    cv2.imshow("YOLO Bounding Boxes", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save if output path provided
    if output_path:
        cv2.imwrite(output_path, image)
        print(f"Annotated image saved to {output_path}")

# Example usage
if __name__ == "__main__":
    image_file = ".\\raw\\RAW IMAGES\\PIZZA_CUTTER\\pizzacutterraw1.jpg"
    bbox_file = ".\\labels\\PIZZA_CUTTER\\pizzacutterbinary1.txt"

    display_yolo_bbox(image_file, bbox_file)