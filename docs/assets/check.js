// 자가체크: 체크 개수에 따라 안내 문구를 바꿉니다.
// <div class="check" data-low="0~1개 안내" data-mid="2~3개 안내" data-high="4개 이상 안내"> 안에 체크박스를 둡니다.
document.querySelectorAll('.check').forEach(function (box) {
  var out = box.querySelector('.check-result');
  if (!out) return;
  function update() {
    var n = box.querySelectorAll('input:checked').length;
    var key = n <= 1 ? 'low' : n <= 3 ? 'mid' : 'high';
    out.innerHTML = '<strong>' + n + '개 체크</strong> · ' + box.dataset[key];
  }
  box.addEventListener('change', update);
  update();
});
