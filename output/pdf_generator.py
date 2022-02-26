from PIL import Image
from fpdf import FPDF
from domain.models import Simulation
from service.simulation_service import SimulationService
from service.subsystem_service import SubsystemService
from datetime import datetime


class PDFGeneration(FPDF):
    _ORIENTATION = 'P'
    _UNIT = 'mm'
    _FORMAT = 'A4'
    _TITLE = 'Raport z przebiegu symulacji'
    _FONT_NAME = 'TimesNewRoman'
    _CREATION_PATH = './controller/simulation_report.pdf'
    simulation_id: int
    _simulation: Simulation
    _simulation_service = SimulationService()

    def __init__(self, simulation_id):
        super().__init__(orientation=self._ORIENTATION, unit=self._UNIT, format=self._FORMAT)
        self.add_font('TimesNewRoman', '', r'C:\Windows\Fonts\times.ttf', uni=True)
        self.add_font('TimesNewRoman', 'B', r'C:\Windows\Fonts\timesbd.ttf', uni=True)
        self.add_font('TimesNewRoman', 'I', r'C:\Windows\Fonts\timesi.ttf', uni=True)
        self.add_font('TimesNewRoman', 'BI', r'C:\Windows\Fonts\timesbi.ttf', uni=True)
        self.set_auto_page_break(auto=True, margin=15)  # auto page break
        self._simulation = self._simulation_service.get_by_id_from_db(simulation_id)

    def generate_pdf(self):
        self._system_parameters(1, "Parametry symulacji niezawodnościowej systemu")
        self._reliability_diagram(2, "Struktura niezawodnościowa systemu")
        self._system_elements(3, "Składowe systemu")
        self._generated_charts(4, "Wyniki symulacji")
        self.output(self._CREATION_PATH, 'F')

    def header(self):
        self.image('resources/agh_logo.jpg', 10, 8, 25)
        self.set_font(self._FONT_NAME, 'B', 24)  # font
        # calculate width of title and position
        title_width = self.get_string_width(self._TITLE)
        document_width = self.w
        self.set_x((document_width - title_width) / 2)
        self.cell(title_width, 20, self._TITLE, ln=1, align='C')  # title
        self.ln(10)  # line break

    def footer(self):
        self.set_y(-15)  # set position
        self.set_font(self._FONT_NAME, '', 12)  # set font
        self.alias_nb_pages()  # get total page numbers
        self.cell(0, 0, f'Strona {self.page_no()} z {{nb}}', align='C')

    def _page_title(self, chapter_number, chapter_title):
        self.set_font(self._FONT_NAME, 'B', 20)  # set font
        self.set_fill_color(200, 220, 255)  # background color
        chapter_title = f'  {chapter_number}. {chapter_title}'  # chapter title
        self.cell(0, 10, chapter_title, ln=1, fill=1)  # page number

    def _system_parameters(self, chapter_number, chapter_title):
        self.add_page()
        self._page_title(chapter_number, chapter_title)
        self._system_parameters_body()

    def _system_parameters_body(self):
        self.set_font(self._FONT_NAME, '', 12)
        self.cell(0, 10, f'Nazwa symulacji: {self._simulation.name}', ln=True)
        self.cell(0, 10, f'Horyzont czasowy: {self._simulation.time_horizon} dni', ln=True)
        self.cell(0, 10, f'Zmiana czasu: {self._simulation.time_change} dni', ln=True)
        self.cell(0, 10, f'Czas naprawy: {self._simulation.time_repair} dni', ln=True)
        self.cell(0, 10, f'Liczba iteracji: {self._simulation.number_of_iterations}', ln=True)
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        self.cell(0, 10, f'Symulacja wykonana: {dt_string}', ln=True)
        self.cell(0, 1, f'', fill=1, ln=True)
        self.cell(0, 10, f'Symulowany system: {self._simulation.system.name}', ln=True)
        self.cell(0, 10, f'Struktura niezawodnościowa systemu: {self._simulation.system.reliability_structure}',
                  ln=True)
        self.cell(0, 10, f'Liczba układów w systemie: {self._simulation.system.number_of_subsystems}', ln=True)
        line_height = 8
        col_width = 55
        col_name_list = ['Lp.', 'Nazwa układu', "Struktura niezawodnościowa", "Liczba elementów"]
        self._table_header(line_height, col_width, col_name_list)
        self._table_body_subsystems(self._simulation.system, line_height, col_width)
        self.cell(0, 10, f'Ostatnia modyfikacja systemu: {self._simulation.system.updated_on}', ln=True)

    def _reliability_diagram(self, chapter_number, chapter_title):
        file_name = './controller/static//system_graph_from_db.png'
        graph = Image.open(file_name)
        graph_w, graph_h = graph.size
        # convert pixel in mm with 1px=0.264583 mm
        width, height = float(graph_w * 0.264583), float(graph_h * 0.264583)
        # A4 format size
        pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
        # get page orientation from image size
        orientation = 'P' if width < height else 'L'
        #  make sure image size is not greater than the pdf format size
        width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
        height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

        self.add_page(orientation=orientation)
        self._page_title(chapter_number, chapter_title)
        self._reliability_diagram_body(file_name, width-15, height)

    def _reliability_diagram_body(self, image_file, image_width, image_height):
        self.image(image_file, x=15, y=60, w=image_width, h=image_height)

    def _system_elements(self, chapter_number, chapter_title):
        self.add_page(orientation='P')
        self._page_title(chapter_number, chapter_title)
        self._system_elements_body()

    def _system_elements_body(self):
        line_height = self.font_size
        col_width = 55
        self.set_fill_color(224, 224, 224)  # background color
        self.set_font(self._FONT_NAME, '', 12)
        subsystem_list = self.get_subsystem_list()
        for index, subsystem in enumerate(subsystem_list):
            self.cell(0, 10, f'{index + 1}. {subsystem.name}', ln=True)
            self.cell(0, 10, f'     Typ układu: {subsystem.reliability_structure}', ln=True)
            self.cell(0, 10, f'     Liczba elementów w układzie: {subsystem.number_of_elements}', ln=True)
            col_name_list = ['Lp.', 'Nazwa elementu', "Intensywność zniszczeń", "Intensywność naprawy"]
            self._table_header(line_height, col_width, col_name_list)
            self._table_body_elements(subsystem, line_height, col_width)

    def get_subsystem_list(self):
        _subsystem_service = SubsystemService()
        subsystem_list = []
        for subsystem in self._simulation.system.subsystems:
            subsystem_from_db = _subsystem_service.get_by_id_from_db(subsystem.id)
            subsystem_list.append(subsystem_from_db)
        return subsystem_list

    def _table_header(self, line_height, col_width, col_name_list):
        self.set_font(self._FONT_NAME, 'B', 12)  # enabling bold text
        for col_name in col_name_list:
            if col_name == 'Lp.':
                self.cell(col_width / 3, line_height, col_name, border=1, fill=1, align='C')
            else:
                self.cell(col_width, line_height, col_name, border=1, fill=1, align='C')
        self.ln(line_height)
        self.set_font(self._FONT_NAME, '', 12)  # disabling bold text

    def _table_body_subsystems(self, system, line_height, col_width):
        for index, subsystem in enumerate(system.subsystems):  # repeat data rows
            element_attr_list = [
                f'{index + 1}.',
                subsystem.name,
                subsystem.reliability_structure,
                subsystem.number_of_elements
            ]
            for element_attr in element_attr_list:
                if element_attr == f'{index + 1}.':
                    self.cell(col_width / 3, line_height, f'{element_attr}', border=1, align='C')
                else:
                    self.cell(col_width, line_height, f'{element_attr}', border=1, align='C')
            self.ln(line_height)

    def _table_body_elements(self, subsystem, line_height, col_width):
        for index, element in enumerate(subsystem.elements):  # repeat data rows
            element_attr_list = [
                f'{index + 1}.',
                element.name,
                element.damage_intensity,
                element.repair_intensity
            ]
            for element_attr in element_attr_list:
                if element_attr == f'{index + 1}.':
                    self.cell(col_width / 3, line_height, f'{element_attr}', border=1, align='C')
                else:
                    self.cell(col_width, line_height, f'{element_attr}', border=1, align='C')
            self.ln(line_height)
        self.cell(0, 3, '', ln=True)

    def _generated_charts(self, chapter_number, chapter_title):
        self.add_page()
        self._page_title(chapter_number, chapter_title)
        self._generate_density_charts()
        self.add_page()
        self._page_title(chapter_number, chapter_title)
        self._generate_empirical_function_charts()
        self.add_page()
        self._page_title(chapter_number, chapter_title)
        self._generate_histogram()

    def _generate_density_charts(self):
        image_list = [
            ('./controller/static/failure_probability_density_chart.png', 15, 50),
            ('./controller/static/repair_probability_density_chart.png', 15, 160),
        ]
        for image in image_list:
            self.image(image[0], x=image[1], y=image[2], w=180, h=110)

    def _generate_empirical_function_charts(self):
        image_list = [
            ('./controller/static/empirical_reliability_function_chart.png', 15, 50),
            ('./controller/static/empirical_failure_function_chart.png', 15, 160),
        ]
        for image in image_list:
            self.image(image[0], x=image[1], y=image[2], w=180, h=110)

    def _generate_histogram(self):
        image = ('./controller/static/histogram.png', 15, 50)
        self.image(image[0], x=image[1], y=image[2], w=180, h=110)
