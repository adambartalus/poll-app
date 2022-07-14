user_btn = document.querySelector('#user-btn')
if(user_btn) {
    user_btn.addEventListener('click', myFunction)
}
function myFunction(e) {
    user_dropdown = document.querySelector("#user-dropdown");
    user_dropdown.classList.add('show')
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  target = event.target.closest('.dropdown')
  if (!target) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}