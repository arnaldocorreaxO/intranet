import psycopg2
import psycopg2.extras

def getIdentificaciones(**Kwargs):
	PSQL_HOST = "10.130.10.117"
	PSQL_PORT = "5434"
	PSQL_USER = "postgres"
	PSQL_PASS = "P0$tGr3$.."
	PSQL_DB   = "identificaciones"
	try	:
		# Conectarse a la base de datos
		connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
		print(connstr)
		conn = psycopg2.connect(connstr)
		# Abrir un cursor para realizar operaciones sobre la base de datos
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

		# Ejecutar una consulta SELECT
		sqlquery = """SELECT 
							per_codcci, 
							per_apynom, 
							per_nombres, 
							TO_DATE(per_fchnaci,'YYYY-MM-DD')::char(10) AS per_fchnaci,
							nac_codpais,
							CASE civ_codeciv
							WHEN '-1' THEN 'DE'
							WHEN '0' THEN 'DE'
							WHEN 'ME' THEN 'DE'
							ELSE
							civ_codeciv
							END, 
							per_desdomi 
						FROM personas 
						WHERE 
						per_codcci = '{vCedula}';""".format(**Kwargs)
		#print(sqlquery)
		cur.execute(sqlquery)

		# Obtener los resultados como objetos Python
		allresults = cur.fetchall()
		#print(dictionary)
		results = []
		for row in allresults:
			results.append(dict(row))        
		#return lista

		#print(results)

		# Cerrar la conexión con la base de datos
		cur.close()
		conn.close()

		# Recuperar datos del objeto Python
		username = row[1]

		# Hacer algo con los datos
		#print(username)

		return results

	except psycopg2.Error as e:
		print("Error de base de datos",e)
		
	"""
	A continuación, debe recuperar el cursor para trabajar. Eso simplemente se hace con

	cursor = connection.cursor()            
	Ahora podrá enviar sus consultas SQL a su base de datos

	cursor.execute("SELECT * from my_db_table")
	Para buscar las filas de resultados

	rows = cursor.fetchall()    
	for row in rows:
		print "   ", row[0]
	"""
