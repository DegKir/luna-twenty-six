import krpc
import time
import os

#очищаем консоль
clear = lambda: os.system('cls')
clear()

def pause_until_end_of_liquid_fuel(conn):
    print("waiting until liquid fuel ends")

    vessel = conn.space_center.active_vessel
    fuel_amount = conn.get_call(vessel.resources.amount, 'LiquidFuel')
    expr = conn.krpc.Expression.less_than(
        conn.krpc.Expression.call(fuel_amount),
        conn.krpc.Expression.constant_float(0.1))
    event = conn.krpc.add_event(expr)
    with event.condition:
        event.wait()

def pause_until_end_of_solid_fuel(conn):
    print("waiting until solid fuel ends")
    vessel = conn.space_center.active_vessel
    fuel_amount = conn.get_call(vessel.resources.amount, 'SolidFuel')
    expr = conn.krpc.Expression.less_than(
        conn.krpc.Expression.call(fuel_amount),
        conn.krpc.Expression.constant_float(0.1))
    event = conn.krpc.add_event(expr)
    with event.condition:
        event.wait()


def second_stage(conn):
    vessel = conn.space_center.active_vessel
    
    #фиксируем направление вбок
    vessel.auto_pilot.target_pitch_and_heading(60, 90)

    #Включаем ступень
    vessel.control.activate_next_stage()

    #Ждем, пока не кончится топливо
    pause_until_end_of_liquid_fuel(conn)


def first_stage(conn):
    vessel = conn.space_center.active_vessel

    #фиксируем направление вверх
    vessel.auto_pilot.target_pitch_and_heading(90, 90)

    #Включаем ступень
    vessel.control.activate_next_stage()

    #Ждем, пока не кончится топливо
    pause_until_end_of_solid_fuel(conn)


def preparations(conn):
    vessel = conn.space_center.active_vessel
    vessel.auto_pilot.engage()  #Подготавливаем двигатель
    vessel.control.throttle = 1 #Максимальная тяга

    #обратный отсчет
    for i in range(4):
        print(4-i)
        time.sleep(1)




conn = krpc.connect(name='Sub-orbital flight')

print("Program start")
preparations(conn)  #обратный отсчет и инициализация аппарата
time.sleep(0.1)
print("Launch")
first_stage(conn)   #вертикальный взлет вверх на первой ступени
time.sleep(0.1)
print("First stage decoupled")
second_stage(conn)  #взлет под наклоном
time.sleep(0.1)
print("Second stage decoupled")
print("Program ends")
