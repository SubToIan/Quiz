function editQuiz(id) {
    fetch(`/api/quizzes/${id}`)
    .then(response => response.json())
    .then(quiz => {
        console.log(quiz)
        document.getElementById('quiz-id').value = quiz.id;
        document.getElementById('quiz-question').value = quiz.question;
        document.getElementById('quiz-choice1').value = quiz.choices[0];
        document.getElementById('quiz-choice2').value = quiz.choices[1];
        document.getElementById('quiz-choice3').value = quiz.choices[2];
        document.getElementById('quiz-choice4').value = quiz.choices[3];
        document.getElementById('quiz-answer').value = quiz.answer;

    });
}

function saveQuiz(event) {
    event.preventDefault();

    const id = document.getElementById('quiz-id').value;
    const question = document.getElementById('quiz-question').value
    const choices = [
        document.getElementById('quiz-choice1').value,
        document.getElementById('quiz-choice2').value,
        document.getElementById('quiz-choice3').value,
        document.getElementById('quiz-choice4').value
    ];
    const answer = document.getElementById('quiz-answer').value
    console.log(answer.value)

    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/quizzes/${id}` : '/api/quizzes';

    console.log(JSON.stringify({ question, choices, answer}))
    fetch(url, {
        method: method,
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify({ question, choices, answer})
    })
    .then(response => response.json())
    .then(data=> { 
        console.log(data)
        location.reload();
    });

}

function deleteQuiz(id) {
    fetch(`/api/quizzes/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then (data => {
        console.log(data)
        if (data.code == 200) {
            const quizElement = document.getElementById(`quiz-${id}`);
            quizElement.remove();
        } else {
            alert('Error deleting quiz');
        }
    });
}