$(document).ready(function() {
  var csrfToken = $('meta[name="csrf-token"]').attr('content') || '';

  function applyButtonState($btn, active) {
    var isLike = String($btn.data('is-like')) === "true";

    // управляем маркерами состояния
    $btn.toggleClass('liked-like', active && isLike);
    $btn.toggleClass('liked-dislike', active && !isLike);

    // управляем bootstrap-классами
    if (active) {
      $btn.removeClass('btn-outline-secondary')
          .addClass(isLike ? 'btn-primary text-white' : 'btn-danger text-white');
    } else {
      $btn.removeClass('btn-primary btn-danger text-white')
          .addClass('btn-outline-secondary');
    }
  }

  /**
   * Универсальная логика выбора метода:
   * - Если не было активной оценки -> POST
   * - Если кликаем ту же активную -> DELETE (снять)
   * - Если кликаем другую при активной -> PUT (сменить)
   */
  function resolveMethod($likeBtn, $dislikeBtn, $clickedBtn) {
    var clickedIsLike = String($clickedBtn.data('is-like')) === "true";

    var hasActive = $likeBtn.hasClass('liked-like') || $dislikeBtn.hasClass('liked-dislike');
    var wasActive = $clickedBtn.hasClass(clickedIsLike ? 'liked-like' : 'liked-dislike');

    if (!hasActive) return "POST";
    if (wasActive) return "DELETE";
    return "PUT";
  }

  // ========== ВОПРОС ==========
  $(document).on('click', '.grade-btn', function(e) {
    e.preventDefault();

    var $btn = $(this);
    var questionId = $btn.data('question-id');
    var isLike = String($btn.data('is-like')) === "true";

    // находим карточку вопроса надежно
    var $card = $btn.closest('[data-card-question-id]');
    var $likeBtn = $card.find('.grade-btn[data-is-like="true"]');
    var $dislikeBtn = $card.find('.grade-btn[data-is-like="false"]');

    var method = resolveMethod($likeBtn, $dislikeBtn, $btn);

    // оптимистично применяем состояние
    if (method === "DELETE") {
      applyButtonState($btn, false);
    } else {
      applyButtonState($likeBtn, isLike);
      applyButtonState($dislikeBtn, !isLike);
    }

    $.ajax({
      url: '/grade/like',
      method: method,
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify({ is_like: isLike, question_id: questionId }),
      headers: {
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest'
      },
      success: function(data) {
        $card.find('.like-count').text(data.like_count);
        $card.find('.dislike-count').text(data.dislike_count);
      },
      error: function() {
        // при ошибке — лучше просто перезагрузить реальные значения с сервера,
        // но если пока нет отдельного GET — откатим на "предыдущее"
        // (минимальный корректный откат — снять всё и дать пользователю повторить)
        applyButtonState($likeBtn, $likeBtn.hasClass('liked-like'));
        applyButtonState($dislikeBtn, $dislikeBtn.hasClass('liked-dislike'));
      }
    });
  });

  // ========== ОТВЕТЫ ==========
  $(document).on('click', '.grade-answer-btn', function(e) {
    e.preventDefault();

    var $btn = $(this);
    var answerId = $btn.data('answer-id');
    var isLike = String($btn.data('is-like')) === "true";

    // контейнер конкретного ответа
    var $answerCard = $btn.closest('article.card');
    var $likeBtn = $answerCard.find('.grade-answer-btn[data-is-like="true"]');
    var $dislikeBtn = $answerCard.find('.grade-answer-btn[data-is-like="false"]');

    var method = resolveMethod($likeBtn, $dislikeBtn, $btn);

    if (method === "DELETE") {
      applyButtonState($btn, false);
    } else {
      applyButtonState($likeBtn, isLike);
      applyButtonState($dislikeBtn, !isLike);
    }

    $.ajax({
      // ВАЖНО: если у вас другой endpoint для ответов — поменяйте здесь.
      // Например: '/grade/answer/'
      url: '/grade/answer',
      method: method,
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify({ is_like: isLike, answer_id: answerId }),
      headers: {
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest'
      },
      success: function(data) {
        $answerCard.find('.answer-like-count').text(data.like_count);
        $answerCard.find('.answer-dislike-count').text(data.dislike_count);
      },
      error: function() {
        applyButtonState($likeBtn, $likeBtn.hasClass('liked-like'));
        applyButtonState($dislikeBtn, $dislikeBtn.hasClass('liked-dislike'));
      }
    });
  });

});