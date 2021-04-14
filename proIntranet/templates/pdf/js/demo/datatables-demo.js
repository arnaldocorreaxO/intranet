// Call the dataTables jQuery plugin
/*@autor xO  
 Fue modificado para mostrar el datatable en español 
 20190804_1100
 
*/
    $(document).ready(function() {
      $('#dataTable').DataTable({
        
        "language": {
          "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
      }
      });
    });

    $(document).ready(function() {
    $('#dataTable1').DataTable( {
    	 "paging": true,
		"ordering": true,
		"searching": true,
		"language": {
		"url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json",
		"decimal": ".",
		"thousands": ",",

     }})
    });
