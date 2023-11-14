class Dropdown {
  constructor(name, elements) {
    this.name = name;
    this.elements = elements;
    this.isOpen = false;

    let element = document.createElement("div");
    element.classList = "relative";

    let closedDropdownHTML = `
        <div
          class="inline-flex items-center overflow-hidden rounded-md border bg-white"
        >
          <a
            class="border-e px-4 py-2 text-sm/none text-gray-600 hover:bg-gray-50 hover:text-gray-700"
          >
            ${this.name}
          </a>
      
          <button
            id="dropdownButton"
            class="h-full p-2 text-gray-600 hover:bg-gray-50 hover:text-gray-700"
          >
            <span class="sr-only">Menu</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
        `;

    let openDropdownHTML = `
        <div
        id="closedPart"
        class="hidden absolute overflow-auto end-0 z-10 mt-2 w-56 lg:w-80 h-36 lg:h-48 rounded-md border border-gray-100 bg-white shadow-lg"
        role="menu"
      >
        <div id="elements" class="p-2">
          
        </div>
      </div>
    </div>
        `;

    element.innerHTML = closedDropdownHTML + openDropdownHTML;

    //  Add the elements
    let elementsDiv = element.querySelector("#elements");
    for (let element of this.elements) {
      console.log(element);
      try {
        elementsDiv.appendChild(element);
      } catch {
        elementsDiv.innerHTML += element;
      }
    }

    let button = element.querySelector("#dropdownButton");

    button.addEventListener("click", () => {
      let closedPart = element.querySelector("#closedPart");

      closedPart.classList.toggle("hidden");
    });

    this.htmlElement = element;
  }
}
