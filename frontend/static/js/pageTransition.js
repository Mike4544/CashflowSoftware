//  Make a transition between pages

let links = document.querySelectorAll('a');

links.forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();

        let app = document.body;
        app.classList.add('fade-out');

        //  Delay the new page
        setTimeout(() => {

            let href = link.getAttribute('href');

            //  Change the page
            window.location.href = href;

        }, 100);
    });
});