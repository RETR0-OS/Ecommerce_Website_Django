const sections = document.querySelectorAll("section");
const navLi = document.querySelectorAll("nav .container-fluid .collapse .navbar-nav .nav-item a");
window.onload = (event) => {
  let current = "";

  sections.forEach((section) => {
    const sectionTop = section.offsetTop;
    if (pageYOffset >= (sectionTop - 400)) {
      current = section.getAttribute('id');
      console.log(current)
    }
  })
  navLi.forEach((a) => {
    a.classList.remove("active");
    if (a.classList.contains(current)){
      a.classList.add("active");
      console.log(current)
    }
    else
    {
      a.classList.remove("active");
    }
  })
};
window.addEventListener('scroll', () => {
  let current = "";

  sections.forEach((section) => {
    const sectionTop = section.offsetTop;
    if (pageYOffset >= (sectionTop - 250)) {
      current = section.getAttribute('id');
      console.log(current)
    }
  })
  navLi.forEach((a) => {
    a.classList.remove("active");
    if (a.classList.contains(current)){
      a.classList.add("active");
    }
    else
    {
      a.classList.remove("active");
    }
  })
})
