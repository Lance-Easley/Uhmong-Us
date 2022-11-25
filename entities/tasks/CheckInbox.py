from entities.tasks.BaseTask import *
from random import randint
import random
import pygame


class CheckInbox(BaseTask):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        # Resources
        self.disabled_send_button = pygame.image.load('images/tasks/check_inbox/disabled_send_button.png').convert()
        self.enabled_send_button = pygame.image.load('images/tasks/check_inbox/enabled_send_button.png').convert()
        self.email_notification = pygame.image.load('images/tasks/check_inbox/email_notification.png').convert()
        self.reply_button = pygame.image.load('images/tasks/check_inbox/reply_button.png').convert()
        self.trash_button = pygame.image.load('images/tasks/check_inbox/trash_button.png').convert()
        self.reply_field = pygame.image.load('images/tasks/check_inbox/reply_field.png').convert()
        self.email_card = pygame.image.load('images/tasks/check_inbox/email_card.png').convert()
        self.desktop = pygame.image.load('images/tasks/check_inbox/desktop.png').convert()

        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.small_font = pygame.font.Font("freesansbold.ttf", 12)

        self.email_count = randint(3, 5)
        self.email_contents = (
            {
                "subject": "You hAve woN!!!!!1!!!",
                "body": "Please replY with your sOcial security numbr and\ncredit card info to claIm your prize!1!!!!!",
                "type": "trash",
                "reply": "WHOO! My social is 123-12-1234. My CC info is\n1234-2345-3456-4567, 12/3, 987. " +
                        "What's my prize??"
            },
            {
                "subject": "Hey buddy!",
                "body": "It's your fellow Crewmate! I hope you're doing well.\nI heard there's a killer on the " +
                        "loose, be careful!",
                "type": "reply",
                "reply": "Hey Man! Yeah there is an imposter aboard. We're\ntrying to figure out who it is. Be safe!"
            },
            {
                "subject": "BEhInd U",
                "body": "Heh3he, I bet you lo0ked",
                "type": "trash",
                "reply": "There's no one behind me...."
            },
            {
                "subject": "Facility Utilities Bill",
                "body": f"Your utilities bill is ${randint(40, 80)}.{randint(10, 99)} and is due this\nmonth. " +
                        "Reply to confirm",
                "type": "reply",
                "reply": "Thanks for the heads up. The bill will be paid by the\nend of the day."
            },
            {
                "subject": "Fr3e TeslA",
                "body": "This is MElon Nusk. I give you car. Just need ur IP\nADDRESS NOW. Send A$AP",
                "type": "trash",
                "reply": "HI MR. MUSK! I'll gladly take this trade! My IP is\n127.0.0.1. Can't wait to get that " +
                        "free Tesla!!"
            },
            {
                "subject": "Your Amason package has Shipped!",
                "body": "Your package will arrive tomorrow! Reply to\nreceive further updates",
                "type": "reply",
                "reply": "Great, please let me know when it is delivered.\nThank you."
            },
            {
                "subject": "U get Iph0ne free winner chiken dinner",
                "body": "U give me bank inFo to confirm u iS u, then I\ns3nd phonE.",
                "type": "trash",
                "reply": "Free IPhone?! Say no more! My routing number is\n12345678, and account is 098765432109!"
            },
            {
                "subject": "Your results are in!",
                "body": "Your DNA test results have come back negative for\nImposter Syndrome! Congrats! Please " +
                        "reply for more",
                "type": "reply",
                "reply": "Phew! That's a relief. I'll be sure to tell the rest\nof the Crewmates. Thanks!"
            },
            {
                "subject": "Ur $69,420 AmAsOn oRder has bEen coFirmed",
                "body": "We HAVE recieve u order. replY for caLl inf0 to Get\nrefUnd if U no maKed dis purchAse.",
                "type": "trash",
                "reply": "I definitely did not make this order. I have time to\ncall now."
            },
            {
                "subject": "Amason Scam Alert",
                "body": "There is a '$69,420 order confirmed' scam going\naround. Reply if you have seen it before",
                "type": "reply",
                "reply": "I have seen it. Thankfully I didn't get scammed by it."
            },
            {
                "subject": "FreE RAM upGrade DOWnLoad Here",
                "body": "U want moRe raM to plAy NiteFort bettr? Reply for\nEASY LINK to GET MOR RAM NOW.",
                "type": "trash",
                "reply": "I've been wanting better FPS for MONTHS now. I'll\ngladly click your link for more RAM!"
            },
            {
                "subject": "Your Credit Score has increased!",
                "body": f"Congrats on your new score of {randint(680, 850)}!\nReply for tips to keep it going!",
                "type": "reply",
                "reply": "Yay! I'd love some advice to get it higher and higher!"
            }
        )

        self.email_list = []  # populated in renew_task_surface()
        self.email_rects = []  # populated in renew_task_surface()

        self.reply_button_rect = pygame.Rect(700, 680, 100, 50)
        self.trash_button_rect = pygame.Rect(825, 680, 100, 50)
        self.send_button_rect = pygame.Rect(1120, 680, 100, 50)

        self.opened_email_index = -1
        self.is_replying = False
        self.reply_field_text = ""

    def renew_task_surface(self):
        self.frame = 35
        self.show_success = False
        self.show_failure = False

        self.task_surface.fill((18, 52, 86))

        self.email_list = random.sample(self.email_contents, self.email_count)
        self.email_rects = (pygame.Rect((680, 400 + (index * 52), 560, 51)) for index in range(self.email_count))

        self.opened_email_index = -1
        self.is_replying = False
        self.reply_field_text = ""

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Visuals
        self.display.blit(self.desktop, (480, 180))
        self.display.blit(self.small_font.render(str(len(self.email_list)), True, (0, 0, 0)), (655, 290))

        if self.opened_email_index == -1:
            for index, email in enumerate(self.email_list):
                self.display.blit(self.email_notification, (680, 400 + (index * 52)))
                self.display.blit(self.font.render(email["subject"], True, (0, 0, 0)), (741, 415 + (index * 52)))

            if pygame.mouse.get_pressed(3)[0]:
                for index, rect in enumerate(self.email_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.opened_email_index = index
        else:
            email_contents = self.email_list[self.opened_email_index]
            self.display.blit(self.email_card, (680, 400))
            self.display.blit(self.font.render(email_contents["subject"], True, (0, 0, 0)), (700, 420))
            render_newline_text(700, 480, email_contents["body"], self.display, 32, self.font)

            self.display.blit(self.reply_button, (700, 680))
            self.display.blit(self.trash_button, (825, 680))

            if self.is_replying:
                self.display.blit(self.reply_field, (685, 595))
                render_newline_text(700, 610, self.reply_field_text, self.display, 32, self.font)

                if self.reply_field_text == email_contents["reply"]:
                    self.display.blit(self.enabled_send_button, (1120, 680))
                    if pygame.mouse.get_pressed(3)[0] and self.send_button_rect.collidepoint(mouse_x, mouse_y):
                        if email_contents["type"] == "reply":
                            self.email_list.pop(self.opened_email_index)
                            self.opened_email_index = -1
                            self.reply_field_text = ""
                            self.is_replying = False
                        else:
                            # TODO: If player responds to scam email, trigger a random sabotage
                            self.show_failure = True
                else:
                    self.display.blit(self.disabled_send_button, (1120, 680))
                    if pygame.event.peek(pygame.KEYDOWN):
                        self.reply_field_text += email_contents["reply"][len(self.reply_field_text)]

            if pygame.mouse.get_pressed(3)[0]:
                if self.reply_button_rect.collidepoint(mouse_x, mouse_y):
                    self.is_replying = True
                elif self.trash_button_rect.collidepoint(mouse_x, mouse_y):
                    if email_contents["type"] == "trash":
                        self.email_list.pop(self.opened_email_index)
                        self.opened_email_index = -1
                    else:
                        self.show_failure = True

        if self.show_failure:
            return self.fail(dt)

        if len(self.email_list) == 0:
            return self.success(dt)
