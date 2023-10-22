class TextInput {

    constructor(
        
    ) {

    }

    __init(
        elementID, formID, label, placeholder, type = 'text', required = false, svg = null, onChange = null
    ) {

        const INNER_HTML = `
        <div class="relative mr-10">
              <label for="${formID}" class="sr-only"> ${label} </label>

              <input
                type="${type}"
                id="${formID}"
                placeholder="${placeholder}"
                ${required ? 'required' : ''}
                class="w-full min-w-[100px] rounded-md border-gray-200 shadow-sm sm:text-sm"
              />

              <span
                class="pointer-events-none absolute inset-y-0 end-0 grid w-10 place-content-center text-gray-500"
              >
                ${svg ?? ''}
              </span>
            </div>
        `.trim();

        let element = new DOMParser().parseFromString(
            INNER_HTML, 'text/html'
        ).body.firstElementChild;

        try {
            let parent = document.querySelector(`${elementID}`);
            parent.appendChild(element);
        }
        catch {
            console.log('The elementID is not valid.');
        }

        //  Add the onChange event listener
        if(onChange != null) {
            element.querySelector('input').addEventListener('input', onChange);
        }
        
        //  console.log(element);
        return element;

    }

    get value() {
        return this.htmlElement.querySelector('input').value;
    }

    set value(text) {
        this.htmlElement.querySelector('input').value = text;
    }

    set placeholder(text) {
        this.htmlElement.querySelector('input').placeholder = text;
    }


    static create(
        elementID, formID, label, placeholder, type = 'text', required = false, svg = null, onChange = null
    ) {

        let textInput = new TextInput();
        textInput.htmlElement = textInput.__init(
            elementID, formID, label, placeholder, type, required, svg, onChange
        );

        //  console.log(textInput.htmlElement);
        return textInput;

    }


}