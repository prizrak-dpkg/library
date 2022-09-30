document.addEventListener("DOMContentLoaded", () => {
  Array.from(document.getElementsByClassName("menu__link")).forEach((item) => {
    item.addEventListener("click", (event) => {
      window.location.replace(event.currentTarget.dataset.href);
    });
  });
  Array.from(document.getElementsByClassName("modal__close")).forEach(
    (item) => {
      item.addEventListener("click", () => {
        const modal = document.querySelector("#modal");
        const modalBody = document.querySelector("#modalBody");
        const modalFooter = document.querySelector("#modalFooter");
        modal.classList.remove("modal--is-open");
        modalBody.innerHTML = "";
        modalFooter.innerHTML = "";
      });
    }
  );
});
