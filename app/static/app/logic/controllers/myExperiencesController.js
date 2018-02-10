(function(){

	angular
		.module('app.controllers')
		.controller('myExperiencesController', myExperiencesController)

	myExperiencesController.$inject = ["$scope", "$http"]

	function myExperiencesController($scope, $http){

		var that = this;

		that.test = "Holibui";

		that.deleteExperience = deleteExperience;

		function deleteExperience(id, title){
			swal({
				title: "Estás seguro?",
				text: "Si borras tu experiencia, desaparecerá de ConviveTIC",
				icon: "warning",
				buttons: ['Cancelar', 'Borrar'],
				dangerMode: true,
			})
			.then((willDelete) => {
				if (willDelete) {
					var data = {'pk' : id};
					$http.post("/experiences/api/delete_experience", data).then(function(response) {
							swal("Se ha borrado la experiencia", {
								icon: "success"
							}).then(function(){
								location.reload();
							});	
						},function(response){
							if(response.data.error){
								swal({
									title: "Error al borrar la experiencia",
									text: response.data.message,
									icon : "error"
								});
							}
						}
				    );
				}
			});
		}

	}


})();