// Call the dataTables jQuery plugin
/*@autor xO  
 Fue modificado para mostrar el datatable en español 
 20190804_1100
 
*/
    $(document).ready(function() {
      $('#dataTable1').DataTable({
      	 // "aaSorting": [], 	//No ordenar por ninguna columna por default, no quita la opcion de ordernar de las columnas
      	 "language": {
          "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
      }
      });
    });

/*Para desactivar el orden de la tabla 
  funcionan los sgtes

  "aaSorting": [] 	//No ordenar por ninguna columna por default
  "ordering": false //Quita el orden en todas las columnas 
  "bSort": false    //Quita la opcion de orden de todas las columnas

*/