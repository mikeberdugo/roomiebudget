from datetime import datetime, timedelta

def calcular_precio_recibo(data):
    """
    Calcula el precio a pagar de un recibo mensual basado en los ocupantes de la vivienda,
    las fechas de estancia de sus invitados, el valor mensual del servicio y el periodo total del servicio.
    El costo del servicio se distribuye proporcionalmente según los días de ocupación de cada ocupante.

    :param data: Diccionario con las fechas de inicio y fin del servicio, valor mensual del servicio,
                 y ocupantes con sus invitados.
    :return: Diccionario con dos listas: 'resultados' y 'informe'.
    """

    fecha_inicio_servicio = datetime.strptime(data['fecha_inicio_servicio'], '%Y-%m-%d')
    fecha_fin_servicio = datetime.strptime(data['fecha_fin_servicio'], '%Y-%m-%d')
    valor_servicio_mensual = data['valor_servicio_mensual']
    
    # Calcular el número total de días del servicio
    dias_totales_servicio = (fecha_fin_servicio - fecha_inicio_servicio).days + 1
    
    # Sumar los días totales de ocupación de cada ocupante y sus invitados
    total_dias_ocupacion = 0
    dias_ocupacion_por_persona = {}
    informe = {}

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

            # Calcular el valor por día para esta persona según las personas a su cargo
            valor_dia = costo_diario_servicio / (personas_a_cargo)
            
            # Agregar la información al informe
            dia_str = dia_actual.strftime('%Y-%m-%d')
            if dia_str not in informe:
                informe[dia_str] = []
            
            informe[dia_str].append({
                'nombre': nombre,
                'invitados': personas_a_cargo - 1,  # No contar al ocupante
                'valor_dia': valor_dia * personas_a_cargo
            })
            
            total_dias_ocupante += (personas_a_cargo - 1)  # Contabilizar los invitados adicionales

        dias_ocupacion_por_persona[nombre] = total_dias_ocupante
        total_dias_ocupacion += total_dias_ocupante
    
    # Ahora calculamos el costo proporcional que cada ocupante debe pagar
    resultados = []
    for nombre, dias_ocupante in dias_ocupacion_por_persona.items():
        proporcion_pago = dias_ocupante / total_dias_ocupacion
        total_a_pagar = valor_servicio_mensual * proporcion_pago
        resultados.append({'nombre': nombre, 'total_a_pagar': total_a_pagar})
    
    return {'resultados': resultados, 'informe': informe}