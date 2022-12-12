$(function () {
    let ips = document.getElementsByTagName('input');

    for (let i = 0; i < ips.length; i++) {
        let elem = ips[i];
        if (elem.getAttribute('type') == 'checkbox') {
            $.ajax({
                    url: "/admin/",
                    type: "POST",
                    data: {
                        title: elem.id,
                    },
                    dataType: 'json',
                    success: function (result) {
                        if (result['ok']) {
                            elem.value = result['value'] == 'true' ? 'on' : 'off'
                            elem.checked = result['value'] == 'true'
                        }
                        else
                            elem.value = 'off'
                        console.log(result);
                    }
                })
            elem.addEventListener('input', function () {
                console.log(elem.value);
                $.ajax({
                    url: "/admin/",
                    type: "POST",
                    data: {
                        title: elem.id,
                        value: elem.value == 'on'
                    },
                    dataType: 'json',
                    success: function (result) {
                        if (result['ok'])
                            elem.value = result['value'] == 'true' ? 'on' : 'off'
                        else
                            elem.value = elem.value == 'on' ? 'off' : 'on'
                        console.log(result);
                    }
                })

            });
        }
    }
})