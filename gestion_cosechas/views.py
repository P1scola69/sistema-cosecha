from django.shortcuts import render, redirect
from django.contrib import messages
from .bd import conexionBD 

# --- DASHBOARD PRINCIPAL ---
def inicio(request):
    conexion = conexionBD()
    

    sql_recientes = """
        SELECT r.kilos, r.variedad, r.fecha, 
               c.nombre as nom_cosechero, c.apellido as ape_cosechero,
               f.nombre as nom_fundo
        FROM registro_kilos r
        JOIN cosecheros c ON r.cosechero_id = c.id
        JOIN fundos f ON r.fundo_id = f.id
        ORDER BY r.fecha DESC LIMIT 5
    """
    recientes = conexion.consulta(sql_recientes)


    sql_ultimo = """
        SELECT r.kilos, r.variedad, r.fecha, c.nombre as cosechero, f.nombre as fundo
        FROM registro_kilos r
        JOIN cosecheros c ON r.cosechero_id = c.id
        JOIN fundos f ON r.fundo_id = f.id
        ORDER BY r.id DESC LIMIT 1
    """
    ultimo_res = conexion.consulta(sql_ultimo)

    contexto = {
        'recientes': recientes,
        'ultimo': ultimo_res[0] if ultimo_res else None
    }
    return render(request, 'gestion_cosechas/inicio.html', contexto)


def fundos(request):
    conexion = conexionBD()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre_fundo')
        ubicacion = request.POST.get('ubicacion')
        
        sql_check = "SELECT * FROM fundos WHERE nombre = %s"
        existe = conexion.consulta(sql_check, [nombre])
  
        if existe:
            messages.error(request, "Error: Este fundo ya está registrado.")
        else:
            sql_insert = "INSERT INTO fundos (nombre, ubicacion) VALUES (%s, %s)"
            conexion.ejecutarSQL(sql_insert, (nombre, ubicacion))
            messages.success(request, f"Fundo '{nombre}' registrado con éxito.")
        
        return redirect('fundos')
    
    todos_los_fundos = conexion.consulta("SELECT * FROM fundos ORDER BY id DESC")
    return render(request, 'gestion_cosechas/fundos.html', {'fundos': todos_los_fundos})


def formulario_supervisor(request):
    conexion = conexionBD()   
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        rut = request.POST.get('rut')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        contrasena = request.POST.get('contrasena')
        fundo_id = request.POST.get('fundo')
        sql_check = "SELECT * FROM supervisores WHERE rut = %s OR correo = %s"
        existe = conexion.consulta(sql_check, (rut, correo))
        if existe:
            messages.error(request, "Error: El supervisor ya existe (RUT o Correo duplicado).")
        else:
            sql_insert = """
                INSERT INTO supervisores (nombre, apellido, rut, correo, telefono, contrasena, fundo_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            conexion.ejecutarSQL(sql_insert, (nombre, apellido, rut, correo, telefono, contrasena, fundo_id))
            messages.success(request, "Supervisor dado de alta con éxito.")     
        return redirect('supervisor')

    lista_fundos = conexion.consulta("SELECT id, nombre FROM fundos")

    sql_supervisores = """
        SELECT s.nombre, s.apellido, s.rut, s.correo, f.nombre as nombre_fundo
        FROM supervisores s
        LEFT JOIN fundos f ON s.fundo_id = f.id
        ORDER BY s.id DESC
    """
    supervisores_registrados = conexion.consulta(sql_supervisores)

    contexto = {
        'fundos': lista_fundos,
        'supervisores': supervisores_registrados,
        'total_supervisores': len(supervisores_registrados) 
    }
    return render(request, 'gestion_cosechas/formulario_supervisor.html', contexto)      



def formulario_cosechero(request):
    conexion = conexionBD()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        rut = request.POST.get('rut')
        nacionalidad = request.POST.get('nacionalidad')
        telefono = request.POST.get('telefono')
        cuadrilla = request.POST.get('cuadrilla')
        existe = conexion.consulta("SELECT * FROM cosecheros WHERE rut = %s", [rut])
        if existe:
            messages.error(request, "Error: Este RUT ya está registrado en el sistema.")
        else:
            sql = """
                INSERT INTO cosecheros (nombre, apellido, rut, nacionalidad, telefono, cuadrilla) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            conexion.ejecutarSQL(sql, (nombre, apellido, rut, nacionalidad, telefono, cuadrilla))
            messages.success(request, f"Cosechero {nombre} {apellido} registrado.")  
        return redirect('cosechero')  
    todos = conexion.consulta("SELECT * FROM cosecheros ORDER BY id DESC")
    return render(request, 'gestion_cosechas/formulario_cosechero.html', {'cosecheros': todos})


def registro_kilos(request):
    conexion = conexionBD() 

    if request.method == 'POST':
        fundo_id = request.POST.get('fundo')
        cosechero_id = request.POST.get('cosechero')
        supervisor_id = request.POST.get('supervisor')
        variedad = request.POST.get('variedad')
        kilos = request.POST.get('kilos')
        if not all([fundo_id, cosechero_id, supervisor_id, kilos]):
            messages.error(request, "Error: Campos obligatorios vacíos.")
            return redirect('registro_kilos')
        sql_insert = "INSERT INTO registro_kilos (fundo_id, cosechero_id, supervisor_id, variedad, kilos) VALUES (%s, %s, %s, %s, %s)"
        conexion.ejecutarSQL(sql_insert, (fundo_id, cosechero_id, supervisor_id, variedad, kilos))
        messages.success(request, "¡Pesaje guardado!")
        return redirect('inicio') 
    

    sql_hoy = """
        SELECT r.fecha, c.nombre, f.nombre as fundo, r.kilos
        FROM registro_kilos r
        JOIN cosecheros c ON r.cosechero_id = c.id
        JOIN fundos f ON r.fundo_id = f.id
        WHERE DATE(r.fecha) = CURDATE()
        ORDER BY r.fecha DESC
    """
    contexto = {
        'fundos': conexion.consulta("SELECT id, nombre FROM fundos"),
        'cosecheros': conexion.consulta("SELECT id, nombre, apellido FROM cosecheros"),
        'supervisores': conexion.consulta("SELECT id, nombre, apellido FROM supervisores"),
        'pesajes_hoy': conexion.consulta(sql_hoy) 
    }
    return render(request, 'gestion_cosechas/registro_kilos.html', contexto)


def procesar(request):
    conexion = conexionBD()
    rut_buscado = request.GET.get("txt_rut")
    
    contexto = {}

    if rut_buscado:
        sql_persona = "SELECT * FROM cosecheros WHERE rut = %s"
        persona = conexion.consulta(sql_persona, [rut_buscado])

        if persona:
            p = persona[0] 

            sql_historial = """
        SELECT r.fecha, r.variedad, r.kilos, f.nombre as fundo
        FROM registro_kilos r
        LEFT JOIN fundos f ON r.fundo_id = f.id
        WHERE r.cosechero_id = %s
        ORDER BY r.fecha DESC
    """
            historial = conexion.consulta(sql_historial, [p['id']])


            total_kilos = sum(item['kilos'] for item in historial)

            contexto = {
                "persona": p,
                "historial": historial,
                "total_kilos": total_kilos,
                "encontrado": True
            }
        else:
            contexto = {"encontrado": False, "rut": rut_buscado}

    return render(request, 'gestion_cosechas/resultado.html', contexto)