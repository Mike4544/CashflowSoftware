       $(document).ready(function(){
	      $(".xp-menubar").on('click',function(){
		    $("#sidebar").toggleClass('active');
			$("#content").toggleClass('active');
		  });
		  
		  $('.xp-menubar,.body-overlay').on('click',function(){
		     $("#sidebar,.body-overlay").toggleClass('show-nav');
		  });
		  
	   });



let table = new DataTable('#myTable');
let table2 = new DataTable('#myTable2');



document.addEventListener("DOMContentLoaded", async function () {
    // Găsește butonul "Adaugă"
    var addButton = document.querySelector("#addEmployeeModal .btn-success");
    addButton.setAttribute('kstate', "add");
  
    // Adaugă un eveniment de click pe buton
    addButton.addEventListener("click", async function (e) {
      e.preventDefault();

      // Găsește toate câmpurile de input din modal
      var inputFields = document.querySelectorAll("#addEmployeeModal input");
  
      // Creează un nou rând în tabel
      var table = document.querySelector("#myTable tbody");


      var newRow = table.insertRow(table.rows.length);
  
      // Adaugă celule în rândul nou creat și populează-le cu valorile din câmpurile de input
      for (var i = 0; i < inputFields.length; i++) {
        var cell = newRow.insertCell(i);
        cell.innerText = inputFields[i].value;
      }

      let sendBody = {};
      inputFields.forEach((entry) => {
        sendBody[entry.id] = entry.value;
      });

      console.log(sendBody);

      //  TODO: Handle the sending
      let kType = addButton.getAttribute('ktype');

      const response = await fetch(`/api/cashflow/add/${kType}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sendBody),
      });

      if (response.ok) {
        console.log('Success!');
      }
      else {
        console.log('Error!');
      }
  
      // Închide modalul după adăugarea datelor
      $('#addEmployeeModal').style = "display: none";
      $('#addEmployeeModal').modal('hide');
  
      // Resetează valorile câmpurilor de input din modal

      $('#addEmployeeModal input').val('');

    });
  });

  var currentID;

  document.addEventListener("DOMContentLoaded", async function () {
    // Găsește toate butoanele "Editează" din tabel
    var editButtons = document.querySelectorAll("#myTable a.edit");
    var deleteButtons = document.querySelectorAll("#myTable a.delete");

    // Adaugă un eveniment de click pe fiecare buton "Editează"
    editButtons.forEach(async function (button) {
        button.addEventListener("click", async function () {
            // Găsește rândul corespunzător butonului "Editează"
            var row = this.closest("tr");

            currentID = row.getAttribute('entryid');

            // Găsește toate câmpurile de input din modalul de editare
            var inputFields = document.querySelectorAll("#editEmployeeModal input");

            // Găsește toate celulele din rândul tabelului
            var cells = row.querySelectorAll("td");

            // Populează câmpurile cu valorile din rândul tabelului
            for (var i = 0; i < inputFields.length; i++) {
                inputFields[i].value = cells[i].innerText;
            }

            var saveButton = document.querySelector("#editEmployeeModal .btn-success");
            saveButton.setAttribute('kstate', "edit");

            // Deschide modalul de editare
            $('#editEmployeeModal').modal('show');
        });
    });

    // Adaugă un eveniment de click pe fiecare buton "Șterge"
    deleteButtons.forEach(async function (button) {
        button.addEventListener("click", async function () {
            currentID = this.closest("tr").getAttribute('entryid');

        });
    });


    // Găsește butonul "Salvează" din modalul de editare
    var saveButton = document.querySelector("#editEmployeeModal .btn-success");

    // Adaugă un eveniment de click pe butonul "Salvează"
    saveButton.addEventListener("click", async function () {

        // Găsește toate câmpurile de input din modalul de editare
        var inputFields = document.querySelectorAll("#editEmployeeModal input");


        let sendBody = {};
        inputFields.forEach((entry) => {
            sendBody[entry.id] = entry.value;
        });

        console.log(sendBody);

        //  TODO: Handle the sending
        let kType = saveButton.getAttribute('ktype');

        const response = await fetch(`/api/cashflow/update/${kType}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: currentID,
            ...sendBody,
          }),
        });

        if (response.ok) {
          console.log('Success!');

          var row = document.querySelector(`#myTable tr[entryid="${currentID}"]`);
          var cells = row.querySelectorAll('td');
          for (var i = 0; i < inputFields.length; i++) {
            cells[i].innerText = inputFields[i].value;
          }
        }
        else {
          console.log('Error!');
        }

        // Închide modalul de editare după salvare
        $('#editEmployeeModal').modal('hide');

        // Set the state to add
        saveButton.setAttribute('kstate', "add");
    });


    var confirmDelete = document.querySelector("#deleteEmployeeModal .btn-danger");

    confirmDelete.addEventListener("click", async function () {

      let kType = confirmDelete.getAttribute('ktype');

      const response = await fetch(`/api/cashflow/delete/${kType}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: currentID
        }),
      });

      if (response.ok) {
        console.log('Success!');

        var row = document.querySelector(`#myTable tr[entryid="${currentID}"]`);
        row.remove();
      }
      else {
        console.log('Error!');
      }

      // Închide modalul de editare după salvare
      $('#deleteEmployeeModal').modal('hide');
    });
});