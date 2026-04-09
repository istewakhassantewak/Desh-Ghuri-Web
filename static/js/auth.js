document.addEventListener("DOMContentLoaded", () => {
  const roleTabs = document.querySelectorAll("[data-role-tab]");
  const roleInput = document.getElementById("userTypeInput");
  const panes = document.querySelectorAll("[data-role-pane]");

  roleTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const role = tab.getAttribute("data-role-tab");
      if (roleInput) {
        roleInput.value = role;
      }
      roleTabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      panes.forEach((pane) => {
        pane.style.display = pane.getAttribute("data-role-pane") === role ? "block" : "none";
      });
    });
  });
});
