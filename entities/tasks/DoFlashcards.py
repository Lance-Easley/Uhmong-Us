from entities.tasks.BaseTask import *
from random import randint
import random
import pygame


class DoFlashcards(BaseTask):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        # Resources
        self.yes_button = pygame.image.load('images/tasks/do_flashcards/yes_button.png').convert()
        self.no_button = pygame.image.load('images/tasks/do_flashcards/no_button.png').convert()
        self.flashcard = pygame.image.load('images/tasks/do_flashcards/flashcard.png').convert()
        self.desktop = pygame.image.load('images/tasks/do_flashcards/desktop.png').convert()

        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.small_font = pygame.font.Font("freesansbold.ttf", 12)

        self.flashcard_count = randint(7, 9)
        self.flashcard_contents = (
            {
                "question": "2 + 2 = 4",
                "answer": True
            },
            {
                "question": "2 + 2 = 5",
                "answer": False
            },
            {
                "question": "The Crewmate's body is comprised of a\nsingle bone",
                "answer": True
            },
            {
                "question": "A 9mm bullet blows the lung out of the\nbody",
                "answer": False
            },
            {
                "question": "7 × 6 = 42",
                "answer": True
            },
            {
                "question": "4 × 7 = 29",
                "answer": False
            },
            {
                "question": "The sky is blue",
                "answer": True
            },
            {
                "question": "You are an Imposter",
                "answer": False
            },
            {
                "question": "You are a Crewmate",
                "answer": True
            },  # change
            {
                "question": "9/11 never happened",
                "answer": False
            },
            {
                "question": "Multi-Tools are called Multi-Tools because\nthey have multiple tools",
                "answer": True
            },
            {
                "question": "There is somebody watching you",
                "answer": False
            },
            {
                "question": "Egg.",
                "answer": True
            },
            {
                "question": "You don't have to worry about Imposters\nkilling people",
                "answer": False
            },
            {
                "question": "Playing Valorant with a controller is\ndisgusting",
                "answer": True
            },
            {
                "question": "Carrots are blue",
                "answer": False
            },
            {
                "question": "There have been only 2 World Wars",
                "answer": True
            },
            {
                "question": "You cannot recreate Among Us in Python",
                "answer": False
            }
        )
        self.flashcard_list = []  # populated in renew_task_surface()

        self.yes_button_rect = pygame.Rect(1120, 660, 100, 50)
        self.no_button_rect = pygame.Rect(700, 660, 100, 50)
        self.mouse_down = False

    def renew_task_surface(self):
        self.frame = 35
        self.show_success = False
        self.show_failure = False

        self.task_surface.fill((18, 52, 86))

        self.flashcard_list = random.sample(self.flashcard_contents, self.flashcard_count)
        self.mouse_down = False

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Visuals
        self.display.blit(self.desktop, (480, 180))
        self.display.blit(self.small_font.render(str(len(self.flashcard_list)), True, (0, 0, 0)), (712, 290))
        self.display.blit(self.flashcard, (680, 375))

        if len(self.flashcard_list) > 0:
            self.display.blit(self.no_button, (700, 660))
            self.display.blit(self.yes_button, (1120, 660))

            flashcard = self.flashcard_list[0]
            render_newline_text(700, 420, flashcard["question"], self.display, 32, self.font)
            if pygame.mouse.get_pressed(3)[0]:
                self.mouse_down = True
            elif self.mouse_down:
                if self.yes_button_rect.collidepoint(mouse_x, mouse_y):
                    if flashcard["answer"]:
                        self.flashcard_list.pop(0)
                    else:
                        self.show_failure = True
                elif self.no_button_rect.collidepoint(mouse_x, mouse_y):
                    if flashcard["answer"]:
                        self.show_failure = True
                    else:
                        self.flashcard_list.pop(0)
                self.mouse_down = False
        else:
            return self.success(dt)

        if self.show_failure:
            return self.fail(dt)
