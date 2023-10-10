class StatsContainer {

    /**
     * 
     * @param {string} color 
     */
    constructor(color) {
        this.title = '';
        this.value = '';
        this.color = color;
    }

  
    init() {
        //  Create the html element and set the skeleton
        const mainStats = document.querySelector("#stats");

        var tempDiv = document.createElement('div');
        const innerHTML = `
        <div class="stats-container relative mr-7 my-5 p-3 h-20 w-48 bg-${this.color} rounded-xl shadow-md">
            <h3 id="stats-container__title" class="text-xs text-ellipsis font-medium tracking-wide text-white opacity-75">Loading...</h3>
            <h3 id="stats-container__value" class="text-2xl font-bold text-white">Loading...</h3>
        
        </div>
        `;

        tempDiv.innerHTML = innerHTML.trim();

        //  Set the element to be accessible by the class
        this.element = tempDiv.firstChild;
        //  console.log(this.element);

        //  Append the element to the main container
        mainStats.appendChild(this.element);
        
    }

    update() {
        //  Update the value
        this.element.querySelector('#stats-container__value').textContent = this.value;

        //  Update the title
        this.element.querySelector('#stats-container__title').textContent = this.title;
    }

    /**
     * 
     * @param {Promise} promise 
     */
    async refresh(promise) {

    }


    /**
     *  
     * @param {string} color
     * @param {string} name
     * @param {string} endpoint
     * @param {Promise} promise
     *  
     */
    static async create(
        color, 
        name, 
        promise
        ) {
        const statsContainer = new StatsContainer(color);
        statsContainer.init();

        statsContainer.title = name;
        statsContainer.value = await promise;

        statsContainer.update();
    }

}