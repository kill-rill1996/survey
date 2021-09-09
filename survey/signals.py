# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import Choice
#
#
# @receiver(pre_save, sender=Choice)
# def create_choice_id(sender, instance, *args, **kwargs):
#
#     all_choices = Choice.objects.all().order_by('-id')
#     if len(all_choices) > 1:
#         last_id = all_choices[0].id
#         instance.id = last_id + 1


