$(document).ready(function() {
  var csrfToken = $('meta[name="csrf-token"]').attr('content') || '';

  $(document).on('change', '.answer-correct-toggle', function(e) {
    var $checkbox = $(this);
    var answerId = $checkbox.data('answer-id');
    var isCorrect = $checkbox.is(':checked');
    var $question = $('.grade-btn');
    var questionId = $question.data('question-id')

    $.ajax({
      url: '/grade/answer/correct',
      method: 'PATCH',
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify({ answer_id: Number(answerId), is_correct: isCorrect, question_id: questionId }),
      headers: {
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest'
      },
      error: function (xhr){
        if (xhr.status === 401 || xhr.status === 403) {
          const next = encodeURIComponent(window.location.pathname + window.location.search);
          window.location.href = `/login?next=${next}`;
          return;
        }
      }
    });
  });
});