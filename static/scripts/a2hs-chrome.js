//https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Add_to_home_screen#How_do_you_make_an_app_A2HS-ready

let deferredPrompt;
const addBtn = document.getElementById('add-button');
addBtn.style.display = 'none';

window.addEventListener('beforeinstallprompt', (e) => {

	//Prevent Chrome 67 and earlier from automatically showing the prompt
	e.preventDefault();

	// Stash the event so it can be triggered later.
	deferredPrompt = e;
	addBtn.style.display = 'block';

	addBtn.addEventListener('click', (e) => {
	
		//Hide the user interface that shows our A2HS button
		addBtn.style.display = 'none';

		//Show the prompt
		deferredPrompt.prompt();

		//Wait for the user to respond to the prompt
		deferredPrompt.userChoice.then((choiceResult) => {

			// if(choiceResult.outcome === 'accepted'){
			// 	console.log('User accepted the A2HS prompt');
			// }else{
			// 	console.log('User dismissed the A2HS prompt');
			// }

			deferredPrompt = null;
		});

	});

});