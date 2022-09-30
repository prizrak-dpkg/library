document.addEventListener("DOMContentLoaded", () => {
  const modal = document.querySelector("#modal");
  const modalTitle = document.querySelector("#modalTitle");
  const modalBody = document.querySelector("#modalBody");
  const createUser = document.querySelector("#createUser");
  createUser.addEventListener("click", () => {
    modalTitle.innerText = "Registrar usuario";
    const form = createUserForm("Registrar usuario", false);
    modalBody.insertAdjacentElement("beforeend", form);
    modal.classList.add("modal--is-open");
  });
  Array.from(document.getElementsByClassName("edit__button")).forEach(
    (item) => {
      item.addEventListener("click", (event) => {
        const userId = event.currentTarget.dataset.id;
        const data = new FormData();
        data.append("get_user", JSON.stringify({ id: userId }));
        sendData("/library/user/", "POST", data, (response) => {
          if (response.response) {
            modalTitle.innerText = "Editar usuario";
            const form = createUserForm("Editar usuario", true, response.data);
            modalBody.insertAdjacentElement("beforeend", form);
            modal.classList.add("modal--is-open");
          }
        });
      });
    }
  );
});
