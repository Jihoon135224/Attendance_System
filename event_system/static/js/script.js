// 부스 상태 업데이트 함수
function updateBoothStatus() {
    fetch('/booth_status')
        .then(response => response.json())
        .then(data => {
            const boothElements = document.querySelectorAll('.booth');
            boothElements.forEach(booth => {
                const boothName = booth.dataset.boothName;
                if (data[boothName] === '참여') {
                    booth.classList.add('participated');
                    booth.classList.remove('not-participated');
                } else {
                    booth.classList.add('not-participated');
                    booth.classList.remove('participated');
                }
            });
        });
}

// 페이지 로드 시 부스 상태 업데이트
window.onload = function() {
    updateBoothStatus();
};