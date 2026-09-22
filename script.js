const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();

const cursor = document.querySelector(".cursor");
if (cursor && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
  window.addEventListener("pointermove", (event) => {
    cursor.style.left = `${event.clientX}px`;
    cursor.style.top = `${event.clientY}px`;
  });

  document.querySelectorAll("a, button, .project").forEach((el) => {
    el.addEventListener("pointerenter", () => cursor.classList.add("grow"));
    el.addEventListener("pointerleave", () => cursor.classList.remove("grow"));
  });
}

// Make project cards clickable
document.querySelectorAll(".project").forEach((project) => {
  project.style.cursor = "pointer";
  project.addEventListener("click", (e) => {
    // Don't navigate if clicking on a link within the project
    if (e.target.closest("a")) return;
    
    const projectTitle = project.querySelector("h3")?.textContent;
    if (!projectTitle) return;
    
    // Map project titles to project IDs
    const projectMap = {
      "Cardiac Function Assessment": "cardiac",
      "Cloud Computing — Docker & Kubernetes": "cloud",
      "Hotel Rating Prediction": "hotel",
      "Multi-Cancer Classification": "cancer",
      "Classical Encryption Package": "encryption",
      "Social App": "social",
      "Shop App": "shop",
      "Bookly": "bookly",
      "News App": "news",
      "BuyingApp — E-commerce (MEAN)": "buying",
    };
    
    const projectId = projectMap[projectTitle];
    if (projectId) {
      window.location.href = `demo.html?id=${projectId}`;
    }
  });
});
