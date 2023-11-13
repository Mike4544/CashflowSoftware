const NODE_PATH = "../node_modules/";

import Datepicker from '../node_modules/vanillajs-datepicker/js/Datepicker.js';


export default main();

function main() {

    const dateButton = document.querySelector('#additional__date', {
        buttonClass: 'btn',
    });
    
    const datepicker = new Datepicker(dateButton, {

    });

}