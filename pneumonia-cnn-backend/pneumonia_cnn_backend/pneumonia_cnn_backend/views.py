from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.decorators import api_view
from PIL import Image
from .cnn_model.code.predict_image import predict

@api_view(['POST'])
def scan_image(request):
    """
    Handles the CT scan of a chest to determine if it has pneumonia or not
    """

    if request.method == "POST":
        # Do stuff
        all_files = request.FILES
        scan_image = all_files.get('scan_image')

        refactored_image = Image.open(scan_image)
        has_pneumonia, probability = predict(refactored_image)
        print(has_pneumonia, probability)

        if probability < 0:
            return JsonResponse({"error": "Model weights cannot be fine"}, status=400)
        else:
            return JsonResponse({"scan_output" : has_pneumonia}, status=200)

    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)

