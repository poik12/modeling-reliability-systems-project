from typing import List

import PIL
from PIL import Image, ImageDraw, ImageFont

from calculations.reliability_structure import ReliabilityStructure
from domain.models import Element, Subsystem, System


class GraphGeneration:
    _WHITE_COLOR = (255, 255, 255)
    _BLACK_COLOR = (0, 0, 0)
    _FONT_SIZE = 20
    _FONT_NAME = 'arial.ttf'
    _LINE_WIDTH = 2

    def __init__(self):
        self._FONT = ImageFont.truetype(self._FONT_NAME, self._FONT_SIZE)

    def draw_graph(self, subsystem_list: List[Subsystem], reliability_structure):
        img_subsystem_list: List[Image] = []
        for subsystem in subsystem_list:
            if subsystem.reliability_structure == ReliabilityStructure.SERIAL_SUBSYSTEM.value:
                img_subsystem_list.append(self._draw_serial_subsystem(subsystem))
            else:
                img_subsystem_list.append(self._draw_parallel_subsystem(subsystem))

        if reliability_structure == ReliabilityStructure.SERIAL_SUBSYSTEM.value:
            system_graph = self._draw_serial_system(img_subsystem_list)
        else:
            system_graph = self._draw_parallel_system(img_subsystem_list)

        # system_graph.show()
        system_graph.save('./output/graph_images/system_graph.png')

    def _draw_parallel_system(self, img_subsystem_list: [Subsystem]) -> Image:
        background_w = 300
        background_h = 0
        for img_subsystem in img_subsystem_list:
            img_w, img_h = img_subsystem.size
            background_h += img_h
            if background_w < img_w:
                background_w = img_w + 40

        img_background = PIL.Image.new(mode="RGB", size=(background_w, background_h), color=self._WHITE_COLOR)

        draw = ImageDraw.Draw(img_background)

        subsystem_first_w, subsystem_first_h = img_subsystem_list[0].size
        subsystem_last_w, subsystem_last_h = img_subsystem_list[-1].size

        start_point = subsystem_first_h / 2
        last_point = background_h - subsystem_last_h / 2

        draw.line((18, start_point) + (18, background_h / 2),
                  fill=self._BLACK_COLOR, width=self._LINE_WIDTH)
        draw.line((19, last_point) + (19, background_h / 2),
                  fill=self._BLACK_COLOR, width=self._LINE_WIDTH)

        draw.line((background_w - 18, start_point) + (background_w - 18, background_h / 2),
                  fill=self._BLACK_COLOR, width=self._LINE_WIDTH)
        draw.line((background_w - 17, last_point) + (background_w - 17, background_h / 2),
                  fill=self._BLACK_COLOR, width=self._LINE_WIDTH)

        draw.line((0, background_h / 2) + (18, background_h / 2),
                  fill=self._BLACK_COLOR, width=self._LINE_WIDTH)
        draw.line((background_w - 18, background_h / 2) + (background_w, background_h / 2),
                  fill=self._BLACK_COLOR, width=self._LINE_WIDTH)

        draw.line((18, start_point) + (background_w - 18, start_point),
                  fill=self._BLACK_COLOR, width=self._LINE_WIDTH)
        draw.line((18, last_point) + (background_w - 17, last_point),
                  fill=self._BLACK_COLOR, width=self._LINE_WIDTH)

        img_h_current = background_h
        for index, img_subsystem in enumerate(reversed(img_subsystem_list)):
            img_w, img_h = img_subsystem.size
            img_h_current -= img_h
            offset = ((background_w - img_w) // 2, img_h_current)
            img_background.paste(img_subsystem, offset)

            #             draw line in parallel img_subsystem to join with rectangle
            #             index in means reliaiblity structure -> parallel structure
            # if len(subsystem_list[index:]) > 2 and index in (0, 1, 3):
            #     next_img_w, next_img_h = subsystem_list[index + 1].size
            # draw.line((18, img_h_current - next_img_h / 2) + (background_w - 18, img_h_current - next_img_h / 2),
            #           fill=self._BLACK_COLOR, width=self._LINE_WIDTH)

        return img_background

    def _draw_serial_system(self, img_subsystem_list: [Subsystem]) -> Image:
        background_w = 20
        background_h = 300

        for img_subsystem in img_subsystem_list:
            img_w, img_h = img_subsystem.size
            background_w += img_w
            if background_h < img_h:
                background_h = img_h + 20

        img_background = PIL.Image.new(mode="RGB", size=(background_w, background_h), color=self._WHITE_COLOR)
        draw = ImageDraw.Draw(img_background)

        draw.line((0, background_h / 2) + (background_w, background_h / 2),
                  fill=self._BLACK_COLOR, width=self._LINE_WIDTH)

        img_w_current = background_w
        for index, img_subsystem in enumerate(reversed(img_subsystem_list)):
            img_w, img_h = img_subsystem.size
            img_w_current -= img_w
            offset = (img_w_current, (background_h - img_h) // 2)
            img_background.paste(img_subsystem, offset)

        return img_background

    def _draw_serial_subsystem(self, subsystem: Subsystem) -> Image:
        img_element = self._draw_element(subsystem.elements[0])
        img_w, img_h = img_element.size

        background_w = img_w * subsystem.number_of_elements
        background_h = img_h
        img_background = PIL.Image.new(mode="RGB", size=(background_w, background_h), color=self._WHITE_COLOR)
        draw = ImageDraw.Draw(img_background)

        for index, element in enumerate(subsystem.elements):
            img_element = self._draw_element(element)
            offset = (index * img_w, (background_h - img_h) // 2)
            img_background.paste(img_element, offset)

        offset = ((background_w - img_w) // 2, 1)
        draw.text(offset, subsystem.name, self._BLACK_COLOR, font=self._FONT)

        return img_background

    def _draw_parallel_subsystem(self, subsystem: Subsystem) -> Image:
        img_element = self._draw_element(subsystem.elements[0])
        img_w, img_h = img_element.size

        background_w = img_w + 4
        background_h = img_h * subsystem.number_of_elements
        img_background = PIL.Image.new(mode="RGB", size=(background_w, background_h), color=self._WHITE_COLOR)
        draw = ImageDraw.Draw(img_background)

        draw.line((0, background_h/2) + (30, background_h/2), fill=self._BLACK_COLOR, width=self._LINE_WIDTH)
        draw.line((250, background_h/2) + (280, background_h/2), fill=self._BLACK_COLOR, width=self._LINE_WIDTH)

        # Border
        # draw.line((0, 0) + (background_w, 0), fill=self._BLACK_COLOR, width=1)
        # draw.line((0, 0) + (0, background_h), fill=self._BLACK_COLOR, width=1)
        # draw.line((0, background_h) + (background_w, background_h), fill=self._BLACK_COLOR, width=1)
        # draw.line((background_w, 0) + (background_w, background_h), fill=self._BLACK_COLOR, width=1)

        bg_w, bg_h = img_background.size
        for index, element in enumerate(subsystem.elements):
            img_element = self._draw_element(element)
            offset = ((bg_w - img_w) // 2, index * img_h)
            img_w, img_h = img_element.size
            img_background.paste(img_element, offset)
            draw.line((0, 50) + (0, (subsystem.number_of_elements - 1) * img_h + 50),
                      fill=self._BLACK_COLOR, width=2)
            draw.line((img_w + 2, 50) + (img_w + 2, (subsystem.number_of_elements - 1) * img_h + 50),
                      fill=self._BLACK_COLOR, width=2)

        offset = ((bg_w - img_w) // 2, 0)
        draw.text(offset, subsystem.name, self._BLACK_COLOR, font=self._FONT)

        return img_background

    def _draw_element(self, element: Element) -> Image:
        img_element = PIL.Image.new(mode="RGB", size=(300, 160), color=self._WHITE_COLOR)
        draw = ImageDraw.Draw(img_element)

        x_0, y_0 = 50, 40
        w, h = 250, 120
        shape = [(x_0, y_0), (w, h)]
        draw.rectangle(shape, fill=self._WHITE_COLOR, outline=self._BLACK_COLOR, width=self._LINE_WIDTH)

        line_x_0, line_y_0 = 0, 80
        draw.line((line_x_0, line_y_0) + (50, 80), fill=self._BLACK_COLOR, width=self._LINE_WIDTH)
        draw.line((250, 80) + (300, 80), fill=self._BLACK_COLOR, width=self._LINE_WIDTH)

        if len(element.name) > 18:
            self.FONT_SIZE = 15
        draw.text((60, 70), element.name, self._BLACK_COLOR, font=self._FONT)

        return img_element.resize((220, 100))
