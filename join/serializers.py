from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import serializers

from join.models import Category, Contact, Subtask, Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups', 'first_name', 'last_name']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    assigned_to = ContactSerializer(many=True)
    subtasks = SubtaskSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        assigned_to_data = validated_data.pop('assigned_to')
        category_data = validated_data.pop('category')
        subtasks_data = validated_data.pop('subtasks')
        
        category_instance, _ = Category.objects.get_or_create(**category_data)

        task = Task.objects.create(category=category_instance, **validated_data)

        for contact_data in assigned_to_data:
            contact_instance, _ = Contact.objects.get_or_create(**contact_data)
            task.assigned_to.add(contact_instance)

        for subtask in subtasks_data:
            subtask_instance, _ = Subtask.objects.get_or_create(**subtask)
            task.subtasks.add(subtask_instance)

        return task
    
    def update(self, instance, validated_data):
        assigned_to_data = validated_data.pop('assigned_to', None)
        category_data = validated_data.pop('category', None)
        subtasks_data = validated_data.pop('subtasks', None)

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.urgency = validated_data.get('urgency', instance.urgency)
        instance.process_status = validated_data.get('process_status', instance.process_status)
        instance.due_date = validated_data.get('due_date', instance.due_date)

        instance.save()

        if assigned_to_data is not None:
            instance.assigned_to.clear()
            for contact_data in assigned_to_data:
                contact_instance, _ = Contact.objects.get_or_create(**contact_data)
                instance.assigned_to.add(contact_instance)

        if category_data is not None:
            category_instance, _ = Category.objects.get_or_create(**category_data)
            instance.category = category_instance

        if subtasks_data is not None:
            for subtask_data in subtasks_data:
                title = subtask_data.get('title')
                if title:
                    try:
                        subtask_instance = Subtask.objects.get(task=instance, title=title)
                        subtask_instance.done = subtask_data.get('done', subtask_instance.done)
                        subtask_instance.save()
                    except Subtask.DoesNotExist:
                        print('Subtask mit Titel "{}" wurde nicht gefunden.'.format(title))
                else:
                    print('Subtask-Titel nicht angegeben.')

        instance.save()

        return instance


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = get_user_model().objects.filter(email=email).first()

            if user and user.check_password(password):
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return data
    

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user