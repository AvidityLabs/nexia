import logging

# logger = logging.getLogger(__name__)

import string


from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import serializers


from api.models import TokenUsage, User, TextToImage, TextToVideo, Instruction, Tone

from documents.models import (Document)


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)
        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance

class LoginSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    is_verified = serializers.CharField(max_length=255, read_only=True)
    display_name = serializers.CharField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)
    photo_url = serializers.CharField(max_length=255, read_only=True)
    pricing_plan = serializers.CharField(max_length=255, read_only=True)
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
             
                'id': user.uid,
                'username': user.email,
                'is_verified': user.is_verified,
                'display_name': user.display_name,
                'photo_url': user.photo_url, 
                'email': user.email,
                'pricing_plan': user.pricing_plan,
                'token': user.token
        }
        

class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    id = serializers.CharField(max_length=255, read_only=True)
    is_verified = serializers.CharField(max_length=255, read_only=True)
    display_name = serializers.CharField(max_length=255, read_only=True)
    photo_url = serializers.CharField(max_length=255, read_only=True)
    pricing_plan = serializers.CharField(max_length=255, read_only=True)
    email = serializers.CharField(max_length=255, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)
    
    pricing_plan = serializers.CharField(max_length=10, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['id','is_verified','display_name','photo_url','username','email', 'password','token', 'pricing_plan']
        

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        # Model serialiser automatically created the groups object for some reason learn about this.
        return User.objects.create_user(**validated_data)


class TokenUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenUsage
        fields = ['id', 'user', 'timestamp', 'prompt_tokens_used',
                  'completion_tokens_used', 'total_tokens_used']
        read_only_fields = ['id', 'user', 'timestamp']


class TextCompletionSerializer(serializers.Serializer):
    text = serializers.CharField(
        min_length=1, max_length=2048,
        error_messages={
            'required': 'This field is required.',
            'blank': 'This field cannot be blank.',
            'max_length': 'This field cannot exceed 100 characters.',
            
        })

    def validate_text(self, value):
        # Check for empty text
        if not value.strip():
            raise serializers.ValidationError("Text cannot be empty.")

        # Check for text containing only spaces
        if value.isspace():
            raise serializers.ValidationError("Text cannot contain only spaces.")

        # Check for text containing only special characters
        if all(c in string.punctuation for c in value):
            raise serializers.ValidationError("Text cannot contain only special characters.")

        # Check for text containing only digits
        if value.isdigit():
            raise serializers.ValidationError("Text cannot contain only digits.")

        # Check for non-ASCII characters
        try:
            value.encode('ascii')
        except UnicodeEncodeError:
            raise serializers.ValidationError("Text cannot contain non-ASCII characters.")

        return value        


class TextSerializer(serializers.Serializer):
    instruction = serializers.CharField(
        min_length=1, max_length=2048,
        error_messages={
            'required': 'This field is required.',
            'blank': 'This field cannot be blank.',
            'max_length': 'This field cannot exceed 100 characters.',
            
        })
    text = serializers.CharField(
        min_length=1, max_length=2048,
        error_messages={
            'required': 'This field is required.',
            'blank': 'This field cannot be blank.',
            'max_length': 'This field cannot exceed 100 characters.',
            
        })

    def validate_text(self, value):
        # Check for empty text
        if not value.strip():
            raise serializers.ValidationError("Text cannot be empty.")

        # Check for text containing only spaces
        if value.isspace():
            raise serializers.ValidationError("Text cannot contain only spaces.")

        # Check for text containing only special characters
        if all(c in string.punctuation for c in value):
            raise serializers.ValidationError("Text cannot contain only special characters.")

        # Check for text containing only digits
        if value.isdigit():
            raise serializers.ValidationError("Text cannot contain only digits.")

        # Check for non-ASCII characters
        try:
            value.encode('ascii')
        except UnicodeEncodeError:
            raise serializers.ValidationError("Text cannot contain non-ASCII characters.")

        return value
    


class TextToImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextToImage
        fields = '__all__'

class TextToVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextToVideo
        fields = '__all__'

class ToneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tone
        fields = ['name']


class InstructionSerializer(serializers.ModelSerializer):
    tones = ToneSerializer(many=True)
    prompt = serializers.CharField(read_only=True)

    class Meta:
        model = Instruction
        fields = ['id', 'description', 'tones', 'audience', 'style', 'context', 'language', 'length', 'source_text', 'prompt']

    def create(self, validated_data):
        tones_data = validated_data.pop('tones')

        tones = []
        for tone_data in tones_data:
            tone, _ = Tone.objects.get_or_create(name=tone_data['name'])
            tones.append(tone)

        # Check if the instruction already exists
        description = validated_data['description']
        existing_instruction = Instruction.objects.filter(description=description).first()

        if existing_instruction:
            # Update the existing instruction if it already exists
            existing_instruction.audience = validated_data.get('audience', existing_instruction.audience)
            existing_instruction.style = validated_data.get('style', existing_instruction.style)
            existing_instruction.context = validated_data.get('context', existing_instruction.context)
            existing_instruction.language = validated_data.get('language', existing_instruction.language)
            existing_instruction.length = validated_data.get('length', existing_instruction.length)
            existing_instruction.source_text = validated_data.get('source_text', existing_instruction.source_text)
            existing_instruction.save()
            existing_instruction.tones.set(tones)
            return existing_instruction
        else:
            # Create a new instruction if it does not exist
            instruction = Instruction.objects.create(**validated_data)
            instruction.tones.set(tones)
            return instruction

class InstructionSerializerResult(serializers.ModelSerializer):
    tones = ToneSerializer(many=True)
    prompt = serializers.CharField(read_only=True)


    class Meta:
        model = Instruction
        fields = ['id', 'description','tones','prompt' ]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'user', 'use_case', 'title', 'content', 'is_saved']




class AnyPayloadSerializer(serializers.Serializer):
    payload = serializers.JSONField()

    """
    In this updated example, a custom validate() method is added to the serializer. It checks whether the 'payload' key is present in the payload data. If it's missing, a ValidationError is raised.
    """
    # def validate(self, attrs):
    #     if 'payload' not in attrs:
    #         raise serializers.ValidationError("Payload is required")
    #     return attrs