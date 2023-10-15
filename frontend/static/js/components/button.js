class Button {
    constructor() {

    }

    __init(
        elementID, text, svg = null, onClick = null
    ) {

        const INNER_HTML = `
        <button
            class="cursor-pointer inline-flex items-center gap-2 rounded border border-blue-600 bg-blue-600 px-8 py-3 text-white hover:bg-transparent hover:text-blue-600 focus:outline-none focus:ring active:text-blue-500"
          >
            <span class="text-sm font-medium"> ${text} </span>

            ${svg ?? ''}
          </button>
        `;

        let element = document.createElement('div');
        element.innerHTML = INNER_HTML;
        element = element.firstElementChild;

        let parent = document.querySelector(`${elementID}`);
        parent.appendChild(element);

        if(onClick != null) {
            element.addEventListener('click', onClick);
            console.log(onClick);
        }

        return element;

    }

    static create(
        elementID, text, svg = null, onClick = null
    ) {
        let button = new Button();
        button.htmlElement = button.__init(
            elementID, text, svg, onClick
        );

        return button;
    }
}