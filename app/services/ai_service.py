# app/services/ai_service.py

def detect_gesture(image):
    """
    This function will handle ML-based gesture detection.

    Right now: dummy output
    Later: replace with real model inference
    """

    # TODO: Load model and predict from image
    prediction = "A"

    confidence = 0.95  # dummy confidence

    return {
        "prediction": prediction,
        "confidence": confidence
    }