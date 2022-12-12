let elements = {};
window.onload = main;

function ft_atoi(string)
{
    let num = '0';

    for (let i = 0; i < string.length; ++i)
    {
        if (string[i] == '0' && num.length == 1 && num == '0')
            continue;
        if (string[i] >= '0' && string[i] <= '9')
        {
            if (num.length == 1 && num == '0')
                num = string[i]
            else
                num += string[i];
        }
        else
            break;
    }
    return num;
}

function init_current()
{
}

function open_mob_menu() {
    elements['mobile-body-overly'].setAttribute('style', 'display: block;');

}

function close_mob_menu() {
    elements['mobile-body-overly'].setAttribute('style', 'display: none;');

}

function main()
{
    let b = document.getElementById('mobile-nav-toggle');

    elements['mobile-nav'] = document.getElementById('mobile-nav')
    elements['mobile-body-overly'] = document.getElementById('mobile-body-overly')
    b.addEventListener('click', open_mob_menu)
    elements['mobile-body-overly'].addEventListener('click', close_mob_menu)
    init_current();
}