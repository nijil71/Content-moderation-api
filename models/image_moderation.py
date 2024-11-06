import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image

class ImageModerator:
    def __init__(self):
        # Initialize NSFW image detection model
        self.feature_extractor = AutoFeatureExtractor.from_pretrained("Falconsai/nsfw_image_detection")
        self.model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
    
    def analyze(self, image_path):
        try:
            image = Image.open(image_path)
            inputs = self.feature_extractor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get prediction
            predicted_label = self.model.config.id2label[probs.argmax().item()]
            confidence = probs.max().item()
            
            return {
                'safe': predicted_label == 'safe',
                'label': predicted_label,
                'confidence': round(confidence, 4)
            }
        
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")