class OperationsTable {

    constructor(headList) {
        this.headList = headList;
        this.entries = [];
    }

    /**
     * 
     * 
     * @returns {HTMLTableElement}
     * 
     */
    init() {

        //  Create the table element
        let parent = document.currentScript.parentElement;

        let div = document.createElement('div');
        div.classList = "overflow-x-auto rounded-lg border border-gray-200";

        let table = document.createElement('table');
        //  Add the tailwind classes
        table.classList = "min-w-full divide-y-2 divide-gray-200 bg-white text-sm"

        //  Create the head
        let thead = document.createElement('thead');
        thead.classList = "text-left";

        //  Create the head rows
        for(let entry in this.headList) {
            let th = document.createElement('th');
            th.classList = "whitespace-nowrap px-4 py-2 font-medium text-gray-900";
            th.textContent = this.headList[entry];
            thead.appendChild(th);
        }

        // Create the body
        let tbody = document.createElement('tbody');
        tbody.classList = "divide-y divide-gray-200";

        //  Create a placeholder body row
        let tr = document.createElement('tr');
        let td = document.createElement('td');
        td.classList = "whitespace-nowrap px-4 py-2 text-gray-700";
        td.textContent = "Loading...";
        tr.appendChild(td);
        tbody.appendChild(tr);

        //  Append the head to the table
        table.appendChild(thead);
        //  Append the body to the table
        table.appendChild(tbody);

        div.appendChild(table);
        //  Append the table to the parent
        parent.appendChild(div);
        //  Return the table
        return table;

    }


    update() {
        //  We are going to use this.tableElement
        //  To update the body

        // Create the body
        let tbody = document.createElement('tbody');
        tbody.classList = "divide-y divide-gray-200";

        //  Create the body rows
        for(let entry in this.entries) {
            let tr = document.createElement('tr');
            //  Create the body cells
            for(let cell in this.entries[entry]) {
                let td = document.createElement('td');
                td.classList = "whitespace-nowrap px-4 py-2 text-gray-700";
                td.innerHTML = this.entries[entry][cell];
                tr.appendChild(td);
            }

            tbody.appendChild(tr);
        }

        //  Append the body to the table
        this.tableElement.tBodies[0].replaceWith(tbody);
    }


    /**
     * 
     * @param {Promise} promise 
     */
    async refresh(promise) {

    }

    /**
     * 
     * @param {Array} headList 
     * @param {Promise} promise
     */
    static async create(headList, promise) {
        //  Create the table
        let table = new OperationsTable(headList);
        table.tableElement = table.init();
        //  Update the table with the data
        table.entries = await promise;
        table.update();
        //  Return the table
        return table;

    }

}