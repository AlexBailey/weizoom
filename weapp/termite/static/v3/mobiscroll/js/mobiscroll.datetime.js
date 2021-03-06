(function ($) {

    $.each(['date', 'time', 'datetime'], function (i, v) {
        $.mobiscroll.presetShort(v);
    });

    // 主题
    var themes = $.mobiscroll.themes.frame,
        theme = {
            display: 'bottom',
            dateOrder: 'MMdyy',
            rows: 5,
            height: 34,
            minWidth: 55,
            headerText: false,
            showLabel: false,
            btnWidth: false,
            selectedLineHeight: true,
            selectedLineBorder: 1,
            useShortLabels: true,
            deleteIcon: 'backspace3',
            checkIcon: 'ion-ios7-checkmark-empty',
            btnCalPrevClass: 'mbsc-ic mbsc-ic-arrow-left5',
            btnCalNextClass: 'mbsc-ic mbsc-ic-arrow-right5',
            btnPlusClass: 'mbsc-ic mbsc-ic-arrow-down5',
            btnMinusClass: 'mbsc-ic mbsc-ic-arrow-up5',
            // @deprecated since 2.14.0, backward compatibility code
            // ---
            onThemeLoad: function (lang, s) {
                if (s.theme) {
                    s.theme = s.theme.replace('ios7', 'ios');
                }
            }
            // ---
        };

    themes.ios = theme;

    // @deprecated since 2.14.0, backward compatibility code
    themes.ios7 = theme;


    // 语言
    $.mobiscroll.i18n.zh = {
        // Core
        setText: '确定',
        cancelText: '取消',
        clearText: '明确',
        selectedText: '{count} 选',
        // Datetime component
        dateFormat: 'yy/mm/dd',
        dateOrder: 'yymmdd',
        dayNames: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
        dayNamesShort: ['日', '一', '二', '三', '四', '五', '六'],
        dayNamesMin: ['日', '一', '二', '三', '四', '五', '六'],
        dayText: '日',
        hourText: '时',
        minuteText: '分',
        monthNames: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        monthNamesShort: ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'],
        monthText: '月',
        secText: '秒',
        timeFormat: 'HH:ii',
        timeWheels: 'HHii',
        yearText: '年',
        nowText: '当前',
        pmText: '下午',
        amText: '上午',
        yearSuffix: '年',
        monthSuffix: '月',
        daySuffix: '日',
        // Calendar component
        dateText: '日',
        timeText: '时间',
        calendarText: '日历',
        closeText: '关闭',
        // Daterange component
        fromText: '开始时间',
        toText: '结束时间',
        // Measurement components
        wholeText: '合计',
        fractionText: '分数',
        unitText: '单位',
        // Time / Timespan component
        labels: ['年', '月', '日', '小时', '分钟', '秒', ''],
        labelsShort: ['年', '月', '日', '点', '分', '秒', ''],
        // Timer component
        startText: '开始',
        stopText: '停止',
        resetText: '重置',
        lapText: '圈',
        hideText: '隐藏',
        // Listview
        backText: '背部',
        undoText: '复原',
        // Form
        offText: '关闭',
        onText: '开启',
        // Numpad
        decimalSeparator: ',',
        thousandsSeparator: ' '
    };

})(jQuery);
