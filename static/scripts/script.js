const sideNavbar = document.querySelector('.nav-sidebar')
const navClose = document.querySelector('.mb-nav-toggle')
const navOpen = document.querySelector('.user-profile')

var inpField = document.getElementById('point-value')
const btnInc = document.getElementById('point-increment')
const btnDec = document.getElementById('point-decrement')




var check = false;

navOpen.addEventListener('click',() => {
    sideNavbar.style.transform = 'translateX(0%)';
    console.log(btnInc) 
    
    
})

navClose.addEventListener('click', function(){
    sideNavbar.style.transform = 'translateX(100%)';
    var check = false;
   
})

btnInc.addEventListener('click',() => {
    if(parseInt(inpField.value) < inpField.max)
    {
        inpField.value = 5+ parseInt(inpField.value)
        inpField.setAttribute('value',inpField.value)
    }


    
})

btnDec.addEventListener('click',() => {
    if(inpField.value >=5)
    {
        inpField.value = parseInt(inpField.value)-5
        inpField.setAttribute('value',inpField.value)
    }


    
})





