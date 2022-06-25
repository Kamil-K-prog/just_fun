let left = document.querySelector('.left');
let content = document.querySelector('.content');
let protos = document.querySelectorAll('.proto');

left.addEventListener('mousemove', (event) => {
    let move = (event.clientX * 0.05) + 4;
    let move2 = (event.clientX * 0.003);
    content.style.transform = `translateX(-${move2}%)`;

    protos.forEach((proto) => {
        proto.style.transform = `translateX(${move}%)`;
    })
});

let btn_registration = document.querySelector('.registration');
btn_registration.onclick = function () {
    let login_form = document.querySelector('.login_form');
    login_form.innerHTML = '<form action="" method="POST">\n' +
        '                    <input type="email" name="email" id="email" placeholder="ваш email">\n' +
        '                    <input type="password" name="pass" id="pass" placeholder="ваш пароль">\n' +
        '                    <input type="password" name="pass2" id="pass2" placeholder="повторите пароль">\n' +
        '                    <button class="create_user">Зарегистрироваться</button>\n' +
        '                </form>';
};

let btn_sign_in = document.querySelector('.sign_in');
btn_sign_in.onclick = function () {
    let login_form = document.querySelector('.login_form');
    login_form.innerHTML = '                <form action="" method="POST">\n' +
        '                    <input type="email" name="email" id="email" placeholder="ваш email">\n' +
        '                    <input type="password" name="pass" id="pass" placeholder="ваш пароль">\n' +
        '                    <button class="signin">Войти</button>\n' +
        '                </form>';
};