from jetson_inference import imageNet
from jetson_utils import loadImage

def predict_image_class(image_path="audio_spec.jpg"):
    """
    Classifies an image using a custom ResNet model and returns the prediction.
    
    Parameters:
        image_path (str): Path to the image file. Defaults to 'audio_spec.jpg'.
    
    Returns:
        tuple: A tuple containing the class label and confidence percentage.
    """
    try:
        # Load the recognition network with custom model and labels
        net = imageNet(model="model/voice/resnet.onnx", 
                       labels="model/voice/labels.txt", 
                       input_blob="input_0", 
                       output_blob="output_0")
        
        # Load the image
        img = loadImage(image_path)

        # Classify the image and get the top prediction
        class_id, confidence = net.Classify(img)

        # Retrieve the class label and format confidence
        class_label = net.GetClassLabel(class_id)
        confidence_percent = confidence * 100.0

        print(f"Prediction: {class_label} ({confidence_percent:.2f}%)")
        return class_label, confidence_percent

    except Exception as e:
        print(f"Error processing image '{image_path}': {e}")
        return None, 0.0

# Example usage
if __name__ == "__main__":
    result = predict_image_class()
    print(f"Result: {result}")
