class TextInput {

    constructor(
        
    ) {

    }

    __init(
        elementID, formID, label, placeholder, type = 'text', required = false, svg = null,
    ) {

        const INNER_HTML = `
        <div class="relative mr-10">
              <label for="${formID}" class="sr-only"> ${label} </label>

              <input
                type="${type}"
                id="${formID}"
                placeholder="${placeholder}"
                ${required ? 'required' : ''}
                class="w-full rounded-md border-gray-200 pe-10 shadow-sm sm:text-sm"
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

        let parent = document.querySelector(`${elementID}`);
        parent.appendChild(element);
        
        //  console.log(element);
        return element;

    }

    get getValue() {
        return this.htmlElement.querySelector('input').value;
    }

    set setValue(text) {
        this.htmlElement.querySelector('input').value = text;
    }


    static create(
        elementID, formID, label, placeholder, type = 'text', required = false, svg = null,
    ) {
        let textInput = new TextInput();
        textInput.htmlElement = textInput.__init(
            elementID, formID, label, placeholder, type, required, svg
        );

        //  console.log(textInput.htmlElement);
        return textInput;

    }


}