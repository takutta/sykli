document.onreadystatechange = function() {
    if (document.readyState === "complete") {
      setTimeout(function() {
        document.querySelector("#loader").style.display = "none";
        document.querySelector("#kaikki").classList.add("visible");
        document.querySelector("#kaikki").classList.remove("hidden");          
      }, 500);
    }
  };