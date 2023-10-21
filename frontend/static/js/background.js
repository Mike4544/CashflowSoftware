const body = document.querySelector('body');

//  Gradient coordonates
const gradient = {
    x: -250,
    y: -250,
    primary: 'rgba(156, 236, 251, 1)',
    secondary: 'rgba(54, 209, 220, 0.37)',
    ternary: 'rgba(238, 130, 238, 0)'
};

//  Create the gradient
const gradientElement = document.createElement('div');
gradientElement.classList = "hidden md:block absolute w-[75%] max-w-[1000px] h-[75%] max-h-[1000px] inset-0 z-[-1] top-0 left-0";
gradientElement.style.opacity = 0.5;
gradientElement.style.background = `radial-gradient(
    circle at 50% 50%,
    ${gradient.primary} 0%, 
    ${gradient.secondary} 16%,
    ${gradient.ternary} 36%,
    rgba(238, 130, 238, 0) 80%
)`;

body.appendChild(gradientElement);

//  Create the interval
setInterval(() => {
    //  Update the gradient
    gradient.x += Math.random() * 7 - 1;
    gradient.y += Math.random() * 7 - 1;

    if(gradient.x > window.innerWidth) gradient.x = -250;
    if(gradient.y > window.innerHeight) gradient.y = -250;

    gradientElement.style.left = `${gradient.x}px`;
    gradientElement.style.top = `${gradient.y}px`;

}, 500);