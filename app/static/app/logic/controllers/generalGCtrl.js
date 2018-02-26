(function(){
	'use strict';

	angular
		.module('app.controllers')
		.controller('guidesController', guidesController);

	guidesController.$inject = ["$scope", "$http", "$sce"];

	function guidesController($scope, $http, $sce){
		
		let that = this;

		/* Constantes de plantillas */
		that.TEMP_INTRO = 'TEMP_INTRO';
		that.TEMP_TEST = 'TEMP_TEST';
		that.TEMP_TEXT = 'TEMP_TEXT';
		that.TEMP_TEST_IMAGE = 'TEMP_TEST_IMAGE';
		that.TEMP_TEST_MULTIPLE = 'TEMP_TEST_MULTIPLE';
		that.TEMP_ACTIVITY = 'TEMP_ACTIVITY';
		that.TEMP_CROSSWORD = 'TEMP_CROSSWORD';
		that.TEMP_FILL_THE_BLANKS = 'TEMP_FILL_THE_BLANKS';
		that.CONST_SEND_ANS = 'Enviar respuestas';

		/* Variables/const para feedback de respuestas */
		that.GOOD_ANSWER = '¡Muy bien!';
		that.BAD_ANSWER = 'Respuesta Incorrecta';
		that.currentFeedback = '';
		that.userHasResponded = false;
		that.finished = false; //El usuario terminó la guía?

		/* Varibles para almacenar respuestas */
		that.requests = []; //Almacena las respuestas dadas por el usuario en el formulario
		that.config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
            }
        };

		/* Mapeo de las guías */
		/*that.guide = {
			'states':[
				{
					'id':1,
					'type': 'TEMP_INTRO',
					'content':'CON TOLERANCIA CONSTRUIMOS PAZ',
					'required':false
				},
				{
					'id':1,
					'type': 'TEMP_FILL_THE_BLANKS',
					'content':'CON TOLERANCIA CONSTRUIMOS PAZ',
					'required':false
				},
				
				{
					'id':2,
					'type': 'TEMP_TEST',
					'content':'¿Qué crees que es la tolerancia?',
					'required':true
				},
				{
					'id':3,
					'type':'TEMP_TEST',
					'content':'¿Por qué crees que las personas son poco tolerantes?',
					'required':true
				},
				{
					'id':4,
					'type':'TEMP_TEST',
					'content':'¿Que podrías aportar en tu comunidad para mejorar la sana convivencia?',
					'required':true
				},
				{
					'id':5,
					'type':'TEMP_TEST_IMAGE',
					'content':'Observa la siguiente imagen y haz un corto relato explicando cómo interpretas cada una de las imágenes.',
					'img_url':'http://via.placeholder.com/200x200',
					'required':true
				},
				{
					'id':6,
					'type':'TEMP_TEXT',
					'content':
						[
							$sce.trustAsHtml(`<span class="text-success">Tolerancia</span> se refiere a la acción y efecto de tolerar. Como tal, la tolerancia se basa en el respeto hacia lo otro o lo que es diferente de lo propio, y puede manifestarse como un acto de indulgencia ante algo
							que no se quiere o no se puede impedir, o como el <span class="text-warning">hecho de soportar o aguantar a alguien o algo.<span>`),
							$sce.trustAsHtml(`La palabra <span class="text-info">proviene del latín tolerantĭa</span>, que significa cualidad de quien puede aguantar, soportar o aceptar.`),
						],
					'required':false
				},
				{
					'id':7,
					'type':'TEMP_TEXT',
					'content':
						[
							$sce.trustAsHtml(`La tolerancia es un <span class="text-success">valor moral</span> que implica el <span class="text-warning">respeto íntegro hacia el otro</span>, hacia sus ideas, prácticas o creencias, independientemente de que choquen o sean diferentes de las nuestras.`), 
							$sce.trustAsHtml(`En este sentido, la tolerancia es también el <span class="text-secondary">reconocimiento de las
							diferencias inherentes a la naturaleza humana</span>, a la diversidad de las culturas, las religiones o las maneras de ser o de actuar.`)
						],
					'required':false
				},
				{
					'id':8,
					'type':'TEMP_TEXT',
					'content':
						[
							$sce.trustAsHtml(`Era el primer día de curso en Villanormal, un pueblo normal y corriente en el que nada ni nadie destacaba sobre lo demás. Y es que en Villanormal existía una ley de normalidad, en la que se decía cómo tenían que ser las cosas para que fueran normales.`),

							$sce.trustAsHtml(`Un día llegó al pueblo una mujer extraña. Había heredado la casa de una tía abuela lejana y había decidido irse a vivir allí. Pero como no era como los demás, la gente no le dirigía la palabra, y se apartaba de su camino al pasar.`),

							$sce.trustAsHtml(`Poco a poco, la gente empezó a ser más y más antipática con ella. La mujer estaba muy enfadada, pues no entendía qué pasaba. Solo un niño, Tito, el hijo del alcalde, era amable con ella.`)
						],
					'title':'LA TOLERANCIA',
					'required':false
				},
				{
					'id':9,
					'type':'TEMP_TEXT',
					'content':
						[	
							$sce.trustAsHtml(`- Te tratan así porque eres diferente -le dijo el niño-. Para ellos no eres normal. Pero a mí… A mí me encantaría ser diferente.`),

							$sce.trustAsHtml(`- ¿Cómo de diferente? -preguntó la mujer.<br> - Me encantaría ser un niño verde -dijo Tito.<br> - ¿Y que haría tu padre entonces? -preguntó la mujer.<br> - Supongo que no le quedaría más remedio que cambiar la ley de normalidad para que no me echaran del pueblo -dijo el niño, riendo solo de pensarlo.<br> - Yo puedo ayudarte si quieres -dijo la mujer-. Soy bruja. Estoy jubilada, pero todavía puedo hacer hechizos interesantes.<br> - ¡Claro!<br> - De acuerdo. Mañana, antes de ir a clase, ven a verme a casa y haré el hechizo.`)							
						],
					'required':false
				},
				{
					'id':10,
					'type':'TEMP_TEXT',
					'content':
						[
							$sce.trustAsHtml(`A la mañana siguiente, Tito se pasó por casa de la bruja, que lo convirtió en un niño verde. Y así se fue el niño al colegio, tan contento y como si no pasase nada raro.`),

							$sce.trustAsHtml(`Cuando entró en el colegio, los profesores se pusieron muy nerviosos, le riñeron, y quisieron expulsarlo de allí, así que llamaron de inmediato a su padre, que no sabía dónde meterse. ¡Su propio hijo, violando la ley de normalidad! Eso era algo que no podía soportar.`),

							$sce.trustAsHtml(`Una niña se levantó de la mesa y se dirigió a Tito:`),

							$sce.trustAsHtml(`- Me gusta tu nuevo estilo. Yo también estoy harta de ser normal. Dime cómo lo has conseguido, porque yo quiero ser rosa.`)
						],
					'required':false

				},
				{
					'id':11,
					'type':'TEMP_TEXT',
					'content':
						[
							$sce.trustAsHtml(`Otro niño se levantó gritando que él quería ser rojo, y luego otro diciendo que quería ser violenta, y otro diciendo que quería tener la piel de lunares.`),

							$sce.trustAsHtml(`Tito, muy satisfecho, le dijo a su padre:`),

							$sce.trustAsHtml(`- Me parece papá, que vas a tener que eliminar la ley de normalidad, porque si no este pueblo se va a quedar sin niños.`),

							$sce.trustAsHtml(`Ese día el alcalde cambió la ley y, desde entonces, lo normal en Villanormal es que cada uno elija ser como quiera y que todos se acepten tal y como son.`),

							$sce.trustAsHtml(`La que no para de trabajar es la bruja, que ahora es la persona más importante del pueblo.`)
						],
					'required':false
				},
				{
					'id':12,
					'type':'TEMP_ACTIVITY',
					'content':'Sopa de letras',
					'required':false
				},
				{
					'id':13,
					'type':'TEMP_TEST_MULTIPLE',
					'content':'Se dice que la tolerancia es la acción que las personas imparten en un grupo determinado o en una comunidad a través de:',
					'answers':['A. La paciencia', 'B. El respeto', 'C. El odio', 'D. La sencillez'],
					'correct':0,
					'required':true
				},
				{
					'id':14,
					'type':'TEMP_TEST_MULTIPLE',
					'content':'La tolerancia es el respeto que se tienen hacia los otros y hacia nosotros mismos además de estar catalogada como:',
					'answers':['A. Un antivalor', 'B. Una habilidad', 'C. Un valor', 'D. Una destreza'],
					'correct':1,
					'required':true
				},
				{
					'id':15,
					'type':'TEMP_TEST_MULTIPLE',
					'content':'La tolerancia es también el reconocimiento inherente a la naturaleza de las personas en ello entra:',
					'answers':['A. Las igualdades', 'B. Las similitudes', 'C. Las buenas acciones', 'D. Las diferencias'],
					'correct':2,
					'required':true
				},
				{
					'id':16,
					'type':'TEMP_CROSSWORD',
					'content':'Crucigrama',
					'required':false
				},
				{
					'id':17,
					'type':'TEMP_TEXT',
					'content':[
						$sce.trustAsHtml('<span class="text-secondary final-text">¡Gracias por tus respuestas!</span><br> <span class="final-desc">Presiona el botón Enviar respuestas para terminar.</span>')
					]
				}
			]
		}*/
		that.guide = {};

		/* Variables del estado de la guia */
		that.currentTemplate =  that.TEMP_INTRO; //En qué plantilla se encuentra actualmente
		that.currentGuide = {"states":[]};
		that.currentGuideIndex = 0; //Indica la pos en el arreglo de estado de la guía
		that.currentStateObj = {}; //Obtiene el objeto con la info del estado actual
		that.statesQuantity = 0; //Cantidad de estados de la guía
		that.answersVisibles = false; //Indica si deben mostrarse o no las respuestas de la pregunta actual. 

		that.guideInfo = null;
		
		that.init = (data) =>{
			
			that.guideInfo = data[0].fields || {};
			data = data.slice(1, data.length);
			console.log(data);
			let questions = [];
			
			data.forEach(function(e){

				let question = {};
				question["id"] = e.pk;
				question["type"] = e.fields.q_type; 
				question["required"] = e.fields.required;

				switch(question["type"]){
					case that.TEMP_INTRO:
					case that.TEMP_TEST:
					case that.TEMP_CROSSWORD:
						question["content"] = e.fields.content;

						break;

					case that.TEMP_TEXT:
						question["content"] = $sce.trustAsHtml(e.fields.content);
						if(e.fields.title)
							question["title"] = e.fields.title;
						
						break;

					case that.TEMP_TEST_MULTIPLE:
						question["content"] = $sce.trustAsHtml(e.fields.content);
						question["correct"] = e.fields.correct_answer;
						let answers = e.fields.answers_av.split(",");
						question["answers"] = answers;

						break;

					case that.TEMP_TEST_IMAGE:
						question["img_url"] = e.fields.img;
						question["content"] = e.fields.content;
						break;

					case that.TEMP_FILL_THE_BLANKS:
						question["content"] = $sce.trustAsHtml(e.fields.content);
						question["fill_answer"] = e.fields.fill_answer;
						question["title"] = e.fields.title;
						question["content_temp"] = e.fields.content_templ;
						break;

					case that.TEMP_ACTIVITY:
						question["content"] = e.fields.content;
						question["title"] = e.fields.title;
						break;
				}

				questions.push(question);
				
			});

			that.guide["states"] = questions;
			that.currentGuide = that.guide;
			that.statesQuantity = that.currentGuide.states.length;
			that.currentStateObj = that.currentGuide.states[0];
		}

		/*
		* Cambia al siguiente estado de la guia, se acciona con el botón siguiente
		*/
		that.nextState = () => {
			that.reviewRequirements();

			if(that.finished){
				that.sendAnswers();
				return;
			}
			

			//Se si cumplen los requisitios del estado actual o no hay requisitos ...
			if((that.currentStateObj.required && that.userHasResponded) || that.currentStateObj.required == false){
				that.saveAnswer();
				that.currentGuideIndex++; 
				that.currentStateObj = that.currentGuide.states[that.currentGuideIndex];
				that.currentTemplate = that.currentStateObj.type;
				that.updateLoader();


				that.answersVisibles = false; //Reiniciar el estado de las preguntas
				that.restartViews();
				that.verifyLast();
			}else{
				swal("Respuesta requerida", "Para continuar debes dar una respuesta");
			}

		}


		/*
		* Cambia al anterior estado de la guia, se acciona con el botón anterior
		*/
		that.previousState = () => {
			that.currentGuideIndex--;
			that.currentStateObj = that.currentGuide.states[that.currentGuideIndex];
			that.currentTemplate = that.currentStateObj.type;
			that.updateLoader();
		}

		/*
		* Actualiza la barra de progreso de la parte superior
		*/
		that.updateLoader = () => {
			let loader_per = (that.currentGuideIndex/(that.statesQuantity-1))*100;
			angular.element(".current").width(loader_per+'%');
		}


		/*
		* Valida la respuesta de preguntas multiples y las colorea como correspondan
		*/
		that.validateAnswer = (answer) => {
			if(that.answersVisibles){
				if(that.currentStateObj.correct == that.currentStateObj.answers.indexOf(answer)){
					return 'good-answer';
				}
				return 'bad-answer';
			}
			return '';
		}

		/*
		* Activa la opción de mostrar respuestas de una pregunta y muestra el feedback del footer
		*/
		that.showAnswersAndFeedback = (answer, ans_n) => {
			that.answersVisibles = true;
			angular.element(".next-btn").addClass("next-btn-feedback");
			if(that.currentStateObj.correct == that.currentStateObj.answers.indexOf(answer)){
				angular.element(".footer-guide").addClass("good-answer");
				that.currentFeedback = that.GOOD_ANSWER;
			}else{
				angular.element(".footer-guide").addClass("bad-answer");
				that.currentFeedback = that.BAD_ANSWER;
			}

			angular.element(".ans-"+ans_n).addClass("selected");

		}

		/*
		* Reinicia las vistas y variables encargadas del feedback
		*/
		that.restartViews = () => {
			angular.element(".footer-guide").removeClass("good-answer");
			angular.element(".footer-guide").removeClass("bad-answer");
			angular.element(".next-btn").removeClass("next-btn-feedback");

			that.currentFeedback = '';
			that.currentAnswer = '';
			that.userHasResponded = false;

			//Vista de intro
			angular.element(".test_input").val("");
		}

		/*
		* Se encarga de verificar si el estado actual es el último
		*/
		that.verifyLast = () => {
			if(that.currentGuideIndex == (that.currentGuide.states.length)-1){
				angular.element(".next-btn").text(that.CONST_SEND_ANS);
				that.finished = true;
			}
		}

		that.reviewRequirements = () =>{

			switch(that.currentStateObj.type){
				case that.TEMP_TEST:
					(angular.element(".test_input").val().trim() != "") ? that.userHasResponded=true : that.userHasResponded=false;
					break;

				case that.TEMP_TEST_IMAGE:
					(angular.element(".test_image_input").val().trim() != "") ? that.userHasResponded=true : that.userHasResponded=false;
					break;

				case that.TEMP_TEST_MULTIPLE:
					(that.answersVisibles) ? that.userHasResponded = true : that.userHasResponded = false;
					break;
			}
		}

		that.saveAnswer = () =>{
			let currentAnswer = '';
			switch(that.currentStateObj.type){
				case that.TEMP_TEST:
					currentAnswer = angular.element(".test_input").val();		
					break;
				case that.TEMP_TEST_IMAGE:
					currentAnswer = angular.element(".test_image_input").val();
					break;
				case that.TEMP_TEST_MULTIPLE:
					currentAnswer = angular.element(".selected").text();
					break;
				case that.TEMP_FILL_THE_BLANKS:
					let selects = document.getElementsByClassName("fill-option");
					currentAnswer = that.currentStateObj.content_temp;

					for (var i = 0; i < selects.length; i++) {
						let sel_resp = (selects[i].options[selects[i].selectedIndex]).text;
						currentAnswer = currentAnswer.replace("#", sel_resp);
					}

					break;
			}	

			if(currentAnswer != undefined && currentAnswer  != ''){
				let data = $.param({
					id:that.currentStateObj.id,
					answer:currentAnswer,
					toolbox:that.guideInfo.guide_n
				});

				let request = () =>{
					return new Promise((resolve, reject) => {
						$http.post("/guides/addAnswer", data , that.config).then(function successCallBack(res){
							console.log("Exitoso");
						}, function errorCallback(resp){
							console.log("Error");
						});
					});
				}

				that.requests.push(request);
				console.log(that.requests);
			}
		}

		that.sendAnswers = () =>{
			let addReview = () =>{

				let data = $.param({
					toolbox:1
				});

				return new Promise((resolve, reject) =>{
					$http.post("/guides/addReview", data, that.config).then(function successCallBack(res){
						console.log("Exitoso");
					}, function errorCallback(res){
						console.log("Error");
					});
				});
			}

			Promise.all([that.requests[0](), that.requests[1](), that.requests[2](),
				that.requests[3](),that.requests[4](),that.requests[5](),
				that.requests[6](), addReview()]).then(values=>{
				console.log("Exitoso");

			}, reason =>{
				console.log(values);
			});
		}

	}


})();