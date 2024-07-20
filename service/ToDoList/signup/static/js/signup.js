document.addEventListener('DOMContentLoaded', function() {
    var errorFields = document.querySelectorAll('.error-tooltip');

    function hideTooltips() {
        errorFields.forEach(function(field) {
            field.style.visibility = 'hidden';
            field.style.opacity = '0';
        });
    }

    function showFirstTooltip() {
        for (var i = 0; i < errorFields.length; i++) {
            var field = errorFields[i];
            var errorText = field.querySelector('.error-text');
            if (errorText && errorText.textContent.trim() !== "") {
                field.style.display = 'flex';
                field.style.visibility = 'visible';
                field.style.opacity = '1';
                var icon = field.querySelector('.icon');
                if (icon) {
                    icon.style.display = 'inline';
                }
                break; // 첫 번째 오류 툴팁만 표시하고 루프 종료
            }
        }
    }

    showFirstTooltip(); // 페이지 로드 시 첫 번째 오류 툴팁 표시

    document.addEventListener('click', function(event) {
        if (!event.target.closest('.signup-group')) {
            hideTooltips();
        }
    });
});