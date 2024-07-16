document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.querySelector('.overlay-sidebar');
    const toggleButton = document.querySelector('.btnSidebarToggle');
    const profileIcon = document.getElementById('profile-icon');
    const profileButtons = document.getElementById('profile-buttons');
    const deleteAccountButton = document.getElementById('delete-account-button');

    // 로컬 스토리지에서 사이드바 상태 불러오기
    const sidebarState = localStorage.getItem('sidebarState');
    if (sidebarState === 'collapsed') {
        sidebar.classList.add('collapsed');
        toggleButton.setAttribute('aria-expanded', 'false');
        toggleButton.innerHTML = '&gt;';
    } else {
        sidebar.classList.remove('collapsed');
        toggleButton.setAttribute('aria-expanded', 'true');
        toggleButton.innerHTML = '&lt;';
    }

    toggleButton.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');
        const expanded = !sidebar.classList.contains('collapsed');
        toggleButton.setAttribute('aria-expanded', expanded);

        // 아이콘 변경
        toggleButton.innerHTML = expanded ? '&lt;' : '&gt;';

        // 사이드바 상태 로컬 스토리지에 저장
        localStorage.setItem('sidebarState', expanded ? 'expanded' : 'collapsed');
    });

    if (profileIcon) {
        profileIcon.addEventListener('click', function () {
            if (profileButtons.style.display === 'none' || profileButtons.style.display === '') {
                profileButtons.style.display = 'block';
            } else {
                profileButtons.style.display = 'none';
            }
        });
    }

    if (deleteAccountButton) {
        deleteAccountButton.addEventListener('click', function () {
            const confirmation = confirm('정말 탈퇴하시겠습니까?');
            if (confirmation) {
                window.location.href = deleteAccountButton.getAttribute('data-url');
            }
        });
    }
});