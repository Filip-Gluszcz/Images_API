from rest_framework import serializers
from images.models import Image
from links.models import ExpiringLink
from collections import OrderedDict
from easy_thumbnails.files import get_thumbnailer
from rest_framework.reverse import reverse
from django.utils import timezone
import random
import string


def generate_random_string(stringLength=30):
    '''
    Generate random string with specified lenght.
    '''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class ImageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Image
        fields = '__all__'


class DisabledOriginalImageLinkSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Image
        fields = ['id', 'title', 'user']


class ExpiringLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpiringLink
        fields = ['image', 'expire_after']

    def create(self, validated_data):
        '''
        Assigns an expiration date based on the specified value.
        '''
        obj = ExpiringLink.objects.create(**validated_data)
        obj.code = generate_random_string()
        obj.expiration_date = timezone.now() + timezone.timedelta(seconds=validated_data['expire_after'])
        obj.save()
        
        return obj
    

    def to_representation(self, instance):
        '''
        Returns the generated link.
        '''
        if not instance:
            return None
        
        try:
            request = self.context.get('request', None)
        except:
            return None
        
        ret = OrderedDict()

        ret['expiring_link'] = reverse('expiring_link', args=[instance.code], request=request)

        return ret
    
    
    def validate_image(self, value):
        '''
        Checks if the image passed to generate the link belongs to the user from the request.
        '''
        request = self.context.get('request', None)
        if Image.objects.filter(id=value.id, user=request.user).exists():
            return value
        else:
            raise serializers.ValidationError('Generating a link to a photo that is not your own is not allowed!')



class ThumbnailSerializer(serializers.Serializer):

    def to_representation(self, instance):
        '''
        Returns links to images corresponding to the account tier.
        '''
        if not instance:
            return None
                
        try:
            user_tier = instance.user.account.tier
        except:
            return None
        
        try:
            request = self.context.get('request', None)
        except:
            return None

        ret = OrderedDict()
        
        for thumbnail in user_tier.thumbnails.all():
            url = get_thumbnailer(instance.image).get_thumbnail({'size': (thumbnail.size, thumbnail.size), 'crop': True}).url
            ret[thumbnail.name] = request.build_absolute_uri(url)

        if user_tier.ori_img_link:
            ret['link_to_original_image'] = request.build_absolute_uri(instance.image.url)
            
        return ret