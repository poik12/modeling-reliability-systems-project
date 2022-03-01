from typing import List

from flask import Flask, render_template, request, redirect, url_for, Response, send_from_directory, send_file
from flask_bootstrap import Bootstrap

from calculations.reliability_structure import ReliabilityStructure
from calculations.simulation_calculations import SimulationCalc
from domain.models import Element, System
from input.dtos import ElementDTO, SubsystemDTO, SystemDTO, SimulationDTO
from output.graph_generator import GraphGeneration
from output.pdf_generator import PDFGeneration
from service.element_service import ElementService
from service.simulation_service import SimulationService
from service.subsystem_service import SubsystemService
from service.system_service import SystemService


app = Flask(__name__, template_folder='template')
Bootstrap(app)

element_service = ElementService()
subsystem_service = SubsystemService()
system_service = SystemService()
simulation_service = SimulationService()

subsystem_elements: List[Element] = []
current_subsystem_elements: List[Element] = []
system_subsystems: List[Element] = []
current_system_subsystems: List[Element] = []

graph_generator = GraphGeneration()


@app.route("/", methods=['GET', 'POST'])
def home():
    element_list = element_service.get_all_from_db()
    subsystem_list = subsystem_service.get_all_from_db()
    system_list = system_service.get_all_from_db()
    simulation_list = simulation_service.get_all_from_db()

    return render_template('home.html', element_list=element_list, subsystem_list=subsystem_list,
                           system_list=system_list, simulation_list=simulation_list)


@app.route("/element", methods=['GET', 'POST'])
def element():
    if request.method == "POST":
        element_service.save_in_db(
            ElementDTO(name=request.form.get("name"),
                       damage_intensity=request.form.get("damage_intensity"),
                       repair_intensity=request.form.get("repair_intensity"))
        )
        return redirect(url_for('home'))
    else:
        return render_template('add_element.html')


@app.route("/element/update/<int:id>", methods=['GET', 'POST'])
def update_element(id):
    element_from_db = element_service.get_by_id_from_db(id)
    if request.method == "POST":
        element_service.update_by_id(ElementDTO(name=request.form['name'],
                                                damage_intensity=request.form['damage_intensity'],
                                                repair_intensity=request.form['repair_intensity']),
                                     id)
        return redirect(url_for('home'))
    else:
        return render_template('update_element.html', element=element_from_db)


@app.route("/element/delete/<int:id>")
def delete_element(id):
    element_service.delete_by_id(id)
    return redirect(url_for('home'))


@app.route('/subsystem/<int:id>', methods=['GET', 'POST'])
def get_subsystem(id):
    subsystem_from_db = subsystem_service.get_by_id_from_db(id)
    return render_template('subsystem_details.html', subsystem=subsystem_from_db)


@app.route("/subsystem", methods=['GET', 'POST'])
def add_subsystem():
    element_list_from_db = element_service.get_all_from_db()
    reliability_structure_list = [ReliabilityStructure.SERIAL_SUBSYSTEM.value,
                                  ReliabilityStructure.PARALLEL_SUBSYSTEM.value]
    if request.method == "POST":
        if request.form["reliability_structure"] == ReliabilityStructure.SERIAL_SUBSYSTEM.value:
            subsystem_type = ReliabilityStructure.SERIAL_SUBSYSTEM
        else:
            subsystem_type = ReliabilityStructure.PARALLEL_SUBSYSTEM
        subsystem_service.save_in_db(SubsystemDTO(name=request.form['name'],
                                                  subsystem_type=subsystem_type,
                                                  elements=subsystem_elements))
        subsystem_elements.clear()
        return redirect(url_for('home'))
    else:
        return render_template('add_subsystem.html', reliability_structure_list=reliability_structure_list,
                               element_list_from_db=element_list_from_db, subsystem_elements=subsystem_elements)


@app.route("/subsystem/add-element/<int:id>", methods=['GET', 'POST'])
def add_element_to_subsystem(id):
    element_from_db = element_service.get_by_id_from_db(id)
    subsystem_elements.append(element_from_db)
    return redirect(url_for('add_subsystem'))


@app.route("/subsystem/delete-element/<int:id>", methods=['GET', 'POST'])
def delete_element_from_subsystem(id):
    for index, subsystem_element in enumerate(subsystem_elements):
        if subsystem_element.id == id:
            subsystem_elements.pop(index)
            break
    return redirect(url_for('add_subsystem'))


