$(document).ready(function() {
  var csrfToken = $('meta[name="csrf-token"]').attr('content') || '';

  function setAnswerCorrectUI($answerCard, isCorrect) {
    $answerCard.toggleClass('answer-correct', !!isCorrect);

    // бейдж "Решение" — если хотите динамически добавлять/убирать
    var $header = $answerCard.find('header.d-flex').first();
    var $badge = $header.find('.answer-correct-badge');

    if (isCorrect) {
      if ($badge.length === 0) {
        $header.append(
          '<span class="badge text-bg-primary answer-correct-badge"><i class="bi bi-check2-square me-1"></i>Решение</span>'
        );
      }
    } else {
      $badge.remove();
    }
  }

  $(document).on('change', '.answer-correct-toggle', function(e) {
    var $checkbox = $(this);
    var answerId = $checkbox.data('answer-id');
    var isCorrect = $checkbox.is(':checked');

    var $answerCard = $checkbox.closest('article.card');
    var prevState = !isCorrect; // до клика было наоборот

    // оптимистично обновим UI:
    // если ставим true — снимаем у всех остальных (обычно верный ответ один)
    if (isCorrect) {
      var $allAnswerCards = $answerCard.closest('section').find('article.card.shadow-sm.mb-3');
      $allAnswerCards.each(function() {
        var $card = $(this);
        $card.find('.answer-correct-toggle').prop('checked', false);
        setAnswerCorrectUI($card, false);
      });
      $checkbox.prop('checked', true);
      setAnswerCorrectUI($answerCard, true);
    } else {
      setAnswerCorrectUI($answerCard, false);
    }

    $.ajax({
      url: '/grade/answer/correct',
      method: 'PATCH', // если у вас POST — поменяйте на 'POST'
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify({ answer_id: Number(answerId), is_correct: isCorrect }),
      headers: {
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest'
      },
      success: function(data) {
        // Если сервер возвращает актуальное состояние и/или correct_answer_id — можно синхронизировать.
        // Минимально: ничего не делаем, UI уже обновлен.
        // Например, если сервер вернул {correct_answer_id: 123}:
        if (data && data.correct_answer_id) {
          var correctId = data.correct_answer_id;
          var $section = $answerCard.closest('section');
          $section.find('.answer-correct-toggle').each(function() {
            var $cb = $(this);
            var id = Number($cb.data('answer-id'));
            var $card = $cb.closest('article.card');
            var ok = (id === correctId);
            $cb.prop('checked', ok);
            setAnswerCorrectUI($card, ok);
          });
        }
      },
      error: function() {
        // откат при ошибке
        $checkbox.prop('checked', prevState);
        setAnswerCorrectUI($answerCard, prevState);
      }
    });
  });
});