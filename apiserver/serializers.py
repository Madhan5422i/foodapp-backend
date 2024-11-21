from rest_framework.serializers import ModelSerializer,SerializerMethodField,StringRelatedField
from .models import Explore_menu,item_List,CusUser,Address
# from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

class Explore_menu_serializer(ModelSerializer):
    """
    Serializer class for Explore_menu model.
    """
    food_image = SerializerMethodField('get_food_image')
    
    class Meta:
        model = Explore_menu
        fields = '__all__'
    
    def get_food_image(self, obj):
        """
        Method to get the food image URL.
        
        Args:
            obj: The Explore_menu object.
        
        Returns:
            The absolute URL of the food image.
        """
        request = self.context.get('request')
        food_image_url = obj.food_image.url
        return request.build_absolute_uri(food_image_url)

class item_List_serializer(ModelSerializer):
    """
    Serializer for the item_List model.

    This serializer includes the 'image' field, which is a SerializerMethodField
    that returns the absolute URL of the food image. It also includes the 'category'
    field, which is a StringRelatedField.

    Attributes:
        image (SerializerMethodField): A SerializerMethodField that returns the absolute URL of the food image.
        category (StringRelatedField): A StringRelatedField that represents the category of the item.

    Meta:
        model (item_List): The model class that this serializer is associated with.
        fields (str): A string indicating that all fields of the model should be included in the serialized output.
    """

    image = SerializerMethodField('get_food_image')
    category = StringRelatedField()

    class Meta:
        model = item_List
        fields = '__all__'

    def get_food_image(self, obj):
        """
        Get the absolute URL of the food image.

        Args:
            obj: The item_List object.

        Returns:
            str: The absolute URL of the food image.
        """
        request = self.context.get('request')
        food_image_url = obj.image.url
        return request.build_absolute_uri(food_image_url)
    
class cartDataSerializer(serializers.Serializer):
    """
    Serializer for cart data.

    This serializer is used to validate and serialize cart data, including the item name,
    quantity, item price, price, and total.

    Attributes:
        item (CharField): The name of the item.
        quantity (IntegerField): The quantity of the item.
        item_price (FloatField): The price of the item.
        price (FloatField): The price of the item multiplied by the quantity.
        total (FloatField): The total price of the cart.

    Methods:
        validate(attrs): Validates the serializer's attributes.

    Raises:
        ValidationError: If the item is not in the item list.

    """
    item = serializers.CharField(max_length=200)
    quantity = serializers.IntegerField()
    item_price = serializers.FloatField()
    price = serializers.FloatField()

    def validate(self, attrs):
        if not item_List.objects.filter(name=attrs['item']).exists():
            raise serializers.ValidationError("item not in list")
        return attrs
    


class loginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    check = serializers.BooleanField(required=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user_obj = CusUser.objects.get(email=email)
                user = authenticate(request=self.context.get('request'), email=user_obj.email, password=password)

                if not user:
                    raise serializers.ValidationError("Invalid credentials")
            except ObjectDoesNotExist:
                raise serializers.ValidationError("User does not exist")
        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        attrs['user'] = user
        return attrs
    

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    firstname = serializers.CharField(required=False)
    password1 = serializers.CharField(required=True,write_only=True)
    password2 = serializers.CharField(required=True,write_only=True)

    def validate_email(self, value):
        if CusUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already registered")
        return value
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("passwords didnt match")
        return attrs
    
    def create(self, validated_data):
        user_obj = CusUser.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],  # Use email as username
        )
        user_obj.set_password(validated_data['password1'])
        user_obj.save()
        user = authenticate(
            request=self.context.get('request'),
            email=validated_data['email'],
            password=validated_data['password1']
        )
        if user is None:
            raise serializers.ValidationError("Authentication failed")
        return {'user_obj': user_obj, 'user': user}

    
class DataSerializer(ModelSerializer):
    class Meta:
        model = CusUser
        fields = ['email','firstname','username','profile_image']


class AddressSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=200,required=True)
    contact = serializers.CharField(max_length=200,required=True)
    door = serializers.CharField(max_length=200,required=True)
    street = serializers.CharField(max_length=200,required=True)
    city = serializers.CharField(max_length=200,required=True)
    zipcode = serializers.CharField(required=True)
    district = serializers.CharField(max_length=200,required=True)

    def validate_zipcode(self, value):
        if len(value)<7 and len(value)>7:
            raise serializers.ValidationError("Enter Correct Zipcode")
        return value
    
    def validate_contact(self, value):
        if len(value)>15:
            raise serializers.ValidationError("Enter Correct Contact Number")
        return value
    
    def validate(self, attrs):
        user = self.context['request'].user
        return attrs


class AdrObjSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Address
        fields = ['id', 'user', 'fullname', 'door', 'street', 'city', 'contact', 'zipcode', 'district']
    

class profileSerializer(ModelSerializer):
    profile_image = SerializerMethodField('get_profile_image')

    class Meta:
        model = CusUser
        fields = ['profile_image']
    
    def get_profile_image(self, obj):
        """
        Method to get the food image URL.
        
        Args:
            obj: The Explore_menu object.
        
        Returns:
            The absolute URL of the food image.
        """
        request = self.context.get('request')
        profile_image_url = obj.profile_image.url
        return request.build_absolute_uri(profile_image_url)