@app.route("/subsystem/update/<int:id>", methods=['GET', 'POST'])
def update_subsystem(id):
    reliability_structure_list = [ReliabilityStructure.SERIAL_SUBSYSTEM.value,
                                  ReliabilityStructure.PARALLEL_SUBSYSTEM.value]
    element_list_from_db = element_service.get_all_from_db()
    subsystem_from_db = subsystem_service.get_by_id_from_db(id)

    for element in subsystem_from_db.element_list:
        if element not in current_subsystem_elements:
            current_subsystem_elements.append(element)

    if request.method == "POST":
        if request.form["reliability_structure"] == ReliabilityStructure.SERIAL_SUBSYSTEM.value:
            subsystem_type = ReliabilityStructure.SERIAL_SUBSYSTEM
        else:
            subsystem_type = ReliabilityStructure.PARALLEL_SUBSYSTEM
        subsystem_service.update_by_id(SubsystemDTO(name=request.form['name'],
                                                    subsystem_type=subsystem_type,
                                                    elements=current_subsystem_elements),
                                       id)

        current_subsystem_elements.clear()
        return redirect(url_for('get_subsystem', id=id))
    else:
        return render_template('update_subsystem.html',
                               subsystem=subsystem_from_db,
                               reliability_structure_list=reliability_structure_list,
                               subsystem_elements=current_subsystem_elements,
                               element_list_from_db=element_list_from_db)


@app.route("/subsystem/<subsystem_id>/add-element/<int:id>", methods=['GET', 'POST'])
def add_element_to_updated_subsystem(id, subsystem_id):
    current_subsystem_elements.append(element_service.get_by_id_from_db(id))
    return redirect(url_for('update_subsystem', id=subsystem_id))


@app.route("/subsystem/<subsystem_id>/delete-element/<int:id>", methods=['GET', 'POST'])
def delete_element_from_updated_subsystem(id, subsystem_id):
    for index, subsystem_element in enumerate(current_subsystem_elements):
        if subsystem_element.id == id:
            current_subsystem_elements.pop(index)
            break
    return redirect(url_for('update_subsystem', id=subsystem_id))


@app.route("/subsystem/delete/<int:id>")
def delete_subsystem(id):
    subsystem_service.delete_by_id(id)
    return redirect(url_for('home'))


@app.route('/system/<int:id>', methods=['GET', 'POST'])
def get_system(id):
    system_from_db = system_service.get_by_id_from_db(id)
    subsystem_list = []
    for subsystem in system_from_db.subsystems:
        subsystem_list.append(subsystem_service.get_by_id_from_db(subsystem.id))
    system_from_db.subsystem_list = subsystem_list
    return render_template('system_details.html', system=system_from_db, system_img='system_graph_from_db.png')


@app.route("/system", methods=['GET', 'POST'])
def add_system():
    subsystem_list_from_db = subsystem_service.get_all_from_db()
    reliability_structure_list = [ReliabilityStructure.SERIAL_SUBSYSTEM.value,
                                  ReliabilityStructure.PARALLEL_SUBSYSTEM.value]
    if request.method == "POST":
        if request.form["reliability_structure"] == ReliabilityStructure.SERIAL_SUBSYSTEM.value:
            system_type = ReliabilityStructure.SERIAL_SUBSYSTEM
        else:
            system_type = ReliabilityStructure.PARALLEL_SUBSYSTEM
        system_service.save_in_db(SystemDTO(name=request.form['name'],
                                            system_type=system_type,
                                            subsystems=system_subsystems))
        system_subsystems.clear()
        return redirect(url_for('home'))
    else:
        return render_template('add_system.html',
                               reliability_structure_list=reliability_structure_list,
                               subsystem_list_from_db=subsystem_list_from_db,
                               system_subsystems=system_subsystems)


@app.route("/system/add-subsystem/<int:id>", methods=['GET', 'POST'])
def add_subsystem_to_system(id):
    system_subsystems.append(subsystem_service.get_by_id_from_db(id))
    return redirect(url_for('add_system'))


@app.route("/system/delete-subsystem/<int:id>", methods=['GET', 'POST'])
def delete_subsystem_from_system(id):
    for index, system_subsystem in enumerate(current_system_subsystems):
        if system_subsystem.id == id:
            current_system_subsystems.pop(index)
            break
    return redirect(url_for('add_system'))


@app.route("/system/delete/<int:id>")
def delete_system(id):
    system_service.delete_by_id(id)
    return redirect(url_for('home'))


@app.route("/system/update/<int:id>", methods=['GET', 'POST'])
def update_system(id):
    reliability_structure_list = [ReliabilityStructure.SERIAL_SUBSYSTEM.value,
                                  ReliabilityStructure.PARALLEL_SUBSYSTEM.value]
    subsystem_list_from_db = subsystem_service.get_all_from_db()
    system_from_db = system_service.get_by_id_from_db(id)

    for subsystem in system_from_db.subsystem_list:
        if subsystem not in current_system_subsystems:
            current_system_subsystems.append(subsystem)

    if request.method == "POST":
        if request.form["reliability_structure"] == ReliabilityStructure.SERIAL_SUBSYSTEM.value:
            system_type = ReliabilityStructure.SERIAL_SUBSYSTEM
        else:
            system_type = ReliabilityStructure.PARALLEL_SUBSYSTEM
        system_service.update_by_id(SystemDTO(name=request.form['name'],
                                              system_type=system_type,
                                              subsystems=current_system_subsystems),
                                    id)

        current_system_subsystems.clear()
        return redirect(url_for('get_system', id=id))
    else:
        return render_template('update_system.html',
                               system=system_from_db,
                               reliability_structure_list=reliability_structure_list,
                               system_subsystems=current_system_subsystems,
                               subsystem_list_from_db=subsystem_list_from_db)


