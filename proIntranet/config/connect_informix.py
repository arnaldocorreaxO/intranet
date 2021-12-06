import IfxPy

def my_Sample(**Kwargs):
    ConStr = "SERVER=ol_informix1170;DATABASE=pl4sjasu;HOST=10.130.10.250;SERVICE=22767;UID=informix;PWD=cnumtc;"

    try:
        # netstat -a | findstr  9088
        conn = IfxPy.connect( ConStr, "", "")
    except Exception as e:
        print ('ERROR: Connect failed')
        print ( e )
        quit()

# Select records
    sql = """
              select * from 
              sjdoc, sjhst, sjsit, sjcol, sjdiv, outer(sjdpt), outer(sjsec), 
              pscon, sjtem, pscco, sjpag, outer(sjsba), outer(sjcar) 
              where 1 = 1
              AND sjdoc.lega = sjhst.lega 
              AND sjdoc.ndoc = {0}
              --AND sjhst.lega = '6125'
              AND sjhst.mmes = {1}
              AND sjhst.aano = {2}
              and sjhst.lega = sjsit.lega and sjhst.conl = sjcol.conl 
              and sjhst.ccos = pscco.ccos and sjhst.conc = pscon.conc 
              and sjsit.tipo_empl = sjtem.tipo_empl 
              and sjsit.divi = sjdiv.divi and sjsit.depa = sjdpt.depa 
              and sjsit.secc = sjsec.secc and sjsit.cent_pago = sjpag.cent_pago 
              and sjsit.carg = sjcar.carg and pscon.tipo = 'NOR' 
              and sjcol.patr_empl = 'E' and sjsit.foli = sjsit.foli_baja 
              and sjsit.lega = sjsba.lega and sjsit.mone = sjsba.mone 
              and sjsba.ddma_vige = (Select max(ddma_vige) 
              from sjsba b 
              WHERE b.lega = sjsba.lega AND b.ddma_vige <= sjhst.ddma_emis) 
              and sjhst.foli = sjhst.foli_baja
              and sjhst.conl not in (select conc from sjcoc)
              and sjhst.conl not in (select conl from sjcoc)
              order by sjhst.lega ASC, sjhst.conl ASC, sjhst.dbcr ASC
          """.format(Kwargs['pCedula'],Kwargs['pMes'],Kwargs['pAnho'])
    #print(sql)
    stmt = IfxPy.exec_immediate(conn, sql)
    row = IfxPy.fetch_assoc(stmt) #Dictionary {}

    rows={} #Dictionary key:[valores como lista]
    nrows=0 #Nro de Filas  
    while row != False:
      nrows+=1
      # print('###########   DICTIONARY      #############')
      for key,value in row.items(): 
        # print('###########   ITEMS      #############')
        try:
          # print(key,'->',value)
          rows[key].append(value)          
        except KeyError:
          rows[key] = [value]
      row = IfxPy.fetch_assoc(stmt)
    
    if nrows:
      legajos = rows['lega']
      # keys = [*rows.keys()] #Desempaquetar dict 
      keys =['lega','nomb','apel','docu','nomb_carg']
      # keys =['lega','nomb','apel',]
      # print(" ".join(keys))
      print(keys)
      for i in range(0,len(legajos)):
        data=''
        for k in range(0,len(keys)):
          data += str(rows[keys[k]][i]).strip() + "\t"
        print(data + "\n")  
    # Free up memory used by result and then stmt too
    IfxPy.free_result(stmt)
    IfxPy.free_stmt (stmt)

    IfxPy.close(conn)

    print ("Done")

#my_Sample(pCedula='3588321',pMes='7',pAnho='2019')    
