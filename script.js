const tabButtons = document.querySelectorAll(".tab-button");
const authForms = document.querySelectorAll(".auth-form");

const updateStudentFields = (form) => {
  const roleSelect = form.querySelector("select[name$='role']");
  const classField = form.querySelector(".conditional-field");
  const nameInput = form.querySelector("input[name$='name']");
  const nameLabel = nameInput?.closest(".field")?.querySelector(".field-label");

  if (!roleSelect || !classField) {
    return;
  }

  const shouldShow = roleSelect.value === "student";
  classField.classList.toggle("is-hidden", !shouldShow);

  if (nameInput && nameLabel) {
    if (roleSelect.value === "admin") {
      nameLabel.textContent = "Admin Username";
      nameInput.placeholder = "Enter admin username";
    } else {
      nameLabel.textContent = "Name";
      nameInput.placeholder = "Enter your name";
    }
  }
};

tabButtons.forEach((button) => {
  button.addEventListener("click", () => {
    tabButtons.forEach((item) => item.classList.remove("is-active"));
    authForms.forEach((form) => form.classList.remove("is-active"));

    button.classList.add("is-active");
    document.getElementById(button.dataset.target)?.classList.add("is-active");
  });
});

authForms.forEach((form) => {
  const roleSelect = form.querySelector("select[name$='role']");
  updateStudentFields(form);

  if (roleSelect) {
    roleSelect.addEventListener("change", () => updateStudentFields(form));
  }
});
