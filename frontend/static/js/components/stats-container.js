class StatsContainer {

    /**
     * 
     * @param {string} color 
     */
    constructor(initVal) {
        this.value = initVal;
    }

  
    __init(
        elementID,
        color,
        name,
        initVal
    ) {
        //  Create the html element and set the skeleton
        const mainStats = document.querySelector(elementID);

        var tempDiv = document.createElement('div');
        const innerHTML = `
        <div class="stats-container mr-7 my-5 p-3 h-16 lg:h-20 w-42 lg:w-48 bg-${color} rounded-xl shadow-md">
            <h3 id="stats-container__title" class="text-xs text-ellipsis font-medium tracking-wide text-white opacity-75">${name}</h3>
            <h3 id="stats-container__value" class="text-2xl font-bold text-white">${initVal}</h3>
        
        </div>
        `;

        tempDiv.innerHTML = innerHTML.trim();
        let element = tempDiv.firstChild;


        //  Append the element to the main container
        mainStats.appendChild(element);

        return element;
        
    }

    update(value) {
        //  Update the value
        this.elementHTML.querySelector('#stats-container__value').textContent = value;
    }


    /**
     *  
     * @param {string} color
     * @param {string} name
     * @param {string} endpoint
     * @param {Promise} promise
     *  
     */
    static create(
        parentElement,
        color, 
        name, 
        initVal
        ) {
        const statsContainer = new StatsContainer(initVal);
        statsContainer.elementHTML = statsContainer.__init(parentElement, color, name, initVal);
        
        return statsContainer;

    }

}