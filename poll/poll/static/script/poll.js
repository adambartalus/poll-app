answer_ul = document.querySelector('#answer_options');

answer_ul.addEventListener('input', function(e) {
    answer_count = answer_ul.getElementsByTagName('li').length
    last_li = answer_ul.lastElementChild;
    last_input = last_li.querySelector('input');
    if(e.target == last_input) {
        new_li = document.createElement('li');
        new_input = document.createElement('input');
        new_label = document.createElement('label');
        s = `answer_options-${answer_count}`;
        new_input.id = s;
        new_input.name = s;
        new_input.type = "text";
        new_label.htmlFor = s;
        new_li.appendChild(new_label);
        new_li.appendChild(new_input);
        answer_ul.appendChild(new_li);
    }
})