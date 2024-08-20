import os
import cv2
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .models import Worker, Fingerprint
from django.core.files.storage import default_storage

def calculate_sift_flann_similarity(image1, image2):
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(image1, None)
    kp2, des2 = sift.detectAndCompute(image2, None)

    if des1 is None or des2 is None:
        return 0

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    similarity = len(good_matches) / max(len(kp1), len(kp2))
    return similarity

class MatchFingerprintView(APIView):
    def post(self, request, *args, **kwargs):
        # Save the new fingerprint image temporarily
        new_fp_image = request.FILES.get('image')
        new_fp_path = os.path.join(settings.MEDIA_ROOT, 'temp_fingerprint.jpg')
        with default_storage.open(new_fp_path, 'wb+') as destination:
            for chunk in new_fp_image.chunks():
                destination.write(chunk)

        new_image = cv2.imread(new_fp_path, cv2.IMREAD_GRAYSCALE)
        if new_image is None:
            return Response({"message": "Error: New fingerprint image could not be loaded."}, status=400)

        max_similarity = 0
        best_match_worker = None

        for worker in Worker.objects.prefetch_related('fingerprints'):
            for fingerprint in worker.fingerprints.all():
                fp_image_path = os.path.join(settings.MEDIA_ROOT, fingerprint.image.name)
                existing_image = cv2.imread(fp_image_path, cv2.IMREAD_GRAYSCALE)
                similarity = calculate_sift_flann_similarity(new_image, existing_image)

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match_worker = worker

        threshold = 0.07
        if max_similarity < threshold:
            return Response({
                "message": "No match!",
                "status": "Not Found"
            }, status=404)
        else:
            return Response({
                "worker_name": best_match_worker.name,
                "similarity_percentage": max_similarity * 100,
                "status": "Found",
            })