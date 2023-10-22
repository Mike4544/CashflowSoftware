const body = document.querySelector("body");

//  Gradient coordonates
const gradients = [
  {
    x: -250,
    y: -250,
    primary: "rgba(156, 236, 251, 1)",
    secondary: "rgba(54, 209, 220, 0.37)",
    ternary: "rgba(238, 130, 238, 0)",
    speed: 20
  },
  {
    x: -150,
    y: -100,
    primary: "rgba(161, 255, 206, 1)",
    secondary: "rgba(250, 255, 209, 0.37)",
    ternary: "rgba(238, 130, 238, 0)",
    speed: 15
  },
  {
    x: -205,
    y: -200,
    primary: "rgba(255, 252, 0, 1)",
    secondary: "rgba(255, 255, 255, 0.37)",
    ternary: "rgba(238, 130, 238, 0)",
    speed: 10
  },
];

//  Create the gradient elementCreate the gradients
for (let gradient of gradients) {
  //  Create the gradient
  const gradientElement = document.createElement("div");
  gradientElement.classList =
    "hidden md:block absolute w-[75%] max-w-[1000px] h-[75%] max-h-[1000px] inset-0 z-[-1] top-0 left-0";
  gradientElement.style.opacity = 0.5;
  gradientElement.style.background = `radial-gradient(
    circle at 50% 50%,
    ${gradient.primary} 0%, 
    ${gradient.secondary} 16%,
    ${gradient.ternary} 36%,
    rgba(238, 130, 238, 0) 80%
)`;

  body.appendChild(gradientElement);

  //  Create the first interval
  setInterval(() => {
    //  Update the gradient
    gradient.x += Math.random() * gradient.speed - 7.5;
    gradient.y += Math.random() * gradient.speed - 7.5;

    if (gradient.x > window.innerWidth || gradient.x < -250) gradient.x = -250;
    if (gradient.y > window.innerHeight || gradient.y < -250) gradient.y = -250;

    gradientElement.style.left = `${gradient.x}px`;
    gradientElement.style.top = `${gradient.y}px`;
  }, 100);
}

//  Create the second interval
// setInterval(() => {
//     //  Get the current opacity and select a random number
//     let currentOpacity = gradientElement.style.opacity;
//     let randomOpacity = Math.random() * 1;

//     //  Create the keyframe string
//     let keyframes = `@keyframes opacity {
//         from { opacity: ${currentOpacity}; }
//         to { opacity: ${randomOpacity}; }
//     }`;

//     //  Create the style element
//     let style = document.createElement('style');
//     style.innerHTML = keyframes;

//     //  Append the style element
//     document.head.appendChild(style);

//     //  Animate the opacity
//     gradientElement.style.animation = 'opacity 0.5s ease-in-out';

// }, 1000);
