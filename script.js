var tabs = document.getElementsByClassName('tab');
var hash = window.location.hash.substr(1);

function clickTab(e){
    for (j = 0; j < tabs.length; j++){
        tabs[j].classList.remove('active')
    }
    e.currentTarget.classList.add('active');
}

for (i = 0; i < tabs.length; i++){
    tabs[i].addEventListener('click', clickTab)
}

if(hash){
    document.getElementsByClassName(hash)[0].classList.add('active');
}