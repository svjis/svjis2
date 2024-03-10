from django.core.management.base import BaseCommand
from articles import utils

class Command(BaseCommand):
    help = "Send messages and empty message queue"

    def handle(self, *args, **options):
        utils.send_message_queue()
