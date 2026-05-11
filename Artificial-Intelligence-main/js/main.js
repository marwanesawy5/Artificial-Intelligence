/* ==========================================
   js/main.js
   Global Interactions / FinAI Advisor
========================================== */

document.addEventListener("DOMContentLoaded", () => {

  /* ========================
     Mobile Navbar Toggle
  ======================== */
  const menuToggle = document.getElementById("menuToggle");
  const navMenu = document.getElementById("navMenu");

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", () => {
      navMenu.classList.toggle("show");
    });

    // Close menu when clicking links
    navMenu.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        navMenu.classList.remove("show");
      });
    });
  }

  /* ========================
     Dashboard Sidebar Toggle
  ======================== */
  const sidebar = document.getElementById("sidebar");
  const openSidebar = document.getElementById("openSidebar");
  const closeSidebar = document.getElementById("closeSidebar");

  if (sidebar && openSidebar) {
    openSidebar.addEventListener("click", () => {
      sidebar.classList.add("show");
    });
  }

  if (sidebar && closeSidebar) {
    closeSidebar.addEventListener("click", () => {
      sidebar.classList.remove("show");
    });
  }

  /* ========================
     Scroll Reveal Animation
  ======================== */
  const reveals = document.querySelectorAll(".fade-up");

  const revealOnScroll = () => {
    const trigger = window.innerHeight - 100;

    reveals.forEach(item => {
      const top = item.getBoundingClientRect().top;

      if (top < trigger) {
        item.classList.add("show");
      }
    });
  };

  revealOnScroll();
  window.addEventListener("scroll", revealOnScroll);

  /* ========================
     Animated Counters
  ======================== */
  const counters = document.querySelectorAll(".counter");

  counters.forEach(counter => {
    const target = +counter.getAttribute("data-target");
    let current = 0;

    const updateCounter = () => {
      const increment = Math.ceil(target / 60);

      current += increment;

      if (current >= target) {
        counter.textContent = target;
      } else {
        counter.textContent = current;
        requestAnimationFrame(updateCounter);
      }
    };

    updateCounter();
  });

  /* ========================
     Button Loading States
  ======================== */
  const buttons = document.querySelectorAll(".btn");

  buttons.forEach(button => {
    button.addEventListener("click", function () {

      if (
        this.type === "submit" ||
        this.classList.contains("loading-btn")
      ) {
        const originalText = this.innerHTML;

        this.innerHTML = "Loading...";
        this.disabled = true;

        setTimeout(() => {
          this.innerHTML = originalText;
          this.disabled = false;
        }, 1200);
      }

    });
  });

  /* ========================
     Smooth Hover Tilt Cards
  ======================== */
  const cards = document.querySelectorAll(".card");

  cards.forEach(card => {

    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();

      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const rotateX = ((y / rect.height) - 0.5) * -6;
      const rotateY = ((x / rect.width) - 0.5) * 6;

      card.style.transform =
        `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });

    card.addEventListener("mouseleave", () => {
      card.style.transform =
        "perspective(800px) rotateX(0deg) rotateY(0deg)";
    });

  });

  /* ========================
     Current Year Auto Footer
  ======================== */
  const yearText = document.querySelector(".copyright");

  if (yearText) {
    yearText.innerHTML =
      `© ${new Date().getFullYear()} FinAI Advisor. All rights reserved.`;
  }

});