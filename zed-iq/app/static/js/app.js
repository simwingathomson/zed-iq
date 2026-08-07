const savedTheme=localStorage.getItem("theme")||"light";document.documentElement.setAttribute("data-bs-theme",savedTheme);document.getElementById("themeToggle")?.addEventListener("click",()=>{const next=document.documentElement.getAttribute("data-bs-theme")==="dark"?"light":"dark";document.documentElement.setAttribute("data-bs-theme",next);localStorage.setItem("theme",next)});

