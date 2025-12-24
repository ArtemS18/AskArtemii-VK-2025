(async function () {
  if (!window.Centrifuge) return;

  async function getToken() {
    const r = await fetch(window.CENTRIFUGO_TOKEN_URL, { credentials: "same-origin" });
    if (!r.ok) throw new Error("Failed to get Centrifugo token");
    const j = await r.json();
    return j.token;
  }

  const token = await getToken();
  console.log("Centrifugo token obtained token:", token);

  const centrifuge = new Centrifuge(window.CENTRIFUGO_WS_URL, { token });
  centrifuge.on("error", function (ctx) {
    console.error("Centrifuge error:", ctx);
  });
  centrifuge.on("connecting", function (ctx) {
    console.log("Centrifuge connected:", ctx);
  });
  centrifuge.on("disconnected", function (ctx) {
    console.warn("Centrifuge disconnected:", ctx);
  });

  const sub = centrifuge.newSubscription(window.QUESTION_CHANNEL);

  sub.on("publication", function (ctx) {
    console.log("Centrifuge publication:", ctx);
    const { type, payload } = ctx.data || {};
    if (!type) return;

    switch (type) {
      case "question.grade_updated":
        updateQuestionGrade(payload);
        break;
      case "answer.created":
        appendAnswer(payload);
        bumpAnswersCount(+1);
        break;
      case "answer.grade_updated":
        updateAnswerGrade(payload);
        break;
      case "answer.correct_updated":
        updateAnswerCorrect(payload);
        break;
      default:
        // unknown event
        break;
    }
  });

  sub.subscribe();

  centrifuge.on("connecting", function (ctx) {
    // console.log("connecting", ctx);
  });

  centrifuge.on("connected", function (ctx) {
    // console.log("connected", ctx);
  });

  centrifuge.on("disconnected", function (ctx) {
    // console.log("disconnected", ctx);
  });

  centrifuge.connect();

  function updateQuestionGrade(p) {
    const like = document.querySelector('[data-question-id] .like-count');
    const dislike = document.querySelector('[data-question-id] .dislike-count');
    if (like && typeof p.like_count === "number") like.textContent = String(p.like_count);
    if (dislike && typeof p.dislike_count === "number") dislike.textContent = String(p.dislike_count);
  }

  function updateAnswerGrade(p) {
    const card = document
        .querySelector(`.grade-answer-btn[data-answer-id="${p.answer_id}"]`)
        ?.closest(".card");

    if (!card) return;

    const likeBtn = card.querySelector('.grade-answer-btn[data-is-like="true"]');
    const dislikeBtn = card.querySelector('.grade-answer-btn[data-is-like="false"]');

    // обновляем счётчики (для всех)
    if (likeBtn && typeof p.like_count === "number") {
        likeBtn.querySelector(".answer-like-count").textContent = p.like_count;
    }
    if (dislikeBtn && typeof p.dislike_count === "number") {
        dislikeBtn.querySelector(".answer-dislike-count").textContent = p.dislike_count;
    }

    // маркеры ТОЛЬКО для текущего пользователя
    if (
        p.user_id &&
        window.CURRENT_USER_ID &&
        String(p.user_id) === String(window.CURRENT_USER_ID)
    ) {
        const isLike = String(p.is_like) === "true";
        const active = !!p.active;

        if (likeBtn) {
          likeBtn.classList.toggle("liked-like", active && isLike);
          likeBtn.classList.toggle("btn-primary", active && isLike);
          likeBtn.classList.toggle("text-white", active && isLike);
          likeBtn.classList.toggle("btn-outline-secondary", !(active && isLike));
        }

        if (dislikeBtn) {
          dislikeBtn.classList.toggle("liked-dislike", active && !isLike);
          dislikeBtn.classList.toggle("btn-danger", active && !isLike);
          dislikeBtn.classList.toggle("text-white", active && !isLike);
          dislikeBtn.classList.toggle("btn-outline-secondary", !(active && !isLike));
        }
    }
    }

  function setAnswerCorrectUI_DOM(card, isCorrect) {
    if (!card) return;

    card.classList.toggle("answer-correct", isCorrect);

    const header = card.querySelector("header");
    const badge = card.querySelector(".answer-correct-badge");

    if (isCorrect) {
      if (!badge && header) {
        const span = document.createElement("span");
        span.className = "badge text-bg-primary answer-correct-badge";
        span.innerHTML = '<i class="bi bi-check2-square me-1"></i>Решение';
        header.appendChild(span);
      }
    } else {
      if (badge) badge.remove();
    }
  }



  function updateAnswerCorrect(p) {
    const btn = document.querySelector(`.grade-answer-btn[data-answer-id="${p.answer_id}"]`);
    const card = btn?.closest(".card");
    if (!card) return;

    const isCorrect = !!p.is_correct;

    // Секция с ответами
    const section = card.closest("section");
    if (!section) return;

    if (isCorrect) {
      // Если текущий ответ стал правильным — снимаем "correct" со всех остальных
      const allCards = section.querySelectorAll("article.card.shadow-sm.mb-3");
      allCards.forEach((c) => {
        const isThis = c === card;
        setAnswerCorrectUI_DOM(c, isThis); // текущему ставим true, остальным false

        const cb = c.querySelector(".answer-correct-toggle");
        if (cb) cb.checked = isThis;
      });
    } else {
      setAnswerCorrectUI_DOM(card, false);

      const cb = card.querySelector(".answer-correct-toggle");
      if (cb) cb.checked = false;
    }
  }

  function bumpAnswersCount(delta) {
    const h2 = document.querySelector("h2.h5.mb-3");
    if (!h2) return;
    // ожидаем формат "Ответы (N)"
    const m = h2.textContent.match(/\((\d+)\)/);
    if (!m) return;
    const n = parseInt(m[1], 10);
    if (Number.isNaN(n)) return;
    h2.textContent = h2.textContent.replace(/\(\d+\)/, `(${n + delta})`);
  }

  function appendAnswer(a) {
    const section = document.querySelector("section.mt-4");
    if (!section) return;
    console.log("Appending new answer:", a);

    // вставим перед формой нового ответа (последняя карточка)
    const formCard = section.querySelector(".card.shadow-sm:last-of-type");
    const wrapper = document.createElement("div");
    wrapper.innerHTML = renderAnswerCard(a);
    const node = wrapper.firstElementChild;
    if (node) {
      if (formCard) formCard.parentNode.insertBefore(node, formCard);
      else section.appendChild(node);
    }
  }

  function escapeHtml(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function renderAnswerCard(a) {
    const img = escapeHtml(a.author?.img_url || "");
    const nick = escapeHtml(a.author?.nickname || "user");
    const text = escapeHtml(a.text || "");
    const created = escapeHtml(a.created_at || "");

    return `
      <article class="card shadow-sm mb-3 ${a.is_correct ? "answer-correct" : ""}">
        <div class="card-body">
          <div class="row g-3 align-items-start">
            <div class="col-3 col-sm-2 col-md-2 col-lg-2 d-flex flex-column align-items-center gap-2">
              <img src="${img}" alt="Аватар" class="img-thumbnail rounded" style="object-fit: cover; width: 50px; height: 50px;">
              <div class="d-flex gap-2">
                <button class="btn btn-outline-secondary btn-sm grade-answer-btn d-flex align-items-center position-relative"
                        type="button"
                        aria-label="like answer"
                        data-answer-id="${a.id}"
                        data-is-like="true">
                  <i class="bi bi-hand-thumbs-up me-1"></i>
                  <span class="answer-like-count small text-muted">${a.like_count ?? 0}</span>
                </button>
                <button class="btn btn-outline-secondary btn-sm grade-answer-btn d-flex align-items-center position-relative"
                        type="button"
                        aria-label="dislike answer"
                        data-answer-id="${a.id}"
                        data-is-like="false">
                  <i class="bi bi-hand-thumbs-down me-1"></i>
                  <span class="answer-dislike-count small text-muted">${a.dislike_count ?? 0}</span>
                </button>
              </div>
            </div>

            <div class="col">
              <header class="d-flex justify-content-between align-items-center mb-2">
                <div class="small text-body-secondary">
                  <a href="/users/${a.author?.id ?? ""}" class="link-secondary">${nick}</a> •
                  <time datetime="data">${created}</time>
                </div>
                ${a.is_correct ? `<span class="badge text-bg-primary answer-correct-badge"><i class="bi bi-check2-square me-1"></i>Решение</span>` : ""}
              </header>

              <p class="mb-3">${text}</p>
            </div>
          </div>
        </div>
      </article>
    `;
  }
})();