@app.route("/system/<system_id>/add-subsystem/<int:id>", methods=['GET', 'POST'])
def add_subsystem_to_updated_system(id, system_id):
    current_system_subsystems.append(subsystem_service.get_by_id_from_db(id))
    return redirect(url_for('update_system', id=system_id))


@app.route("/subsystem/<subsystem_id>/delete-element/<int:id>", methods=['GET', 'POST'])
def delete_subsystem_from_updated_system(id, system_id):
    for index, system_subsystem in enumerate(current_system_subsystems):
        if system_subsystem.id == id:
            current_system_subsystems.pop(index)
            break
    return redirect(url_for('update_system', id=system_id))


@app.route("/simulation", methods=['GET', 'POST'])
def add_simulation():
    system_list = system_service.get_all_from_db()
    chosen_system = None

    if request.method == "POST":
        for system in system_list:
            if system.name == request.form.get('system'):
                chosen_system = system

        simulation_service.save_in_db(
            SimulationDTO(name=request.form.get("name"),
                          system=chosen_system,
                          time_horizon=request.form.get('time_horizon'),
                          time_change=request.form.get('time_change'),
                          time_repair=request.form.get('time_repair'),
                          number_of_iterations=request.form.get('number_of_iterations'))
        )
        return redirect(url_for('home'))
    else:
        return render_template('add_simulation.html', system_list=system_list)


@app.route('/simulation/<int:id>', methods=['GET', 'POST'])
def get_simulation(id):
    simulation_from_db = simulation_service.get_by_id_from_db(id)
    system_from_db = system_service.get_by_id_from_db(simulation_from_db.system_id)

    subsystem_list = []
    for subsystem in system_from_db.subsystems:
        subsystem_list.append(subsystem_service.get_by_id_from_db(subsystem.id))

    return render_template('simulation_details.html', simulation=simulation_from_db,
                           system_img='system_graph_from_db.png', subsystem_list=subsystem_list)


@app.route("/simulation/update/<int:id>", methods=['GET', 'POST'])
def update_simulation(id):
    simulation_from_db = simulation_service.get_by_id_from_db(id)
    system_list = system_service.get_all_from_db()
    chosen_system = None

    if request.method == "POST":
        for system in system_list:
            if system.name == request.form.get('system'):
                chosen_system = system

        simulation_service.update_by_id(
            dto=SimulationDTO(name=request.form.get("name"),
                              system=chosen_system,
                              time_horizon=request.form.get('time_horizon'),
                              time_change=request.form.get('time_change'),
                              time_repair=request.form.get('time_repair'),
                              number_of_iterations=request.form.get('number_of_iterations')),
            entity_id=id
        )
        return redirect(url_for('get_simulation', id=id))
    else:
        return render_template('update_simulation.html', simulation=simulation_from_db, system_list=system_list)


@app.route("/simulation/delete/<int:id>")
def delete_simulation(id):
    simulation_service.delete_by_id(id)
    return redirect(url_for('home'))


@app.route("/simulation/<int:id>/results")
def calculate_simulation(id):
    simulation_from_db = simulation_service.get_by_id_from_db(id)
    system_from_db = system_service.get_by_id_from_db(simulation_from_db.system_id)

    subsystem_list = []
    for subsystem in system_from_db.subsystems:
        subsystem_list.append(subsystem_service.get_by_id_from_db(subsystem.id))

    simulation_calc = SimulationCalc(id)
    simulation_calc.calculate_simulation()

    chart_img_dict = {
        'failure_probability_density': 'failure_probability_density_chart.png',
        'repair_probability_density': 'repair_probability_density_chart.png',
        'empirical_failure_function': 'empirical_failure_function_chart.png',
        'empirical_reliability_function': 'empirical_reliability_function_chart.png',
        'histogram': 'histogram.png',
    }

    return render_template('simulation_results.html', simulation=simulation_from_db, subsystem_list=subsystem_list,
                           charts=chart_img_dict, system_img='system_graph_from_db.png')


@app.route('/simulation/<int:id>/pdf', methods=['GET', 'POST'])
def download(id):
    pdf_generator = PDFGeneration(id)
    pdf_generator.generate_pdf()
    path = "simulation_report.pdf"
    return send_file(path, as_attachment=True)
