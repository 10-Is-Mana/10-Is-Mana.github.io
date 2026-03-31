var tabs = document.getElementsByClassName('tab');
var hash = window.location.hash.substr(1);

function clickTab(e) {
    for (var j = 0; j < tabs.length; j++) {
        tabs[j].classList.remove('active');
    }
    e.currentTarget.classList.add('active');
}

for (var i = 0; i < tabs.length; i++) {
    tabs[i].addEventListener('click', clickTab);
}

if (hash) {
    for (var k = 0; k < tabs.length; k++) {
        tabs[k].classList.remove('active');
    }
    var matchingTab = document.getElementsByClassName(hash)[0];
    if (matchingTab) {
        matchingTab.classList.add('active');
    }
}

function expandCard(pageID) {
    Array.from(document.getElementsByClassName("card")).forEach(function (element) {
        element.setAttribute("class", "card-hidden");
    });
    var card = document.createElement("div");
    card.setAttribute("class", "expanded-card");
    card.setAttribute("id", "expanded-card");
    Array.from(document.getElementById(pageID).childNodes).forEach(function (element) {
        card.appendChild(element.cloneNode(true));
    });
    card.lastElementChild.firstChild.innerHTML = "Back";
    card.lastElementChild.firstChild.setAttribute("onclick", "(function() { \
        document.getElementById('expanded-card').remove(); \
        Array.from(document.getElementsByClassName('card-hidden')).forEach(element => element.setAttribute('class', 'card')); \
      })()");
    document.getElementById("contents").appendChild(card);
}
