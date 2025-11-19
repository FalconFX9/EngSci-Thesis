from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Load a model
model = YOLO("yolo11m-obb.pt")  # load an official model

# Predict with the model
results = model("./dish_spoon_simple.jpg") 

def draw_rotated_rectangle(ax, center, width, height, angle, label, confidence):
    # Calculate the rectangle's 4 corner points
    rect = np.array([
        [-width / 2, -height / 2],
        [ width / 2, -height / 2],
        [ width / 2,  height / 2],
        [-width / 2,  height / 2]
    ])
    
    # Rotate and translate rectangle points to the center and angle
    rotation_matrix = cv2.getRotationMatrix2D((0, 0), angle * 180 / np.pi, 1)
    rotated_rect = cv2.transform(rect[None, :, :], rotation_matrix)[0]
    translated_rect = rotated_rect + np.array(center)

    # Draw the rectangle
    ax.add_patch(plt.Polygon(translated_rect, closed=True, fill=None, edgecolor='red'))
    
    # Add label with confidence
    ax.text(center[0], center[1], f"{label} ({confidence:.2f})", color='red', fontsize=12, bbox=dict(facecolor='yellow', alpha=0.5))

def plot_yolo_results(image_path, results):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    # Create a figure and axis
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.imshow(image)

    # Loop through the bounding boxes and draw them on the image
    for result in results:
        xywhr = result.obb.xywhr  # center-x, center-y, width, height, angle (radians)
        name = [result.names[cls.item()] for cls in result.obb.cls.int()]  # class name of each box
        conf = result.obb.conf  # confidence score of each box

        print(xywhr)
        center = (xywhr[0], xywhr[1])  # (center-x, center-y)
        width = xywhr[2]
        height = xywhr[3]
        angle = xywhr[4]  # in radians

        draw_rotated_rectangle(ax, center, width, height, angle, name, conf)

    # Customize the plot
    plt.axis('off')
    plt.title('YOLO Results with Oriented Bounding Boxes')
    plt.show()


plot_yolo_results("./dish_spoon_simple.jpg", results)


