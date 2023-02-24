from django.shortcuts import get_object_or_404
from images.models import Image
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import permissions
from .permissions import ExpiringLinkPermission
from .serializers import ImageSerializer, DisabledOriginalImageLinkSerializer, ThumbnailSerializer, ExpiringLinkSerializer


class ImageList(ListAPIView):
    '''
    List user images.
    '''
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)
        
    def get_serializer_class(self):
        original_image_link_enabled = self.request.user.account.tier.ori_img_link
        if original_image_link_enabled:
            return ImageSerializer
        else:
            return DisabledOriginalImageLinkSerializer
    

class ImageCreate(CreateAPIView):
    '''
    Create image.
    '''
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    

class ImageDetails(APIView):
    '''
    Image detail. Response contains links to images corresponding to account tier.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        image = get_object_or_404(Image, id=pk, user=request.user)
        links = ThumbnailSerializer(image, context={"request": request})

        return Response(links.data)
    

class GenerateExpiringLink(CreateAPIView):
    '''
    Generate expiring link to specified image.
    '''
    permission_classes = [permissions.IsAuthenticated, ExpiringLinkPermission]
    serializer_class = ExpiringLinkSerializer