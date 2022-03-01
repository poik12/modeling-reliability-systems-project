import numpy as np

from calculations.simulation_calculations import SimulationCalc
from calculations.system_calculations import SystemCalc
from controller.home import app
from domain.database_connection import DatabaseConnection
from input.dtos import ElementDTO, SubsystemDTO, SystemDTO, SimulationDTO
from output.chart_generator import ChartGeneration
from output.graph_generator import GraphGeneration
from output.pdf_generator import PDFGeneration
from service.element_service import ElementService

from service.simulation_service import SimulationService
from service.subsystem_service import SubsystemService
from service.system_service import SystemService
from calculations.reliability_structure import ReliabilityStructure


def main():
    database_connector = DatabaseConnection()
    database_connector.get_connection_to_database()

    """Create rows in db"""
    # crete_elements()
    # create_subsystems()
    # create_systems()
    # create_simulation()

    """Info about rows from db"""
    # system_info()

    """"Element"""
    # element_service = ElementService()
    # element_service.get_all_from_db()
    # element_service.get_by_id_from_db(1)
    # element_service.save_in_db(ElementDTO("Rama", 0.052, 0.39))
    # element_service.update_by_id(ElementDTO("Rama_2", 0.052, 0.39), 10)
    # element_service.delete_by_id(10)

    """"Subsystem"""
    # subsystem_service = SubsystemService()
    # subsystem_service.get_all_from_db()
    # subsystem_service.get_by_id_from_db(1)
    # element_service = ElementService()
    # element_list = [element_service.get_by_id_from_db(1)]
    # subsystem_service.save_in_db(
    #     SubsystemDTO("Uk. zawieszenia", ReliabilityStructure.PARALLEL_SUBSYSTEM, element_list)
    # )
    # subsystem_service.update_by_id(
    #     SubsystemDTO("Uk. hamulcowy", ReliabilityStructure.SERIAL_SUBSYSTEM, element_list), 4
    # )
    # subsystem_service.delete_by_id(4)

    """System"""
    # system_service = SystemService()
    # system_service.get_all_from_db()
    # system_service.get_by_id_from_db(1)
    # subsystem_service = SubsystemService()
    # subsystem_list = [subsystem_service.get_by_id_from_db(1)]
    # system_service.save_in_db(SystemDTO("Kolej Linowa", ReliabilityStructure.SERIAL_SUBSYSTEM, subsystem_list))
    # system_service.update_by_id(SystemDTO("Kolej Linowa", ReliabilityStructure.SERIAL_SUBSYSTEM, subsystem_list), 2)
    # system_service.delete_by_id(2)

    """Simulation"""
    # simulation_service = SimulationService()
    # simulation_service.get_all_from_db()
    # simulation_service.get_by_id_from_db(1)
    # system_service = SystemService()
    # system = system_service.get_by_id_from_db(1)
    # simulation_service.save_in_db(SimulationDTO("Symulacja niezawod. koleji linowej", system, 730, 2, 10, 120))
    # simulation_service.update_by_id(SimulationDTO("Symulacja niezawod. przenosnika wibr.", system, 340, 5, 20, 80), 2)
    # simulation_service.delete_by_id(2)

    """Calculations"""
    # simulation_calc = SimulationCalc(simulation_id=7)
    # simulation_calc.calculate_simulation()

    """APP"""
    app.run(host="localhost", debug=True)


def crete_elements():
    elements = [
        ElementDTO("Kamera", 0.054, 0.89),
        ElementDTO("Czujnik", 0.031, 0.78),
        ElementDTO("Kontroler", 0.023, 0.72),
        ElementDTO("Akumulator", 0.043, 0.42),
        ElementDTO("Silnik", 0.073, 0.63),
        ElementDTO("Przekladnia Pasowa", 0.053, 0.89),
        ElementDTO("Alternator", 0.023, 0.60),
        ElementDTO("Przekladnia Zebata", 0.078, 0.69),
        ElementDTO("Nadwozie", 0.093, 0.52),
        ElementDTO("Podwozie", 0.013, 0.22),
    ]
    element_service = ElementService()
    [element_service.save_in_db(element) for element in elements]


def create_subsystems():
    element_service = ElementService()
    subsystem_service = SubsystemService()
    elements = element_service.get_all_from_db()
    subsystem_dto_list = [
        SubsystemDTO("Uklad Napedowy", ReliabilityStructure.PARALLEL_SUBSYSTEM, elements[0:2]),
        SubsystemDTO("Zasilanie", ReliabilityStructure.SERIAL_SUBSYSTEM, elements[3:6]),
        SubsystemDTO("System Pomiarowy", ReliabilityStructure.PARALLEL_SUBSYSTEM, elements[7:9]),
    ]
    [subsystem_service.save_in_db(subsystem_dto) for subsystem_dto in subsystem_dto_list]


def create_systems():
    subsystem_service = SubsystemService()
    system_service = SystemService()
    subsystems = subsystem_service.get_all_from_db()
    system_dto_list = [
        SystemDTO("Autobus", ReliabilityStructure.PARALLEL_SUBSYSTEM, subsystems[0:3]),
    ]
    [system_service.save_in_db(system_dto) for system_dto in system_dto_list]


def create_simulation():
    simulation_service = SimulationService()
    system_service = SystemService()
    system_from_db = system_service.get_by_id_from_db(4)
    simulation_dto = SimulationDTO("Symulacja niezawodnosci autobusu", system_from_db, 400, 2, 10, 150)
    simulation_service.save_in_db(simulation_dto)


def system_info():
    system_service = SystemService()
    subsystem_service = SubsystemService()
    systems = system_service.get_all_from_db()
    for index, system in enumerate(systems):
        print(type(system))
        print(f"System {index + 1} zawiera {system.number_of_subsystems} układy: {system.subsystem_list}")
        print("***************************************************")
        for index, subsystem in enumerate(system.subsystem_list):
            subsystem_from_db = subsystem_service.get_by_id_from_db(subsystem.id)
            print(f"Subystem {index + 1}, Liczba elementów: {subsystem_from_db.number_of_elements}")
            print(f"Element {index + 1}: {subsystem_from_db.element_list}")
            print("***************************************************")


if __name__ == "__main__":
    main()
