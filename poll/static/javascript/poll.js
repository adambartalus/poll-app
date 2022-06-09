answer_ul = document.querySelector('#answer_options');

answer_ul.addEventListener('input', function(e) {
    last_li = answer_ul.lastElementChild;
    last_input = last_li.querySelector('input');
    if(e.target == last_input) {
        new_li = document.createElement('li');
        new_input = document.createElement('input');
        new_input.type = "text";
        new_input.name = "answer";
        new_li.appendChild(new_input);
        answer_ul.appendChild(new_li);
    }
})