class OperationsTable {

    constructor(headList, border, data) {
        this.headList = headList;
        this.hasBorder = border;
        this.entries = data;
    }

    /**
     * 
     * 
     * @returns {HTMLTableElement}
     * 
     */
    __init(elementID) {

        parent = document.querySelector(elementID);
        console.log(elementID);
        console.log(parent);

        //  Create the table element
        let div = document.createElement('div');
        div.classList = `rounded-lg ${this.hasBorder ? "border border-gray-200" : ''}`;

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

         //  Create the body rows
         for(let entry in this.entries) {
            let tr = document.createElement('tr');
            tr.classList = 'h-14 overflow-x-auto';
            //  Create the body cells
            for(let cell in this.entries[entry]) {
                let td = document.createElement('td');
                td.classList = "whitespace-nowrap px-2 py-2 text-gray-700";
                // Append the HTML element
                try {
                    td.appendChild(this.entries[entry][cell]);
                }
                catch {
                    td.innerHTML = this.entries[entry][cell];
                }
                tr.appendChild(td);
            }

            tbody.appendChild(tr);
        }

        //  Append the head to the table
        table.appendChild(thead);
        //  Append the body to the table
        table.appendChild(tbody);

        div.appendChild(table);
        
        parent.appendChild(div);
        //  Return the table
        return table;

    }


    update(data) {
        //  We are going to use this.tableElement
        //  To update the body
        this.entries = data;

        // Create the body
        let tbody = document.createElement('tbody');
        tbody.classList = "divide-y divide-gray-200";

        //  Create the body rows
        for(let entry in this.entries) {
            let tr = document.createElement('tr');
            tr.classList = 'h-14';
            //  Create the body cells
            for(let cell in this.entries[entry]) {
                let td = document.createElement('td');
                td.classList = "whitespace-nowrap px-4 py-2 text-gray-700";
                // Append the HTML element
                try {
                    td.appendChild(this.entries[entry][cell]);
                }
                catch {
                    td.innerHTML = this.entries[entry][cell];
                }
                tr.appendChild(td);
            }

            tbody.appendChild(tr);
        }

        //  Append the body to the table
        this.tableElement.tBodies[0].replaceWith(tbody);
    }


    get getTableElement() {
        return this.tableElement;
    }

    get getEntries() {
        return this.entries;
    }



    /**
     * 
     * @param {Array} headList 
     * @param {Boolean} hasBorder
     * @param {Promise} promise
     */
    static create(elementID, headList, data, hasBorder = true) {
        //  Create the table
        let table = new OperationsTable(headList, hasBorder, data);
        table.tableElement = table.__init(elementID);

        //  Return the table
        return table;

    }

}


class StaticTable {

    constructor(headList, data, border) {
        this.headList = headList;
        this.hasBorder = border;
        this.entries = data;

        //  Create the table element
        let div = document.createElement('div');
        div.classList = `overflow-x-auto h-full rounded-lg ${this.hasBorder ? "border border-gray-200" : ''}`;

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

         //  Create the body rows
         for(let entry in this.entries) {
            let tr = document.createElement('tr');
            tr.className = 'h-14';
            //  Create the body cells
            for(let cell in this.entries[entry]) {
                let td = document.createElement('td');
                td.classList = "whitespace-nowrap px-4 py-2 text-gray-700";
                // Append the HTML element
                try {
                    td.appendChild(this.entries[entry][cell]);
                }
                catch {
                    td.innerHTML = this.entries[entry][cell];
                }
                tr.appendChild(td);
            }

            tbody.appendChild(tr);
        }

        //  Append the head to the table
        table.appendChild(thead);
        //  Append the body to the table
        table.appendChild(tbody);

        div.appendChild(table);

        console.log(table);

        this.tableElement = table;
    }


    update(data) {
        //  We are going to use this.tableElement
        //  To update the body
        this.entries = data;

        console.log("DATA:", data);

        // Create the body
        let tbody = document.createElement('tbody');
        tbody.classList = "divide-y divide-gray-200";

        //  Create the body rows
        for(let entry in data) {
            console.log("ENTRY:", data[entry]);
            let tr = document.createElement('tr');
            tr.className = 'h-14';
            //  Create the body cells
            for(let cell in data[entry]) {
                console.log("CELL:", data[entry][cell]);
                let td = document.createElement('td');
                td.classList = "whitespace-nowrap px-4 py-2 text-gray-700";
                // Append the HTML element
                try {
                    td.appendChild(data[entry][cell]);
                }
                catch {
                    td.innerHTML = data[entry][cell];
                }
                tr.appendChild(td);
            }

            tbody.appendChild(tr);
        }

        //  Append the body to the table
        console.log("BODIES:", this.tableElement.tBodies.length);
        this.tableElement.tBodies[0].replaceWith(tbody);
    }

}

