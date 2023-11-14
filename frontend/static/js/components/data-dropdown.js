class DataDropdown {
  constructor() {}

  __init(htmlID, formID, name, elements) {
    //  Get the parent
    let parent = document.querySelector(htmlID);

    //  Create the element
    let element = document.createElement("div");
    element.classList = "mr-10";

    //  Create the closed dropdownCreate the label child
    let labelHTML = `
        <label
                for="${formID}"
                class="block text-sm font-medium text-gray-900"
              >
                ${name}
              </label>
        `;

    let optionsHTML = elements
      .map((element) => `<option value="${element}">${element}</option>`)
      .join("");

    let selectHTML = `
        <select
        name="${formID}"
        id="${formID}"
        class="mt-1.5 w-full rounded-lg border-gray-300 text-gray-700 sm:text-sm"
      >
        ${optionsHTML}
      </select>
        `;

    element.innerHTML = labelHTML + selectHTML;

    //  Append the element
    parent.appendChild(element);

    return element;
  }

  get getValue() {
    return this.htmlElement.value;
  }

  static create(htmlID, formID, name, elements) {
    let dropdown = new DataDropdown();
    dropdown.htmlElement = dropdown.__init(htmlID, formID, name, elements);
    return dropdown;
  }
}
