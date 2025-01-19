document.addEventListener("DOMContentLoaded", () => {
    // Select the button and the flyout menu
    const productButton = document.getElementById("product-button");
    const productButton2 = document.getElementById("product-button2");
    const productButton3 = document.getElementById("product-button3");
    const productButton4 = document.getElementById("product-button4");
    const flyoutMenu = document.getElementById("flyout-menu");
    const flyoutMenu2 = document.getElementById("flyout-menu2");
    const flyoutMenu3 = document.getElementById("flyout-menu3");
    // Toggle flyout menu visibility
    productButton.addEventListener("click", () => {
      const isHidden = flyoutMenu.classList.contains("hidden");
      if (isHidden) {
        flyoutMenu.classList.remove("hidden"); // Show the menu
      } else {
        flyoutMenu.classList.add("hidden"); // Hide the menu
      }
    });
    productButton2.addEventListener("click",() => {
        flyoutMenu2.classList.remove("hidden");
    });
    productButton3.addEventListener("click",() => {
        flyoutMenu2.classList.add("hidden");
    });
    productButton4.addEventListener("click", () => {
        const isHidden = flyoutMenu3.classList.contains("hidden");
        if (isHidden) {
          flyoutMenu3.classList.remove("hidden"); // Show the menu
        } else {
          flyoutMenu3.classList.add("hidden"); // Hide the menu
        }
      });
  
    // Optional: Close the flyout menu when clicking outside
    document.addEventListener("click", (event) => {
      if (!productButton.contains(event.target) && !flyoutMenu.contains(event.target)) {
        flyoutMenu.classList.add("hidden");
      }
    });
  });


  