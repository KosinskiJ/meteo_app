$.datetimepicker.setLocale('pl');
jQuery("input[id*='begin_date'], input[id*='finish_date']").datetimepicker({
    format: 'Y-m-d H:i',
    step:
        10,
});


