document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;
  const themeToggle = document.getElementById("themeToggle");
  const savedTheme = localStorage.getItem("deshGhuriTheme");
  const initialTheme = savedTheme || "dark";
  body.setAttribute("data-theme", initialTheme);
  if (themeToggle) {
    themeToggle.innerHTML = initialTheme === "dark" ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    themeToggle.addEventListener("click", () => {
      const nextTheme = body.getAttribute("data-theme") === "dark" ? "light" : "dark";
      body.setAttribute("data-theme", nextTheme);
      localStorage.setItem("deshGhuriTheme", nextTheme);
      themeToggle.innerHTML = nextTheme === "dark" ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    });
  }

  const navbar = document.querySelector(".navbar");
  const navbarCollapseEl = document.getElementById("navbarNav");
  const navLinks = document.querySelectorAll("[data-nav-link]");
  const navbarCollapse =
    navbarCollapseEl && window.bootstrap
      ? new bootstrap.Collapse(navbarCollapseEl, { toggle: false })
      : null;

  function updateNavbarScrolled() {
    if (!navbar) return;
    if (window.scrollY > 20) {
      navbar.classList.add("nav-scrolled");
    } else {
      navbar.classList.remove("nav-scrolled");
    }
  }

  function setActiveNav() {
    const currentPath = window.location.pathname;
    const currentHash = window.location.hash;
    let activeSet = false;
    navLinks.forEach((link) => {
      link.classList.remove("active");
      const href = link.getAttribute("href") || "";
      const isPackagesHash = href.includes("#tour-packages") && currentHash === "#tour-packages";
      const isExactPath = href === currentPath && currentHash !== "#tour-packages";
      if (!activeSet && (isPackagesHash || isExactPath)) {
        link.classList.add("active");
        activeSet = true;
      }
    });
  }

  updateNavbarScrolled();
  setActiveNav();
  window.addEventListener("scroll", updateNavbarScrolled);

  const revealItems = document.querySelectorAll(".card, .feature-card, .package-card");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  revealItems.forEach((item) => {
    item.style.opacity = "0";
    item.style.transform = "translateY(18px)";
    item.style.transition = "opacity .5s ease, transform .5s ease";
    observer.observe(item);
  });

  const smoothLinks = document.querySelectorAll('a[href^="#"]');
  smoothLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      const targetId = link.getAttribute("href");
      if (!targetId || targetId === "#") return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      if (window.innerWidth < 992 && navbarCollapseEl?.classList.contains("show")) {
        navbarCollapse?.hide();
      }
    });
  });
});
