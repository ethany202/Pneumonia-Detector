from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.decorators import api_view
from PIL import Image
from .cnn_model.code.predict_image import predict
from .settings import MEDIA_URL, MEDIA_ROOT
# from .models import SaliencyImage
from .models.saliency_image import SaliencyImage

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
        has_pneumonia, probability = predict(refactored_image, MEDIA_ROOT)
        print(has_pneumonia, probability)

        if probability < 0:
            return JsonResponse({"error": "Model weights cannot be found"}, status=400)
        else:
            return JsonResponse({"scan_output" : has_pneumonia}, status=200)

    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)

def serve_image(request, image_id):
    print("Serving Image")
    try:
        image = SaliencyImage.objects.get(id=image_id)
        with open(image.image.path, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except Image.DoesNotExist:
        return HttpResponse(status=404)