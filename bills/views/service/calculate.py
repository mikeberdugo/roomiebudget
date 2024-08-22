from datetime import datetime, timedelta

def generar_informe(data):
    """
    Genera un informe detallado basado en el cálculo del costo diario del servicio para cada ocupante
    y sus invitados.

    :param data: Diccionario con las fechas de inicio y fin del servicio, valor mensual del servicio,
                 y ocupantes con sus invitados.
    :return: Diccionario con el informe detallado por fecha.
    """
    
    fecha_inicio_servicio = datetime.strptime(data['fecha_inicio_servicio'], '%Y-%m-%d')
    fecha_fin_servicio = datetime.strptime(data['fecha_fin_servicio'], '%Y-%m-%d')
    valor_servicio_mensual = data['valor_servicio_mensual']
    
    # Calcular el número total de días del servicio
    dias_totales_servicio = (fecha_fin_servicio - fecha_inicio_servicio).days + 1
    
    # Calcular el costo diario del servicio
    costo_diario_servicio = valor_servicio_mensual / dias_totales_servicio
    
    # Inicializar el informe
    informe = { (fecha_inicio_servicio + timedelta(days=i)).strftime('%Y-%m-%d'): {} for i in range(dias_totales_servicio)}
    
    # Distribuir el costo diario
    for i in range(dias_totales_servicio):
        dia_actual = fecha_inicio_servicio + timedelta(days=i)
        dia_str = dia_actual.strftime('%Y-%m-%d')
        
        # Inicializar los costos diarios
        personas_a_cargo = {}
        
        for ocupante in data['ocupantes']:
            nombre = ocupante['nombre']
            fecha_inicio_ocupante = fecha_inicio_servicio
            fecha_fin_ocupante = fecha_fin_servicio
            
            if fecha_inicio_ocupante <= dia_actual <= fecha_fin_ocupante:
                if nombre not in personas_a_cargo:
                    personas_a_cargo[nombre] = 0  # Inicializar el contador para esta persona

                personas_a_cargo[nombre] += 1  # El ocupante siempre está

                if ocupante['invitados']:
                    for invitado in ocupante['invitados']:
                        fecha_inicio_invitado = datetime.strptime(invitado['fecha_inicio'], '%Y-%m-%d')
                        fecha_fin_invitado = datetime.strptime(invitado['fecha_fin'], '%Y-%m-%d')

                        if fecha_inicio_invitado <= dia_actual <= fecha_fin_invitado:
                            if nombre not in personas_a_cargo:
                                personas_a_cargo[nombre] = 0
                            personas_a_cargo[nombre] += 1
        
        # Calcular el costo diario total a repartir entre las personas a cargo
        total_personas_a_cargo = sum(personas_a_cargo.values())
        if total_personas_a_cargo > 0:
            costo_diario_total = costo_diario_servicio / total_personas_a_cargo
        
            for nombre, cantidad_personas in personas_a_cargo.items():
                if nombre not in informe[dia_str]:
                    informe[dia_str][nombre] = 0
                informe[dia_str][nombre] += costo_diario_total * cantidad_personas
    
    return informe


def calcular_precio_recibo(data):
    """
    Calcula el precio a pagar de un recibo mensual basado en los ocupantes de la vivienda,
    las fechas de estancia de sus invitados, el valor mensual del servicio y el periodo total del servicio.
    El costo del servicio se distribuye proporcionalmente según los días de ocupación de cada ocupante.

    :param data: Diccionario con las fechas de inicio y fin del servicio, valor mensual del servicio,
                 y ocupantes con sus invitados.
    :return: Diccionario con una lista de 'resultados'.
    """

    fecha_inicio_servicio = datetime.strptime(data['fecha_inicio_servicio'], '%Y-%m-%d')
    fecha_fin_servicio = datetime.strptime(data['fecha_fin_servicio'], '%Y-%m-%d')
    valor_servicio_mensual = data['valor_servicio_mensual']
    
    # Calcular el número total de días del servicio
    dias_totales_servicio = (fecha_fin_servicio - fecha_inicio_servicio).days + 1
    
    # Inicializar estructuras para el cálculo de días de ocupación
    total_dias_ocupacion = 0
    dias_ocupacion_por_persona = {}

    # Calcular el costo diario del servicio
    costo_diario_servicio = valor_servicio_mensual / dias_totales_servicio

    for ocupante in data['ocupantes']:
        nombre = ocupante['nombre']
        total_dias_ocupante = dias_totales_servicio  # El ocupante está en la vivienda todos los días

        for i in range(dias_totales_servicio):
            dia_actual = fecha_inicio_servicio + timedelta(days=i)
            personas_a_cargo = 1  # El ocupante siempre está

            if ocupante['invitados']:
                for invitado in ocupante['invitados']:
                    fecha_inicio_invitado = datetime.strptime(invitado['fecha_inicio'], '%Y-%m-%d')
                    fecha_fin_invitado = datetime.strptime(invitado['fecha_fin'], '%Y-%m-%d')

                    # Asegurarse de que las fechas del invitado estén dentro del rango del servicio
                    if fecha_inicio_invitado <= dia_actual <= fecha_fin_invitado:
                        personas_a_cargo += 1

            # Agregar la información al cálculo de días de ocupación
            total_dias_ocupante += (personas_a_cargo - 1)  # Contabilizar los invitados adicionales

        dias_ocupacion_por_persona[nombre] = total_dias_ocupante
        total_dias_ocupacion += total_dias_ocupante
    
    # Ahora calculamos el costo proporcional que cada ocupante debe pagar
    resultados = []
    for nombre, dias_ocupante in dias_ocupacion_por_persona.items():
        proporcion_pago = dias_ocupante / total_dias_ocupacion
        total_a_pagar = valor_servicio_mensual * proporcion_pago
        resultados.append({'nombre': nombre, 'total_a_pagar': total_a_pagar})
    
    return {'resultados': resultados}



