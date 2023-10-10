class OperationRibbon {
  INTRARE_HTML = `
    <span
    class="inline-flex items-center justify-center rounded-full bg-emerald-100 px-2.5 py-0.5 text-emerald-700"
    >
    <svg xmlns="http://www.w3.org/2000/svg" class="-ms-1 me-1.5 h-4 w-4" width="14" height="14" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
        <path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0"></path>
        <path d="M8 12l4 4"></path>
        <path d="M12 8v8"></path>
        <path d="M16 12l-4 4"></path>
     </svg>

    <p class="whitespace-nowrap text-sm">Intrare</p>
    </span>
    `;

  IESIRE_HTML = `
    <span
    class="inline-flex items-center justify-center rounded-full bg-red-100 px-2.5 py-0.5 text-red-700"
    >
    <svg xmlns="http://www.w3.org/2000/svg" class="-ms-1 me-1.5 h-4 w-4" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
    <path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0"></path>
    <path d="M12 8l-4 4"></path>
    <path d="M12 8v8"></path>
    <path d="M16 12l-4 -4"></path>
    </svg>

    <p class="whitespace-nowrap text-sm">Iesire</p>
    </span>
    `;

  /**
   *
   * @param {string} type
   */
  constructor(type) {

    

    switch(type) {
        case "intrare":
            this.element = this.INTRARE_HTML;
            break;
        case "iesire":
            this.element = this.IESIRE_HTML;
            break;
        default:
            this.element = this.INTRARE_HTML;
    }

  }

}
