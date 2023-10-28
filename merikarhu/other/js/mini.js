let siirraAlas = true;
$(document).ready(function () {
    $("#toggleLapset").click(function () {
        // ryhmien kavennus
        $("th:nth-child(2), td:nth-child(2)").toggle();
        const sections = document.getElementsByClassName('toggle-section');
        $("th:nth-child(6), td:nth-child(6)").toggle();

        // ryhmät rivissä
        let divs = document.querySelectorAll('div.minitoggle');
        for (let i = 0; i < divs.length; i++) {
            divs[i].classList.toggle('ryhma');
        }
        //yläpalkki mini-moodissa
        var navbarToggler = document.getElementById("navbarToggler");
        var collapseButton = document.getElementById("collapseButton");

        if (navbarToggler.style.display === "none") {
            collapseButton.style.setProperty("opacity", "1", "");
            navbarToggler.style.setProperty("display", "", "");
        } else {
            collapseButton.style.setProperty("opacity", "0", "");
            navbarToggler.style.setProperty("display", "none", "important");
        }
        console.log("jee")
        // Kuvaajien siirto alas/ylös
        for (let paiva = 0; paiva <= 6; paiva++) {
            for (let i = 0; i <= 50; i++) {
                let ala = document.getElementById(`${paiva}${i}_kuvaajaAla`);
                let yla = document.getElementById(`${paiva}${i}_kuvaajaYla`); 
                
                if (siirraAlas) {
                    while (yla && yla.firstChild) {
                        ala.appendChild(yla.firstChild);
                    }
                } else {
                    while (ala && ala.firstChild) {
                        if (yla) {
                            yla.appendChild(ala.firstChild);
                        } else {
                            console.error('Yläelementtiä ei löydy. Elementin ID: ', `${paiva}${i}_kuvaajaYla`);
                            break;
                        }
                    }
                }
                
            }
        }
        
        siirraAlas = !siirraAlas;
    }); 
});