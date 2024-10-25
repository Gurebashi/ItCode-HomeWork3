from rest_framework import serializers
from shop import models
class BiographySer(serializers.ModelSerializer):
    class Meta:
        model = models.Biography
        fields = '__all__'

class PainterSer(serializers.ModelSerializer):
    biography=BiographySer()
    pictures_count = serializers.SerializerMethodField()
    class Meta:
        model = models.Painter
        fields = '__all__'
    def get_pictures_count(self,obj):
        return (models.Picture.objects.filter(author=obj).count())
class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
class StyleSer(serializers.ModelSerializer):
    class Meta:
        model = models.Style
        fields = '__all__'
class PictureSer(serializers.ModelSerializer):
    author=PainterSer()
    style=StyleSer(many=True)
    category=CategorySer()
    class Meta:
        model = models.Picture
        fields = '__all__'

