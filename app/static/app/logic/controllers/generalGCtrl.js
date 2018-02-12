(function(){
	'use strict';

	angular
		.module('app.controllers')
		.controller('guidesController', guidesController);

	guidesController.$inject = ["$scope", "$http"];

	function guidesController($scope, $http){
		
		let that = this;

		/* Constantes de plantillas */
		that.TEMP_INTRO = 'TEMP_INTRO';
		that.TEMP_TEST = 'TEMP_TEST';
		that.TEMP_TEXT = 'TEMP_TEXT';
		that.TEMP_TEST_IMAGE = 'TEMP_TEST_IMAGE';
		that.TEMP_TEST_MULTIPLE = 'TEMP_TEST_MULTIPLE';
		that.TEMP_ACTIVITY = 'TEMP_ACTIVITY';
		that.TEMP_CROSSWORD = 'TEMP_CROSSWORD';
		

		/* Mapeo de las guías */
		that.guide1 = {
			'states':[
				{
					'_id':1,
					'type': 'TEMP_INTRO',
					'content':'CON TOLERANCIA CONSTRUIMOS PAZ',
				},
				{
					'_id':2,
					'type': 'TEMP_TEST',
					'content':'¿Qué crees que es la tolerancia?',
				},
				{
					'_id':3,
					'type':'TEMP_TEST',
					'content':'¿Por qué crees que las personas son poco tolerantes?'
				},
				{
					'_id':4,
					'type':'TEMP_TEST',
					'content':'¿Que podrías aportar en tu comunidad para mejorar la sana convivencia?'
				},
				{
					'_id':5,
					'type':'TEMP_TEST_IMAGE',
					'content':'Observa la siguiente imagen y haz un corto relato explicando cómo interpretas cada una de las imágenes.',
					'img_url':'http://via.placeholder.com/200x200'
				},
				{
					'_id':6,
					'type':'TEMP_TEXT',
					'content':`Tolerancia se refiere a la acción y efecto de tolerar. Como tal, la tolerancia se basa en el respeto hacia lo otro o lo que es diferente de lo propio, y puede manifestarse como un acto de indulgencia ante algo
								que no se quiere o no se puede impedir, o como el hecho de soportar o aguantar a alguien o algo.
								La palabra proviene del latín tolerantĭa, que significa ‘cualidad de quien puede aguantar, soportar o aceptar.`
				},
				{
					'_id':7,
					'type':'TEMP_TEXT',
					'content':`La tolerancia es un valor moral que implica el espeto íntegro hacia el otro, hacia sus ideas, prácticas o creencias, independientemente de que choquen o sean diferentes de las nuestras. En este sentido, la tolerancia es también el reconocimiento de las
								diferencias inherentes a la naturaleza humana, a la diversidad de las culturas, las religiones o las maneras de ser o de actuar.`
				},
				{
					'_id':8,
					'type':'TEMP_TEXT',
					'content':`Era el primer día de curso en Villanormal, un pueblo normal y corriente
								en el que nada ni nadie destacaba sobre lo demás. Y es que en
								Villanormal existía una ley de normalidad, en la que se decía cómo
								tenían que ser las cosas para que fueran normales.
								Un día llegó al pueblo una mujer extraña. Había heredado la casa de
								una tía abuela lejana y había decidido irse a vivir allí. Pero como no
								era como los demás, la gente no le dirigía la palabra, y se apartaba de
								su camino al pasar.
								Poco a poco, la gente empezó a ser más y más antipática con ella. La
								mujer estaba muy enfadada, pues no entendía qué pasaba.
								Solo un niño, Tito, el hijo del alcalde, era amable con ella.
								- Te tratan así porque eres diferente -le dijo el niño-. Para ellos no eres
								normal. Pero a mí… A mí me encantaría ser diferente.`,
					'title':'LA TOLERANCIA'
				},
				{
					'_id':9,
					'type':'TEMP_TEXT',
					'content':`- ¿Cómo de diferente? -preguntó la mujer.
								- Me encantaría ser un niño verde -dijo Tito.
								- ¿Y que haría tu padre entonces? -preguntó la mujer.
								- Supongo que no le quedaría más remedio que cambiar la ley de
								normalidad para que no me echaran del pueblo -dijo el niño, riendo
								solo de pensarlo.
								- Yo puedo ayudarte si quieres -dijo la mujer-. Soy bruja. Estoy
								jubilada, pero todavía puedo hacer hechizos interesantes.
								- ¡Claro!
								- De acuerdo. Mañana, antes de ir a clase, ven a verme a casa y haré
								el hechizo.
								A la mañana siguiente, Tito se pasó por casa de la bruja, que lo
								convirtió en un niño verde. Y así se fue el niño al colegio, tan contento
								y como si no pasase nada raro.
								Cuando entró en el colegio, los profesores se pusieron muy nerviosos,
								le riñeron, y quisieron expulsarlo de allí, así que llamaron de inmediato
								a su padre, que no sabía dónde meterse. ¡Su propio hijo, violando la
								ley de normalidad! Eso era algo que no podía soportar.`
				},
				{
					'_id':10,
					'type':'TEMP_TEXT',
					'content':`El niño verdeUna niña se levantó de la mesa y se dirigió a Tito:
							- Me gusta tu nuevo estilo. Yo también estoy harta de ser normal.
							Dime cómo lo has conseguido, porque yo quiero ser rosa.
							Otro niño se levantó gritando que él quería ser rojo, y luego otro
							diciendo que quería ser violenta, y otro diciendo que quería tener la
							piel de lunares.
							Tito, muy satisfecho, le dijo a su padre:
							- Me parece papá, que vas a tener que eliminar la ley de normalidad,
							porque si no este pueblo se va a quedar sin niños.
							Ese día el alcalde cambió la ley y, desde entonces, lo normal en
							Villanormal es que cada uno elija ser como quiera y que todos se
							acepten tal y como son.

							La que no para de trabajar es la bruja, que ahora es la persona más
							importante del pueblo.`
				},
				{
					'_id':11,
					'type':'TEMP_ACTIVITY',
					'content':'Sopa de letras'
				},
				{
					'_id':12,
					'type':'TEMP_TEST_MULTIPLE',
					'content':'Se dice que la tolerancia es la acción que las personas imparten en un grupo determinado o en una comunidad a través de:',
					'answers':['A.La paciencia', 'B.El respeto', 'C.El odio', 'D.La sencillez']
				},
				{
					'_id':13,
					'type':'TEMP_TEST_MULTIPLE',
					'content':'La tolerancia es el respeto que se tienen hacia los otros y hacia nosotros mismos además de estar catalogada como:',
					'answers':['A.Un antivalor', 'B.Una habilidad', 'C.Un valor', 'D.Una destreza']
				},
				{
					'_id':14,
					'type':'TEMP_TEST_MULTIPLE',
					'content':'La tolerancia es también el reconocimiento inherente a la naturaleza de las personas en ello entra:',
					'answers':['A.Las igualdades', 'B.Las similitudes', 'C.Las buenas acciones', 'D.Las diferencias']
				},
				{
					'_id':15,
					'type':'TEMP_CROSSWORD',
					'content':'Crucigrama'
				},
				{
					'_id':16,
					'type':'TEMP_TEXT',
					'content':'Fin'
				}
			]
		}

		/* Variables del estado de la guia */
		that.currentTemplate =  that.TEMP_INTRO; //En qué plantilla se encuentra actualmente
		that.currentGuide = that.guide1; //Guía actual (1,2,3)
		that.currentGuideIndex = 0; //Indica la pos en el arreglo de estado de la guía
		that.currentStateObj = that.currentGuide.states[that.currentGuideIndex]; //Obtiene el objeto con la info del estado actual
		that.statesQuantity = that.currentGuide.states.length; //Cantidad de estados de la guía
		
		/*
		* Cambia al siguiente estado de la guia, se acciona con el botón siguiente
		*/
		that.nextState = () => {
			that.currentGuideIndex++; 
			that.currentStateObj = that.currentGuide.states[that.currentGuideIndex];
			that.currentTemplate = that.currentStateObj.type;
		}


		/*
		* Cambia al anterior estado de la guia, se acciona con el botón anterior
		*/
		that.previousState = () => {
			that.currentGuideIndex--;
			that.currentStateObj = that.currentGuide.states[that.currentGuideIndex];
			that.currentTemplate = that.currentStateObj.type;
		}
	}


})();