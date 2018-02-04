(function(){
	'use strict';

	angular
		.module('app.controllers')
		.controller('contactController', contactController)

	contactController.$inject = ["$scope", "$http"];

	function contactController($scope, $http){
		var that = this;
		that.name = "";
		that.lastname = "";
		that.email = ""
		that.comment = "";
		that.phone = "";
		that.sendForm = sendForm;
		that.contactUsMessage = contactUsMessage;
		that.showSuccessMessage = showSuccessMessage;
		that.showErrorMessage = showErrorMessage;


		function sendForm(){
			if($scope.form.$valid){
				//$("#contact-form").submit();
			}
		}

		function contactUsMessage(){
			if(that.name != "" && that.lastname != "" 
				&& that.email != "" && that.phone != "" && that.comment != ""){

				$.ajax({
			    	type: 'POST',
			    	url: '../../send_email',
			    	data: {
						'name': "",
						'lastname': "",
						'email': "",
						'comment': "",
						'phone': ""
					},
			    	success : function(data){
			    		if (data.type == "Success") {
				    		that.showSuccessMessage(data.message);
							that.refreshForm();	    		
			    		}else if(data.type == "error"){
			    			that.showErrorMessage(data.message);
			    		}
			    	},
			    	error : function(data){
			    		that.showErrorMessage(data.message);
			    	}
			    });
			}else{
				alert("ingresa la informacion");
			}
		}
		function refreshForm(){
			that.name = "";
			that.lastname = "";
			that.email = ""
			that.comment = "";
			that.phone = "";
		}

		function showSuccessMessage(message){
			swal({
			  title: "Gracias !",
			  text: message,
			  icon: "success",
			  button: "Aceptar",
			});
		}
		function showErrorMessage(message){
			swal({
			  title: "Ups !",
			  text: message,
			  icon: "error",
			  button: "Aceptar",
			});
		}
	}
})();

